import datetime, sys
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine,\
                     Float, update
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication

def odd_even(message):
    msg = QMessageBox()
    msg.setStyleSheet("font: 10pt Arial; color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle('Reset parameter')
    msg.exec_()

try:
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
    message = "Reset parameter successful!"
except:
    message = "Reset parameter failed"

app = QApplication(sys.argv)
app.setStyle("Windows")
sys.exit(odd_even(message))
app.exec_()

