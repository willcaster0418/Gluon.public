from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

# create the app
# configure the SQLite database, relative to the app instance folder
# initialize the app with the extension
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+pymysql://oms@localhost:3306/AUTH"
db = SQLAlchemy(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(32))

with app.app_context():
    db.create_all()

user = User(
            username="fury8208",
            email="fury8208@gmail.com",
)

with app.app_context():
    db.session.add(user)
    db.session.commit()
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    for user in users:
        print(user)
        import pdb;pdb.set_trace()