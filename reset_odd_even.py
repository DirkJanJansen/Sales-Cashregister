import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine,\
                     Float, update

metadata = MetaData()
params = Table('params', metadata,
       Column('paramID', Integer(), primary_key=True),
       Column('item', String),
       Column('value', Float))

engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
con = engine.connect()

myear = int(str(datetime.date.today())[0:4])
updeven = update(params).where(params.c.paramID == 4).values(value = int(myear%2))
con.execute(updeven)
