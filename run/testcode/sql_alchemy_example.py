import sqlalchemy as db
from sqlalchemy import Integer, String, Column
uri =  "mariadb+pymysql://oms@localhost:3306/AUTH"
engine = db.create_engine(uri)

connection = engine.connect()

metadata = db.MetaData()
table = db.Table('user', metadata, Column("id", Integer), Column("username", String(40)))
print(table.columns.keys())

query = table.select()
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)