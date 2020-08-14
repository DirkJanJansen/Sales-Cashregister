# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:09:47 2020

@author: Dirk
"""

from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine,\
                     Float, select, update,insert, delete, func, and_, ForeignKey
                     
metadata = MetaData()
buttons = Table('buttons', metadata,
    Column('buttonID', Integer(), primary_key=True),
    Column('buttontext', String),
    Column('reference', String),
    Column('barcode',  String),
    Column('accent', Integer),
    Column('bg_color', String))


engine = create_engine('postgresql+psycopg2://postgres@localhost/catering')
con = engine.connect()

selbtn = select([buttons]).order_by(buttons.c.buttonID)
rpbtn = con.execute(selbtn) 

#default color = #FFFFF0

#color chooser https://htmlcolorcodes.com

#colors per row all pages the same color scheme

x = 0
for row in rpbtn:
    if x%18 < 3:
        color = '#e36f43'  
        upd = update(buttons).where(buttons.c.buttonID == row[0])\
          .values(bg_color = color)
        con.execute(upd)
        print(row[0], color)
    elif x%18 < 6:
        color = '#e3ba21'
        upd = update(buttons).where(buttons.c.buttonID == row[0])\
          .values(bg_color = color)
        con.execute(upd)
        print(row[0], color)
    elif x%18 < 9:
        color = '#aee84e'
        upd = update(buttons).where(buttons.c.buttonID == row[0])\
          .values(bg_color = color)
        con.execute(upd)
        print(row[0], color)
    elif x%18 < 12:
        color = '#5fa5df'
        upd = update(buttons).where(buttons.c.buttonID == row[0])\
          .values(bg_color = color)
        con.execute(upd)
        print(row[0],color)
    elif x%18 < 15:
        color = '#d75898'
        upd = update(buttons).where(buttons.c.buttonID == row[0])\
          .values(bg_color = color)
        con.execute(upd)
        print(row[0], color)
    elif x%18 < 18:
        color = '#f1c40f'
        upd = update(buttons).where(buttons.c.buttonID == row[0])\
          .values(bg_color = color)
        con.execute(upd)
        print(row[0], color)
    x += 1
        
        

 
   
      