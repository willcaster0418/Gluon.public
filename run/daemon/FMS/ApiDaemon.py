from flask import Flask
from flask import Blueprint, jsonify

from pkg.auth.oauth2 import config_oauth
from pkg.auth.models import db
from pkg.auth.oauth2 import require_oauth
import os, logging, datetime
from authlib.integrations.flask_oauth2 import current_token

def initialize():
    nstr = datetime.datetime.now().strftime("%Y%m%d")
    try:
        logging.basicConfig(
            filename = f"/gluon/log/{nstr}.ApiDaemon.log",
            format ='%(asctime)s:%(levelname)s:%(message)s',
            datefmt ='%m/%d/%Y %I:%M:%S %p',
            level = logging.INFO
        )
    except Exception as e:
        logging.info(f"Error(ApiDaemon.py >> initialize) : {str(e)}")
        
    try:
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict if name != "CoinTrader"]
        for logger in loggers:
            logger.setLevel(logging.CRITICAL)
            # log logger name
            logging.info(f"Logger {logger.name} set to CRITICAL")
    except Exception as e:
        logging.info(f"Error(ApiDaemon.py >> initialize) : {str(e)}")
    logging.info("---*--- Api Daemon ---*---")

initialize()

############################################################################################################
# application callback should registered here
#
############################################################################################################
bp = Blueprint('home', __name__)
@bp.route('/me')
@require_oauth('user')
def api_me():
    user = current_token.user
    return jsonify(uid=user.uid, username=user.name)

############################################################################################################
# source code originated from
# https://github.com/authlib/example-oauth2-server
############################################################################################################
def create_app(app = None, config=None, url_prefix='/auth/'):
    if app == None:
        app = Flask(__name__)

    # load default configuration
    # app.config.from_object('website.settings')

    # load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    db.init_app(app)
    # Create tables if they do not exist already
    #with app.app_context():
    #    db.create_all()
    config_oauth(app)
    app.register_blueprint(bp, url_prefix=url_prefix)

    return app

app = Flask(__name__)

app = create_app(app = app, config = {
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'mariadb+pymysql://oms@localhost:3306/AUTH',
}, url_prefix='/api')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)