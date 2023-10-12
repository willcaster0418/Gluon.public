from flask import Flask
from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify

from pkg.auth.oauth2 import config_oauth
from pkg.auth.models import db, User, OAuth2Client, OAuth2Token
from pkg.auth.oauth2 import authorization, require_oauth
import os, time, logging, json, datetime
from werkzeug.security import gen_salt
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error

def initialize():
    nstr = datetime.datetime.now().strftime("%Y%m%d")
    try:
        logging.basicConfig(
            filename = f"/gluon/log/{nstr}.AuthDaemon.log",
            format ='%(asctime)s:%(levelname)s:%(message)s',
            datefmt ='%m/%d/%Y %I:%M:%S %p',
            level = logging.INFO
        )
    except Exception as e:
        logging.info(f"Error(AuthDaemon.py >> initialize) : {str(e)}")
        
    try:
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict if name != "CoinTrader"]
        for logger in loggers:
            logger.setLevel(logging.CRITICAL)
            # log logger name
            logging.info(f"Logger {logger.name} set to CRITICAL")
    except Exception as e:
        logging.info(f"Error(AuthDaemon.py >> initialize) : {str(e)}")
    logging.info("---*--- Auth Daemon ---*---")

initialize()

def current_user():
    if 'uid' in session:
        uid = session['uid']
        return db.session.get(User, uid)
    return None

def jsonify_client(clients, result = {}):
    result.update({"client" : [c.client_info for c in clients]
                    , "client_meta" : [c.client_metadata for c in clients]})

    return jsonify(result)


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

bp = Blueprint('home', __name__)
@bp.route('/signup', methods=['POST'])
def signup():
    try:
        uid = request.form.get('uid', type=str, default='default')
        name = request.form.get('name', type=str, default='default')
        password = request.form.get('password', type=str, default='default')
        logging.info(f"# signup => uid : {uid}, name : {name}, password : {password}")

        user = User.query.filter_by(uid=uid).first()
        if not user:
            user = User(uid=uid, name=name, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"status" : True})
        else:
            return jsonify({"status" : False, "error" : "user already exists"})
    except Exception as e:
        return jsonify({"status" : False, "error" : str(e)})

@bp.route('/signin', methods=['POST'])
def signin():
    try:
        uid = request.form.get('uid', type=str, default='default')
        password = request.form.get('password', type=str, default='default')
        logging.info(f"# signin => uid : {uid}, password : {password}")
        user = User.query.filter_by(uid=uid).first()
        if user and user.check_password(password):
            session['uid'] = user.uid
            return jsonify({"status" : True, "uid" : user.uid, "uname" : user.name})
        else:
            return jsonify({"status" : False, "error" : "password error"})
    except Exception as e:
        return jsonify({"status" : False, "error" : str(e)})

@bp.route('/signout', methods=['POST', 'GET'])
def signout():
    if 'uid' in session:
        del session['uid']
        return jsonify({"status" : True})
    else:
        return jsonify({"status" : False})

@bp.route('/list_sso', methods=['POST'])
def list_sso():
    try:
        user = current_user()
        if not user:
            logging.info("# list_sso : no user")
            return jsonify({"status" : False})
        logging.info(f"# list_sso => user : {user.uid}")

        req = {}
        req['name']  = request.form.get('name', type=str, default='default')
        clients = OAuth2Client.query.filter_by(
                    user_id=user.uid, 
                    name=req['name']).all()

        return jsonify_client(clients, result={"status" : True})
    except Exception as e: 
        return jsonify({"status" : False, "error" : str(e)})

@bp.route('/register_sso', methods=['POST'])
def register_sso():
    try:
        req = {}
        req['uid']  = request.form.get('uid', type=str, default='default')
        req['name']  = request.form.get('name', type=str, default='default')
        req['scope'] = request.form.get('scope', type=str, default='default')
        req['grant_type'] = request.form.get('grant_type', type=str, default='password')
        
        logging.info(f"# register_sso => req : {req}")
        
        clients = db.session.query(OAuth2Client).filter_by(
            user_id=req['uid'],
            name=req['name']).all()

        if len(clients) > 0:
            return jsonify_client(clients, result={"status" : False})
    
        client_id = gen_salt(24)
        client_id_issued_at = int(time.time())
        client = OAuth2Client(
            client_id=client_id,
            client_id_issued_at=client_id_issued_at,
            user_id=req['uid'],
            name=req['name']
        )
        
        client_metadata = {
            "scope": req["scope"],
            "grant_types": split_by_crlf(req['grant_type']),
            "token_endpoint_auth_method" : "client_secret_basic"
        }
        client.set_client_metadata(client_metadata)
        client.client_secret = gen_salt(48)
        
        db.session.add(client)
        db.session.commit()

        clients = OAuth2Client.query.filter_by(
                    user_id=req['uid'], 
                    name=req['name']).all()

        return jsonify_client(clients, result={"status" : True})
    except Exception as e:
        return jsonify({"status" : False, "error" : str(e)})

@bp.route('/token', methods=['POST'])
def issue_token():
    logging.info(f"# issue_token")
    if current_user():
        return authorization.create_token_response()
    else:
        return jsonify({"status" : False, "error" : "invalid session"})

#####################################
@bp.route('/validate_token', methods=['POST'])
@require_oauth('user')
def validate_token():
    #curl -k -H "Authorization: Bearer ${access_token}" https://localhost:3000/api/me
    user = current_token.user
    return jsonify({"status" : True, "uid" : user.uid})

@require_oauth()
def not_validate_token():
    return jsonify({"status" : False})
#####################################

@bp.route('/revoke', methods=['POST'])
def revoke_token():
    logging.info(f"# revoke_token")
    return authorization.create_endpoint_response('revocation')

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
    with app.app_context():
        db.create_all()
    config_oauth(app)
    app.register_blueprint(bp, url_prefix=url_prefix)

    return app

app = Flask(__name__)

app = create_app(app = app, config = {
    'SECRET_KEY': 'secret',
    'OAUTH2_REFRESH_TOKEN_GENERATOR': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_DATABASE_URI': 'mariadb+pymysql://oms@localhost:3306/AUTH',
}, url_prefix='/auth')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)