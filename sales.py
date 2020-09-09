import sys, random, barcode, datetime, os, subprocess, shutil, re
from math import sqrt
from barcode.writer import ImageWriter 

from PyQt5.QtCore import Qt, QSize, QRegExp, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie, QRegExpValidator, QColor,\
            QImage, QPainter
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel, QPushButton,\
        QMessageBox, QSpinBox, QComboBox, QTextEdit, QApplication, QWidget,\
        QVBoxLayout, QTableView, QStyledItemDelegate, QCheckBox, QPlainTextEdit
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine,\
                     Float, select, update,insert, delete, func, and_, ForeignKey

def alertText(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.setWindowTitle('Warning message')
    msg.exec_() 
    
def actionOK(message):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle('Information message')
    msg.exec_()
         
def windowClose(self):
    self.close()
    sys.exit()
    
def printEan(self, x1 ,y1):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msgBox.setWindowTitle("Printing barcodeID")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setFont(QFont("Arial", 10))
    msgBox.setText("Do you want to print the barcode for scanning?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        self.printer = QPrinter()
        self.pixmap = QPixmap(self.path+str(self.mbarcode)+'.png')
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
             painter = QPainter(self.printer)
             rect = painter.viewport()
             size = self.pixmap.size()
             size.scale(rect.size(), Qt.KeepAspectRatio)
             painter.setViewport(rect.x(), rect.y(), x1 , y1) #aspect and size for barcodes Ean 
             painter.setWindow(self.pixmap.rect())
             painter.drawPixmap(0, 0, self.pixmap)
             
def reprintForms(path):
    filelist = []
    for file in os.listdir(path):
        if file[-4:] == '.txt':
            filelist.append(file)
    class combo(QDialog):
        def __init__(self, parent=None):
              super(combo, self).__init__(parent)
              self.setWindowTitle("Reprinting forms")
              self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
              self.setFont(QFont("Arial", 10))
              self.setStyleSheet("background-color: #D9E1DF") 
                  
              grid = QGridLayout()
              grid.setSpacing(20)
              
              pyqt = QLabel()
              movie = QMovie('./logos/pyqt.gif')
              pyqt.setMovie(movie)
              movie.setScaledSize(QSize(240,80))
              movie.start()
              grid.addWidget(pyqt, 0 ,0, 1, 2)
            
              logo = QLabel()
              pixmap = QPixmap('./logos/logo.jpg')
              logo.setPixmap(pixmap)
              grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
              
              self.cb = QComboBox()
              self.cb.setFixedWidth(700)
              self.cb.setFont(QFont("Arial",12))
              self.cb.setStyleSheet("color: black;  background-color: #F8F7EE")
              for item in range(len(filelist)):
                  self.cb.addItem(filelist[item])
                  self.cb.model().sort(0)
              grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignRight)
                         
              def cbChanged():
                  self.cb.setCurrentText(self.cb.currentText())
              self.cb.currentTextChanged.connect(cbChanged)
               
              self.q2Edit = QLineEdit('1')
              self.q2Edit.setStyleSheet("background: #F8F7EE")
              self.q2Edit.setFixedWidth(40)
              self.q2Edit.setFont(QFont("Arial",12))
              reg_ex = QRegExp("^[0-9]{1,2}$")
              input_validator = QRegExpValidator(reg_ex, self.q2Edit)
              self.q2Edit.setValidator(input_validator)
              
              def q2Changed():
                  self.q2Edit.setText(self.q2Edit.text())
              self.q2Edit.textChanged.connect(q2Changed) 
              
              def printForm():
                  filename = self.cb.currentText()
                  copies = int(self.q2Edit.text())
                  for x in range(0, copies):
                      if sys.platform == 'win32':
                          os.startfile(path+filename, "print")
                      else:
                          os.system("lpr "+path+filename)
                  message = 'Printing'
                  actionOK(message)
                  
              grid.addWidget(QLabel('Copies'), 2, 2, 1, 1, Qt.AlignTop | Qt.AlignRight)
              grid.addWidget(self.q2Edit, 2, 2, 1, 1, Qt.AlignBottom | Qt.AlignRight)
              
              plbl = QLabel()
              pmap = QPixmap('./logos/printer.png')
              plbl.setPixmap(pmap)
              grid.addWidget(plbl , 2, 0, 2, 2)
                    
              cancelBtn = QPushButton('Close')
              cancelBtn.clicked.connect(self.close)  
                
              grid.addWidget(cancelBtn, 3, 1, 1, 1, Qt.AlignRight)
              cancelBtn.setFont(QFont("Arial",10))
              cancelBtn.setFixedWidth(90)
              cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")    
              
              printBtn = QPushButton('Printen')
              printBtn.clicked.connect(lambda: printForm())  
                
              grid.addWidget(printBtn,  3, 2)
              printBtn.setFont(QFont("Arial",10))
              printBtn.setFixedWidth(90)
              printBtn.setStyleSheet("color: black;  background-color: gainsboro")    
                  
              grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
                
              self.setLayout(grid)
              self.setGeometry(900, 200, 150, 150)
              
    win = combo()
    win.exec_()
    
def countTurnover(mindex):
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('ID', Integer, primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('item_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
 
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Countings gross turnover")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            q1Edit = QLineEdit('20')
            q1Edit.setFixedWidth(100)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            
            lbl4 = QLabel('')
            grid.addWidget(lbl4, 2, 0)

            def q1Changed():
                q1Edit.setText(q1Edit.text())
            q1Edit.textChanged.connect(q1Changed)
            
            if mindex == 0:
                reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}-[01]{1}[0-9]{1}-[0123]{1}[0-9]{1}$")
                input_validator = QRegExpValidator(reg_ex, q1Edit)
                q1Edit.setValidator(input_validator)
                lbl1 = QLabel('Daily <yyyy-mm-dd>')
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
            elif mindex == 1:
                reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}-[01]{1}[0-9]{1}$")
                input_validator = QRegExpValidator(reg_ex, q1Edit)
                q1Edit.setValidator(input_validator)
                lbl1 = QLabel('Monthly <yyyy-mm>')
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
            elif mindex == 2:
                reg_ex = QRegExp("^[2]{1}[0]{1}[0-9]{2}$")
                input_validator = QRegExpValidator(reg_ex, q1Edit)
                q1Edit.setValidator(input_validator)
                lbl1 = QLabel('Yearly <yyyy>')
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
                          
            def counting(mindex):
                mdate = str(q1Edit.text())

                if mindex == 0 and len(mdate) == 10:
                    selsales = select([sales]).where(sales.c.mutation_date == mdate)
                elif mindex == 1 and len(mdate) == 7:
                    selsales = select([sales]).where(sales.c.mutation_date.like(mdate+'%'))
                elif mindex == 2 and len(mdate) == 4:
                    selsales = select([sales]).where(sales.c.mutation_date.like(mdate+'%'))
                else:
                    return
                
                rpsales = con.execute(selsales)
                
                total = 0
                totalvat = 0
                for row in rpsales:
                    total += row[6]
                    totalvat += row[7]               
                 
                lbl2 = QLabel('Totals: '+'{:12.2f}'.format(total)+'           Totals-VAT: '+'{:12.2f}'.format(totalvat)) 
                lbl2.setFont(QFont("Arial", 10))
                grid.addWidget(lbl2, 2, 0, 1, 3) 
                     
            applyBtn = QPushButton('Count')
            applyBtn.clicked.connect(lambda: counting(mindex))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 4, 2)

            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 4, 1, 1, 1, Qt.AlignRight)                 

            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 5, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
             
def turnoverMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Turnover Menu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(300)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Daily gross turnover')
            self.k0Edit.addItem('Monthly gross turnover')
            self.k0Edit.addItem('Yearly gross turnover')
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
            
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                countTurnover(mindex)
                     
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
                                                   
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 

def accountMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("AccountMenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(280)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('New account')
            self.k0Edit.addItem('View / Change accounts')
                                       
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    emplAccess()
                elif mindex == 1:
                    emplRequest()

            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
    
def articleMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("ArticleMenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(300)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Insert new articles')
            self.k0Edit.addItem('View / Change articles')
            self.k0Edit.addItem('Booking loss articles')
            self.k0Edit.addItem('View loss articles')
                                         
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    insertArticles()
                elif mindex == 1:
                    mflag = 0
                    articleRequest(mflag, 0)
                elif mindex == 2:
                    flag = 2
                    articleRequest(flag, 0)
                elif mindex == 3:
                    requestLoss()

            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()
    
def newSupplier():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            
            self.setWindowTitle("Insert new supplier")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
    
            grid = QGridLayout()
            grid.setSpacing(20)
            
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
  
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
            
            metadata = MetaData()
            suppliers = Table('suppliers', metadata,
                Column('supplierID', Integer, primary_key=True),
                Column('company_name', String),
                Column('street', String),
                Column('housenumber', String),
                Column('zipcode', String),
                Column('residence', String),
                Column('telephone', String),
                Column('email', String),
                Column('addition', String))
            
            engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
            con = engine.connect()
  
            try:
               supplnr = (con.execute(select([func.max(suppliers.c.supplierID, type_=Integer)])).scalar())
               supplnr += 1
            except:
               supplnr = 1
             
            #supplierID
            self.q1Edit = QLineEdit(str(supplnr))
            self.q1Edit.setFixedWidth(100)
            self.q1Edit.setDisabled(True)
            self.q1Edit.setStyleSheet('color: black')
            self.q1Edit.setFont(QFont("Arial", 10))
            
            #Company-name
            self.q2Edit = QLineEdit()
            self.q2Edit.setFixedWidth(300)
            self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q2Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,40}$")
            input_validator = QRegExpValidator(reg_ex, self.q2Edit)
            self.q2Edit.setValidator(input_validator)
 
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            #Street
            self.q3Edit = QLineEdit()
            self.q3Edit.setFixedWidth(300)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,40}$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
            self.q3Edit.setValidator(input_validator)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            #housenumber
            self.q4Edit = QLineEdit()
            self.q4Edit.setFixedWidth(100)
            self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q4Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,13}$")
            input_validator = QRegExpValidator(reg_ex, self.q4Edit)
            self.q4Edit.setValidator(input_validator)

            def q4Changed():
                self.q4Edit.setText(self.q4Edit.text())
            self.q4Edit.textChanged.connect(q4Changed)
            
            #Zip-code
            self.q5Edit = QLineEdit()
            self.q5Edit.setFixedWidth(100)
            self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q5Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^[0-9]{4}[0-9A-Za-z]{0,3}$")
            input_validator = QRegExpValidator(reg_ex, self.q5Edit)
            self.q5Edit.setValidator(input_validator)
            
            def q5Changed():
                self.q5Edit.setText(self.q5Edit.text())
            self.q5Edit.textChanged.connect(q5Changed)
            
            #residence
            self.q6Edit = QLineEdit()
            self.q6Edit.setFixedWidth(300)
            self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q6Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^.{1,40}$")
            input_validator = QRegExpValidator(reg_ex, self.q6Edit)
            self.q6Edit.setValidator(input_validator)
            
            def q6Changed():
                self.q6Edit.setText(self.q6Edit.text())
            self.q6Edit.textChanged.connect(q6Changed)
            
            #telephone
            self.q7Edit = QLineEdit()
            self.q7Edit.setFixedWidth(150)
            self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q7Edit.setFont(QFont("Arial", 10))
            reg_ex = QRegExp("^[+0-9]{0,15}$")
            input_validator = QRegExpValidator(reg_ex, self.q7Edit)
            self.q7Edit.setValidator(input_validator)
            
            def q7Changed():
                self.q7Edit.setText(self.q7Edit.text())
            self.q7Edit.textChanged.connect(q7Changed)
            
            #email
            self.q8Edit = QLineEdit()
            self.q8Edit.setFixedWidth(300)
            self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q8Edit.setFont(QFont("Arial", 10))
             
            def q8Changed():
                self.q8Edit.setText(self.q8Edit.text())
            self.q8Edit.textChanged.connect(q8Changed)
            
            #additions-country-bound
            self.q9Edit = QPlainTextEdit()
            self.q9Edit.setFixedSize(300,100)
            self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q9Edit.setFont(QFont("Arial", 10))
                                        
            def insertSupplier():
                mcompany = self.q2Edit.text()
                mstreet = self.q3Edit.text()
                mhousenr = self.q4Edit.text()
                mzipcode = self.q5Edit.text().upper()
                mresid = self.q6Edit.text()
                mtel = self.q7Edit.text()
                def memailContr(memail):
                    ab = re.compile("[^@]+@[^@]+\.[^@]+$")
                    if ab.match(memail):
                        return(True)
                    else:
                        return(False)
                if memailContr(self.q8Edit.text()) and len(self.q8Edit.text()) < 201:
                    memail = self.q8Edit.text()
                else:
                    message = 'No valid e-mail adress!'
                    alertText(message)
                    return
                if len(self.q9Edit.toPlainText()) > 1000:
                    message = 'No more then 1000 characters allowed!'
                    alertText(message)
                    return
                else:
                    maddition = self.q9Edit.toPlainText()
                
                inssup = insert(suppliers).values(supplierID=supplnr,company_name=mcompany,\
                  street=mstreet,housenumber=mhousenr, zipcode = mzipcode, residence = mresid,
                  telephone=mtel,email=memail,addition=maddition)
                con.execute(inssup)
                self.close()
            
            lblq1 = QLabel('Supplier id')
            grid.addWidget(lblq1, 1, 0)
            grid.addWidget(self.q1Edit, 1, 1)
            
            lblq2 = QLabel('Company name')
            grid.addWidget(lblq2, 2, 0)
            grid.addWidget(self.q2Edit, 2, 1)
            
            lblq3 = QLabel('Street')
            grid.addWidget(lblq3, 3, 0)
            grid.addWidget(self.q3Edit, 3, 1)
            
            lblq4 = QLabel('Housenumber')
            grid.addWidget(lblq4, 4, 0)
            grid.addWidget(self.q4Edit, 4, 1)
            
            lblq5 = QLabel('Zip-code')
            grid.addWidget(lblq5, 5, 0)
            grid.addWidget(self.q5Edit, 5, 1)
             
            lblq6 = QLabel('Residence')
            grid.addWidget(lblq6, 6, 0)
            grid.addWidget(self.q6Edit, 6, 1)
            
            lblq7 = QLabel('Telephone')
            grid.addWidget(lblq7, 7, 0)
            grid.addWidget(self.q7Edit, 7, 1)
            
            lblq8 = QLabel('E-Mail')
            grid.addWidget(lblq8, 8, 0)
            grid.addWidget(self.q8Edit, 8, 1)
            
            lblq9= QLabel('Addional country\nbound data\nVAT-number\nChamber of commerce')
            grid.addWidget(lblq9, 9, 0)
            grid.addWidget(self.q9Edit, 9, 1)
          
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insertSupplier())  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 10, 1, 1, 1, Qt.AlignRight)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 10, 0, 1, 2, Qt.AlignCenter)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 11, 0, 1, 2, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()
    
def requestSupplier():
    metadata = MetaData()
    suppliers = Table('suppliers', metadata,
        Column('supplierID', Integer, primary_key=True),
        Column('company_name', String),
        Column('street', String),
        Column('housenumber', String),
        Column('zipcode', String),
        Column('residence', String),
        Column('telephone', String),
        Column('email', String),
        Column('addition', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
     
    sel = select([suppliers]).order_by(suppliers.c.supplierID)
    if con.execute(sel).fetchone():
        selsup = select([suppliers]).order_by(suppliers.c.supplierID)
        rpsup = con.execute(selsup)
    else:
        message = "No records found!"
        alertText(message)
        return
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setWindowTitle('Suppliers request / change')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(changeSupplier)
            grid.addWidget(table_view, 0, 0)
                       
            reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            reglbl.setFont(QFont("Arial", 10))
            grid.addWidget(reglbl, 1, 0)
            
            self.setLayout(grid)
            self.setGeometry(800, 50, 1000, 600)
            self.setLayout(grid)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['Suppliernr', 'Company name', 'Street', 'Housenumber','Zip-code',\
              'Residence','Telephone', 'E-mail','Addional']
    
    data_list=[]
    for row in rpsup:
        data_list += [(row)]
         
    def changeSupplier(idx):
        suppliernr = idx.data()
        selsupl = select([suppliers]).where(suppliers.c.supplierID == suppliernr)
        rpsupl = con.execute(selsupl).first()
        if idx.column()== 0:
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    
                    self.setWindowTitle("Change supplier")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF") 
          
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    #supplierID
                    self.q1Edit = QLineEdit(str(rpsupl[0]))
                    self.q1Edit.setFixedWidth(100)
                    self.q1Edit.setDisabled(True)
                    self.q1Edit.setStyleSheet('color: black')
                    self.q1Edit.setFont(QFont("Arial", 10))
                    
                    #Company-name
                    self.q2Edit = QLineEdit(rpsupl[1])
                    self.q2Edit.setFixedWidth(300)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,40}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
         
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    #Street
                    self.q3Edit = QLineEdit(rpsupl[2])
                    self.q3Edit.setFixedWidth(300)
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,40}$")
                    input_validator = QRegExpValidator(reg_ex, self.q3Edit)
                    self.q3Edit.setValidator(input_validator)
                    
                    def q3Changed():
                        self.q3Edit.setText(self.q3Edit.text())
                    self.q3Edit.textChanged.connect(q3Changed)
                    
                    #housenumber
                    self.q4Edit = QLineEdit(rpsupl[3])
                    self.q4Edit.setFixedWidth(100)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q4Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,13}$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
        
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                    
                    #Zip-code
                    self.q5Edit = QLineEdit(rpsupl[4])
                    self.q5Edit.setFixedWidth(100)
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q5Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^[0-9]{4}[0-9A-Za-z]{0,3}$")
                    input_validator = QRegExpValidator(reg_ex, self.q5Edit)
                    self.q5Edit.setValidator(input_validator)
                    
                    def q5Changed():
                        self.q5Edit.setText(self.q5Edit.text())
                    self.q5Edit.textChanged.connect(q5Changed)
                    
                    #residence
                    self.q6Edit = QLineEdit(rpsupl[5])
                    self.q6Edit.setFixedWidth(300)
                    self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q6Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^.{1,40}$")
                    input_validator = QRegExpValidator(reg_ex, self.q6Edit)
                    self.q6Edit.setValidator(input_validator)
                    
                    def q6Changed():
                        self.q6Edit.setText(self.q6Edit.text())
                    self.q6Edit.textChanged.connect(q6Changed)
                    
                    #telephone
                    self.q7Edit = QLineEdit(rpsupl[6])
                    self.q7Edit.setFixedWidth(150)
                    self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q7Edit.setFont(QFont("Arial", 10))
                    reg_ex = QRegExp("^[+0-9]{0,15}$")
                    input_validator = QRegExpValidator(reg_ex, self.q7Edit)
                    self.q7Edit.setValidator(input_validator)
                    
                    def q7Changed():
                        self.q7Edit.setText(self.q7Edit.text())
                    self.q7Edit.textChanged.connect(q7Changed)
                    
                    #email
                    self.q8Edit = QLineEdit(rpsupl[7])
                    self.q8Edit.setFixedWidth(300)
                    self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q8Edit.setFont(QFont("Arial", 10))
                                
                    def q8Changed():
                        self.q8Edit.setText(self.q8Edit.text())
                    self.q8Edit.textChanged.connect(q8Changed)
                    
                    #additions-country-bound
                    self.q9Edit = QPlainTextEdit(rpsupl[8])
                    self.q9Edit.setFixedSize(300,100)
                    self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q9Edit.setFont(QFont("Arial", 10))

                    def updateSupplier():
                        mcompany = self.q2Edit.text()
                        mstreet = self.q3Edit.text()
                        mhousenr = self.q4Edit.text()
                        mzipcode = self.q5Edit.text().upper()
                        mresid = self.q6Edit.text()
                        mtel = self.q7Edit.text()
                        def memailContr(memail):
                            ab = re.compile("[^@]+@[^@]+\.[^@]+$")
                            if ab.match(memail):
                                return(True)
                            else:
                                return(False)
                        if memailContr(self.q8Edit.text()) and len(self.q8Edit.text()) < 201:
                            memail = self.q8Edit.text() 
                        else:
                            message = 'No valid e-mail adress!'
                            alertText(message)
                            return
                        if len(self.q9Edit.toPlainText()) > 1000:
                            message = 'No more then 1000 characters allowed!'
                            alertText(message)
                            return
                        else:
                            maddition = self.q9Edit.toPlainText()
                        
                        updsup = update(suppliers).where(suppliers.c.supplierID ==\
                          suppliernr).values(company_name=mcompany,\
                          street=mstreet,housenumber=mhousenr, zipcode=mzipcode,\
                          residence = mresid, telephone=mtel,email=memail,addition=maddition)
                        con.execute(updsup)
                        self.close()
                    
                    lblq1 = QLabel('Supplier id')
                    grid.addWidget(lblq1, 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                    
                    lblq2 = QLabel('Company name')
                    grid.addWidget(lblq2, 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1)
                    
                    lblq3 = QLabel('Street')
                    grid.addWidget(lblq3, 3, 0)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    lblq4 = QLabel('Housenumber')
                    grid.addWidget(lblq4, 4, 0)
                    grid.addWidget(self.q4Edit, 4, 1)
                    
                    lblq5 = QLabel('Zip-code')
                    grid.addWidget(lblq5, 5, 0)
                    grid.addWidget(self.q5Edit, 5, 1)
                    
                    lblq6 = QLabel('Residence')
                    grid.addWidget(lblq6, 6, 0)
                    grid.addWidget(self.q6Edit, 6, 1)
                    
                    lblq7 = QLabel('Telephone')
                    grid.addWidget(lblq7, 7, 0)
                    grid.addWidget(self.q7Edit, 7, 1)
                    
                    lblq8 = QLabel('E-Mail')
                    grid.addWidget(lblq8, 8, 0)
                    grid.addWidget(self.q8Edit, 8, 1)
                    
                    lblq9= QLabel('Addional country\nbound data')
                    grid.addWidget(lblq9, 9, 0)
                    grid.addWidget(self.q9Edit, 9, 1)
                  
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updateSupplier())  
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(90)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(applyBtn, 10, 1, 1, 1, Qt.AlignRight)
                    
                    closeBtn = QPushButton('Close')
                    closeBtn.clicked.connect(self.close)  
                    closeBtn.setFont(QFont("Arial",10))
                    closeBtn.setFixedWidth(90)
                    closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(closeBtn, 10, 1, 1, 1, Qt.AlignCenter)
                         
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 11, 0, 1, 2, Qt.AlignCenter)
                   
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 350, 100)
                        
            window = Widget()
            window.exec_()
    
    win = Widget(data_list, header)
    win.exec_()
    
def handleInvoices():
    metadata = MetaData()
    invoices = Table('invoices', metadata,
       Column('invoiceID', Integer, primary_key=True),
       Column('barcode', String),
       Column('description', String),
       Column('delivery', Float),
       Column('item_price', Float),
       Column('supplierID', Integer),
       Column('orderlineID', Integer),
       Column('paydate', String),
       Column('bookdate', String),
       Column('item_unit', String))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
    sel = select([invoices]).order_by(invoices.c.supplierID, invoices.c.paydate)
    if con.execute(sel).fetchone():
        selinv = select([invoices]).order_by(invoices.c.supplierID, invoices.c.paydate)
        rpinv = con.execute(selinv)
    else:
        message = "no records found!"
        alertText(message)
        return
    class tableView(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(300, 50, 900, 900)
            self.setWindowTitle('Paying invoices suppliers')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(invoicePaying)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['InvoiceID', 'Barcode', 'Description', 'Deliveries', 'Itemprice',\
              'SupplierID', 'OrderlineID','Paydate','Bookdate','Item-unit']
    
    data_list=[]
    for row in rpinv:
        data_list += [(row)]
    
    def invoicePaying(idx):
        paynr=idx.data()
        selinv = select([invoices]).where(invoices.c.invoiceID==paynr)
        rpinv = con.execute(selinv).first()
        if idx.column()==0:
            class Window(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Paying invoice supplier")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setFont(QFont('Arial', 10))   
                    self.setStyleSheet("background-color: #D9E1DF")
                    
                    #invoiceID
                    q1Edit = QLineEdit(str(rpinv[0]))
                    q1Edit.setCursorPosition(0)
                    q1Edit.setFixedWidth(100)
                    q1Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q1Edit.setDisabled(True)
                                    
                    #barcode
                    q2Edit = QLineEdit(rpinv[1])
                    q2Edit.setFixedWidth(130)
                    q2Edit.setAlignment(Qt.AlignRight)
                    q2Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q2Edit.setDisabled(True)
                     
                    #description
                    q3Edit = QLineEdit(rpinv[2])
                    q3Edit.setFixedWidth(300)
                    q3Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q3Edit.setDisabled(True)
                                               
                    #deliveries
                    q4Edit = QLineEdit('{:12.2f}'.format(rpinv[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setAlignment(Qt.AlignRight)
                    q4Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q4Edit.setDisabled(True)
                    
                    #item-price
                    q5Edit = QLineEdit('{:12.2f}'.format(rpinv[4]))
                    q5Edit.setFixedWidth(100)
                    q5Edit.setAlignment(Qt.AlignRight)
                    q5Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q5Edit.setDisabled(True)
                    
                    #supplierID
                    q6Edit = QLineEdit(str(rpinv[5]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setAlignment(Qt.AlignRight)
                    q6Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q6Edit.setDisabled(True)
                    
                    #orderlineID
                    q7Edit = QLineEdit(str(rpinv[6]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setAlignment(Qt.AlignRight)
                    q7Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q7Edit.setDisabled(True)
                    
                    #paydate
                    q8Edit = QLineEdit(str(rpinv[7]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setAlignment(Qt.AlignRight)
                    q8Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q8Edit.setDisabled(True)
                    
                    #item_unit
                    q9Edit = QLineEdit(rpinv[9])
                    q9Edit.setFixedWidth(160)
                    q9Edit.setAlignment(Qt.AlignRight)
                    q9Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q9Edit.setDisabled(True)
                    
                    #bookdate
                    q10Edit = QLineEdit(str(rpinv[8]))
                    q10Edit.setFixedWidth(100)
                    q10Edit.setAlignment(Qt.AlignRight)
                    q10Edit.setStyleSheet("QLineEdit {font-size: 10pt; font-family: Arial; color: black }")
                    q10Edit.setDisabled(True)
                    
                    self.cBoxpay = QCheckBox()
                    self.cBoxpay.setText('Paying')
                    self.cBoxpay.setFont(QFont("Arial", 10))
                    if rpinv[7]:
                        self.cBoxpay.setChecked(True)
                        self.cBoxpay.setText('Payment done')
                        self.cBoxpay.setDisabled(True)
                      
                    def cboxChanged():
                        self.cBoxpay.setCheckState(self.cBoxpay.checkState())
                    self.cBoxpay.stateChanged.connect(cboxChanged) 
                    
                    def invPay(self):
                        mtoday = str(datetime.datetime.now())[0:10]
                        if self.cBoxpay.checkState():
                            upd = update(invoices).where(invoices.c.invoiceID==paynr)\
                              .values(paydate = mtoday)
                            con.execute(upd)
                            message = 'Payment done!'
                            actionOK(message)
                            self.close()
                        else:
                            self.close()
          
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
       
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 3, 1 ,1, Qt.AlignRight)
                    
                    lbl1 = QLabel('Invoicenr')
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(q1Edit, 1, 1)
                    
                    lbl2 = QLabel('Barcode')
                    grid.addWidget(lbl2, 1, 2)
                    grid.addWidget(q2Edit, 1, 3)
                           
                    lbl3 = QLabel('Description')  
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(q3Edit, 2, 1, 1, 3) 
                                                         
                    lbl4 = QLabel('Deliveries')  
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(q4Edit, 3, 1)
                    
                    lbl11 = QLabel('Bookdate')
                    grid.addWidget(lbl11, 3, 2)
                    grid.addWidget(q10Edit, 3, 3)
 
                    lbl5 = QLabel('Item-price')  
                    grid.addWidget(lbl5, 4, 0)
                    grid.addWidget(q5Edit, 4, 1)
                     
                    lbl10 = QLabel('Item-unit')
                    grid.addWidget(lbl10, 4, 2)
                    grid.addWidget(q9Edit, 4, 3)
                    
                    lbl7 = QLabel('supplierID')  
                    grid.addWidget(lbl7, 5, 0)
                    grid.addWidget(q6Edit, 5, 1)
                                   
                    lbl8 = QLabel('Orderlinenr')  
                    grid.addWidget(lbl8, 5, 2)
                    grid.addWidget(q7Edit, 5, 3)
                    
                    lbl9 = QLabel('Paydate')
                    grid.addWidget(lbl9, 6, 0)
                    grid.addWidget(q8Edit, 6, 1)
                                     
                    lbl6 = QLabel('Orderline total    =  '+'{:12.2f}'.format(rpinv[3]*rpinv[4]))
                    grid.addWidget(lbl6, 7, 0, 1, 2)
                    
                    grid.addWidget(self.cBoxpay, 7, 2, 1, 2)
                      
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
            
                    applyBtn = QPushButton('Pay / Close')
                    applyBtn.clicked.connect(lambda: invPay(self))
            
                    grid.addWidget(applyBtn, 8, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(120)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 9, 0, 1, 4, Qt.AlignCenter)
                    
            mainWin = Window()
            mainWin.exec_() 
              
    win = tableView(data_list, header)
    win.exec_()
    
def supplierMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Supplier Submenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
 
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Suppliers new')
            self.k0Edit.addItem('Suppliers view / change')
            self.k0Edit.addItem('Invoices suppliers / paying')
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    newSupplier()
                elif mindex == 1:
                    requestSupplier()
                elif mindex == 2:
                    handleInvoices()
                    
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
    
def purchaseMenu():
    mtoday = str(datetime.datetime.now())[0:10]
    metadata = MetaData()
    purchase_orderlines = Table('purchase_orderlines', metadata,
        Column('orderlineID', Integer,primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('item_price', Float),
        Column('item_unit', String),
        Column('order_size', Float),
        Column('supplierID', Integer),
        Column('bookdate', String),
        Column('ordered', Float),
        Column('order_date', String),
        Column('delivery', Float),
        Column('delivery_date', String))
    suppliers = Table('suppliers', metadata,
        Column('supplierID', Integer, primary_key=True),
        Column('company_name', String))
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('item_stock', Float),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('supplierID', Integer))
    invoices = Table('invoices', metadata,
       Column('invoiceID', Integer, primary_key=True),
       Column('barcode', String),
       Column('description', String),
       Column('delivery', Float),
       Column('item_price', Float),
       Column('supplierID', Integer),
       Column('orderlineID', Integer),
       Column('paydate', String),
       Column('bookdate', String),
       Column('item_unit', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
    selsup = select([purchase_orderlines,suppliers]).where(suppliers.c.supplierID==\
       purchase_orderlines.c.supplierID).distinct(purchase_orderlines.c.supplierID)\
      .order_by(purchase_orderlines.c.supplierID)
    rpsup = con.execute(selsup)
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Orders / deliveries")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            self.msuppliernr = 0
            self.msupplier = ''
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
 
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(450)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Collecting purchases')
            self.k0Edit.addItem('Unknown supplier - ordering')
            self.k0Edit.addItem('Receiving / processing deliveries')
            for row in rpsup:
                if not row[11] and not row[9]:
                    self.k0Edit.addItem('Ordering suppliernr '+str(row[12])+'\u2003'+row[13])
            self.k0Edit.addItem('To order yet - view')
            self.k0Edit.addItem('Ordered - view')
            self.k0Edit.addItem('All orders - view')
            self.k0Edit.addItem('Delivered orders - view')
            
            def k0Changed():
                self.k0Edit.setCurrentText(self.k0Edit.currentText())
            self.k0Edit.currentTextChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
             
            def menuChoice():
                mconnect = 0
                if self.k0Edit.currentText().startswith('Collecting'):
                    purchaseCollect(self)
                if self.k0Edit.currentText().startswith('Unknown'): 
                    sel = select([purchase_orderlines])\
                       .where(purchase_orderlines.c.supplierID==0)
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines])\
                            .where(purchase_orderlines.c.supplierID==0)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return
                    mconnect = 2
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Receiving'):
                    sel = select([purchase_orderlines,suppliers])\
                      .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                      purchase_orderlines.c.order_date != ''))
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers])\
                          .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                          purchase_orderlines.c.order_date != '')).order_by(suppliers.c.company_name)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return 
                    mconnect = 3
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Ordering'):
                    mpos = self.k0Edit.currentText().find('\u2003')
                    self.msuppliernr = int(self.k0Edit.currentText()[20:mpos])
                    self.msupplier = self.k0Edit.currentText()[mpos+1:]
                    sel = select([purchase_orderlines,suppliers])\
                        .where(and_(purchase_orderlines.c.supplierID==self.msuppliernr,\
                        purchase_orderlines.c.order_date=='',suppliers.c.supplierID==\
                        purchase_orderlines.c.supplierID))
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers])\
                          .where(and_(purchase_orderlines.c.supplierID==self.msuppliernr,\
                           purchase_orderlines.c.order_date=='',suppliers.c.supplierID==\
                           purchase_orderlines.c.supplierID))
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                         
                    mconnect = 4
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('To'):
                    sel = select([purchase_orderlines])\
                     .where(purchase_orderlines.c.order_date == '')
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines])\
                          .where(purchase_orderlines.c.order_date == '').order_by(purchase_orderlines.c.supplierID)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return    
                    mconnect = 5
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Ordered'):
                    sel = select([purchase_orderlines,suppliers])\
                     .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                      purchase_orderlines.c.order_date != '')) 
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines,suppliers])\
                         .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                          purchase_orderlines.c.order_date != '')).order_by(suppliers.c.company_name)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                        
                    mconnect = 6
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('All'):
                    sel = select([purchase_orderlines])
                    if con.execute(sel).fetchone():
                        selord = select([purchase_orderlines]).order_by(purchase_orderlines.c.supplierID)
                        rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                         
                    mconnect = 7
                    orderViews(self,rpord, mconnect)
                elif self.k0Edit.currentText().startswith('Delivered'):
                    sel = select([purchase_orderlines,suppliers])\
                     .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                      purchase_orderlines.c.delivery_date != ''))
                    if con.execute(sel).fetchone():
                         selord = select([purchase_orderlines,suppliers])\
                             .where(and_(purchase_orderlines.c.supplierID==suppliers.c.supplierID,\
                             purchase_orderlines.c.delivery_date != '')).order_by(suppliers.c.company_name)
                         rpord = con.execute(selord)
                    else:
                        message = 'No records found!'
                        alertText(message)
                        return                         
                    mconnect = 8
                    orderViews(self,rpord, mconnect)
                
            def orderViews(self,rpord, mconnect):
                msuppliernr = self.msuppliernr
                msupplier = self.msupplier
                class Widget(QDialog):
                    def __init__(self, data_list, header, *args):
                        QWidget.__init__(self, *args)
                        self.setWindowTitle('Ordering / deliveries')
                        self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                        self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinMaxButtonsHint)
                        self.setFont(QFont('Arial', 10))
                        
                        grid = QGridLayout()
                        grid.setSpacing(20)
                                                
                        table_model = MyTableModel(self, data_list, header)
                        table_view = QTableView()
                        table_view.setModel(table_model)
                        font = QFont("Arial", 10)
                        table_view.setFont(font)
                        table_view.resizeColumnsToContents()
                        table_view.setSelectionBehavior(QTableView.SelectRows)
                        table_view.resizeColumnsToContents()
                        table_view.setColumnWidth(6, 0)
                        table_view.clicked.connect(orderHandle)
                                      
                        grid.addWidget(table_view, 0, 0, 1, 6)
                        
                        def processOrders(self,rpord):
                            mtotal = 0
                            mpage = 0
                            rgl = 0
                            if sys.platform == 'win32':
                                fpurchase_order = '.\\forms\\Purchasing\\Purchase_Order_Supplier_'+str(msuppliernr)+'_'+mtoday+'.txt'
                            else:
                                fpurchase_order = './forms//Purchasing/Purchase_Order_Supplier_'+str(msuppliernr)+'_'+mtoday+'.txt'
                            def heading(self, mpage):
                                head=\
                            ('Purchase Order Supplier '+str(msuppliernr)+'  '+str(msupplier)+' Date : '+str(mtoday)+' Pagenumber '+str(mpage)+' \n'+
                            '==================================================================================================\n'+
                            'Order  Barcode       Description                      Number Unit               Price    Subtotal \n'+
                            '==================================================================================================\n')
                                return(head)
                            for row in rpord:
                                updline = update(purchase_orderlines)\
                                 .where(purchase_orderlines.c.orderlineID==row[0])\
                                 .values(ordered=row[5],order_date=mtoday)
                                con.execute(updline) 
                                morderline = row[0]
                                mbarcode = row[1]
                                mdescr = str(row[2])[0:30]
                                mprice = float(row[3])
                                munit = str(row[4])
                                mnumber = float(row[5])
                                mtotal += mprice*mnumber
                                rgl += 1
                                if rgl == 1:
                                    mpage += 1
                                    open(fpurchase_order, 'w').write(heading(self, mpage))
                                    rgl += 4
                                elif rgl%58 == 1:
                                    mpage += 1
                                    open(fpurchase_order, 'a').write(heading(self, mpage))
                                    rgl += 4
                                                                
                                open(fpurchase_order,'a').write('{:>6s}'.format(str(morderline))+' '+str(mbarcode)\
                                     +' '+'{:<30s}'.format(mdescr)+' '+'{:>8.2f}'.format(mnumber)\
                                     +' '+'{:<16s}'.format(munit)+'{:>8.2f}'.format(mprice)+'    '\
                                     +'{:>8.2f}'.format(mprice*mnumber)+'\n')
                                                                                                             
                            tail=\
                            ('===================================================================================================\n'+
                             'Total price orders                                                                   '+'{:>12.2f}'.format(mtotal)+'\n'+
                             '===================================================================================================\n')
                            if rgl > 0:
                                open(fpurchase_order,'a').write(tail) 
                                if sys.platform == 'win32':
                                    from os import startfile
                                    startfile(fpurchase_order, "print")
                                else:
                                    from os import system
                                    system("lpr "+fpurchase_order)
                                message ='Printing of purchase orders'
                                actionOK(message)
                            else:
                                message = 'No transactions for printing!'
                                alertText(message)
                    
                        if mconnect == 4:
                            printBtn = QPushButton('Process / Printing')
                            printBtn.clicked.connect(lambda: processOrders(self,rpord))
                            printBtn.setFont(QFont("Arial",10))
                            printBtn.setFixedWidth(180)
                            printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                            
                            grid.addWidget(printBtn, 1, 5, 1, 1, Qt.AlignRight)
                        
                        closeBtn = QPushButton('Close')
                        closeBtn.clicked.connect(self.close)  
                        closeBtn.setFont(QFont("Arial",10))
                        closeBtn.setFixedWidth(100)
                        closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                        
                        if mconnect == 4:
                           grid.addWidget(closeBtn, 1, 4, 1, 1, Qt.AlignRight)
                        else:
                           grid.addWidget(closeBtn, 1, 5, 1, 1, Qt.AlignRight)
                                                           
                        reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                        reglbl.setFont(QFont("Arial", 10))
                        grid.addWidget(reglbl, 2, 0, 1, 6, Qt.AlignCenter)
                        
                        self.setLayout(grid)
                        self.setGeometry(300, 100, 1500, 700)
                        self.setLayout(grid)
                
                class MyTableModel(QAbstractTableModel):
                    def __init__(self, parent, mylist, header, *args):
                        QAbstractTableModel.__init__(self, parent, *args)
                        self.mylist = mylist
                        self.header = header
                    def rowCount(self, parent):
                        return len(self.mylist)
                    def columnCount(self, parent):
                        return len(self.mylist[0])
                    def data(self, index, role):
                        veld = self.mylist[index.row()][index.column()]
                        if not index.isValid():
                            return None
                        elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                            return Qt.AlignRight | Qt.AlignVCenter
                        elif role != Qt.DisplayRole:
                            return None
                        if type(veld) == float:
                            return '{:12.2f}'.format(veld)
                        else:
                            return veld
                    def headerData(self, col, orientation, role):
                        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                            return self.header[col]
                        return None
                         
                header = ['Orderlinenr','Barcode','Description','Item-price','Item-unit',\
                          'Order-size','','Bookdate','Ordered','Order-date','Deliveries',\
                          'Delivery-date','Suppliernr','Company_name']
                if mconnect == 2 or mconnect == 5 or mconnect == 7:
                    del header[-2:]

                data_list=[]
                for row in rpord:
                    data_list += [(row)]
                     
                if mconnect == 4:
                    mpos = self.k0Edit.currentText().find('\u2003')
                    msuppliernr = int(self.k0Edit.currentText()[20:mpos])
                    selord = select([purchase_orderlines,suppliers])\
                        .where(and_(purchase_orderlines.c.supplierID==msuppliernr,\
                        purchase_orderlines.c.order_date=='',suppliers.c.supplierID==\
                        purchase_orderlines.c.supplierID))
                    rpord = con.execute(selord)
                                 
                def orderHandle(idx):
                    orderlinenr = idx.data()
                    if mconnect == 2:  #supplier unknown 
                        selorderline = select([purchase_orderlines])\
                         .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                          purchase_orderlines.c.supplierID==0))
                        rporderline = con.execute(selorderline).first()
                    elif mconnect == 3: #process deliveries
                        selorderline = select([purchase_orderlines, suppliers])\
                         .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                            purchase_orderlines.c.supplierID==suppliers.c.supplierID))\
                            .order_by(suppliers.c.company_name)
                        rporderline = con.execute(selorderline).first()
                    elif mconnect == 4 or mconnect == 8: #orders generated all suppliers per supplier
                        selorderline = select([purchase_orderlines, suppliers])\
                         .where(and_(purchase_orderlines.c.orderlineID==orderlinenr,\
                            purchase_orderlines.c.supplierID==suppliers.c.supplierID)).order_by(suppliers.c.company_name)
                        rporderline = con.execute(selorderline).first()
                    else:
                        selorderline = select([purchase_orderlines])\
                         .where(purchase_orderlines.c.orderlineID==orderlinenr)\
                            .order_by(purchase_orderlines.c.supplierID)
                        rporderline = con.execute(selorderline).first()
                                             
                    if idx.column()==0:
                        class MainWindow(QDialog):
                            def __init__(self):
                                QDialog.__init__(self)
                                self.setWindowTitle("Ordering / Deliveries")
                                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                                self.setStyleSheet("background-color: #D9E1DF")
                                self.setFont(QFont('Arial', 10)) 
                                
                                grid = QGridLayout()
                                grid.setSpacing(20)
                                
                                pyqt = QLabel()
                                movie = QMovie('./logos/pyqt.gif')
                                pyqt.setMovie(movie)
                                movie.setScaledSize(QSize(240,80))
                                movie.start()
                                grid.addWidget(pyqt, 0, 0, 1, 2)
                           
                                logo = QLabel()
                                pixmap = QPixmap('./logos/logo.jpg')
                                logo.setPixmap(pixmap.scaled(70,70))
                                grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
                                
                                #orderline
                                self.q1Edit = QLineEdit(str(rporderline[0]))
                                self.q1Edit.setFixedWidth(40)
                                self.q1Edit.setFont(QFont("Arial",10))
                                self.q1Edit.setStyleSheet('color: black; background-color: gainsboro')
                                self.q1Edit.setDisabled(True)
                                
                                #barcode
                                self.q2Edit = QLineEdit(rporderline[1])
                                self.q2Edit.setFixedWidth(130)
                                self.q2Edit.setFont(QFont("Arial", 10))
                                self.q2Edit.setStyleSheet('color: black')
                                self.q2Edit.setDisabled(True)    
                                
                                #description
                                self.q3Edit = QLineEdit(rporderline[2])
                                self.q3Edit.setFixedWidth(300)
                                self.q3Edit.setFont(QFont("Arial", 10))
                                self.q3Edit.setDisabled(True)
                                self.q3Edit.setStyleSheet('color: black')
                                
                                #item-price
                                self.q4Edit = QLineEdit(str(rporderline[3]))
                                self.q4Edit.setFixedWidth(100)
                                self.q4Edit.setFont(QFont("Arial", 10))
                                self.q4Edit.setDisabled(True)
                                self.q4Edit.setStyleSheet('color: black')
                                
                                #item-unit
                                self.q4aEdit = QLineEdit(rporderline[4])
                                self.q4aEdit.setFixedWidth(100)
                                self.q4aEdit.setFont(QFont("Arial", 10))
                                self.q4aEdit.setDisabled(True)
                                self.q4aEdit.setStyleSheet('color: black')
                                
                                #Order-size
                                self.q5Edit = QLineEdit(str(rporderline[5]))
                                self.q5Edit.setFixedWidth(100)
                                self.q5Edit.setFont(QFont("Arial", 10))
                                self.q5Edit.setDisabled(True)
                                self.q5Edit.setStyleSheet('color: black')
                                   
                                #Bookdate
                                self.q8Edit = QLineEdit(str(rporderline[7]))
                                self.q8Edit.setFixedWidth(100)
                                self.q8Edit.setFont(QFont("Arial", 10))
                                self.q8Edit.setDisabled(True)
                                self.q8Edit.setStyleSheet('color: black')
                                
                                #Ordered amount
                                self.q9Edit = QLineEdit(str(rporderline[8]))
                                self.q9Edit.setDisabled(True)
                                self.q9Edit.setStyleSheet('color: black')
                                self.q9Edit.setFixedWidth(50)
                                self.q9Edit.setFont(QFont("Arial", 10))
                                                                  
                                #Order_date
                                self.q10Edit = QLineEdit(rporderline[9])
                                self.q10Edit.setFixedWidth(100)
                                self.q10Edit.setFont(QFont("Arial", 10))
                                self.q10Edit.setDisabled(True)
                                self.q10Edit.setStyleSheet('color: black')
                                
                                #Deliveries
                                self.q11Edit = QLineEdit(str(rporderline[10]))
                                self.q11Edit.setFixedWidth(100)
                                self.q11Edit.setFont(QFont("Arial", 10))
                                self.q11Edit.setDisabled(True)
                                self.q11Edit.setStyleSheet('color: black')
                                if mconnect == 3:
                                    self.q11Edit.setEnabled(True)
                                    self.q11Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                                    def q11Changed():
                                        self.q11Edit.setText(self.q11Edit.text())
                                    self.q11Edit.textChanged.connect(q11Changed)
                                
                                #Delivery_date
                                self.q12Edit = QLineEdit(rporderline[11])
                                self.q12Edit.setFixedWidth(100)
                                self.q12Edit.setFont(QFont("Arial", 10))
                                self.q12Edit.setDisabled(True)
                                self.q12Edit.setStyleSheet('color: black')
                             
                                #Suppliernr
                                if mconnect == 2:
                                    self.q13Edit = QLineEdit('')
                                    def q13Changed():
                                       self.q13Edit.setText(self.q13Edit.text())
                                    self.q13Edit.textChanged.connect(q13Changed)
                                    self.q13Edit.setFixedWidth(100)
                                    self.q13Edit.setFont(QFont("Arial", 10))
                                    self.q13Edit.setStyleSheet('color: black ; background-color: #F8F7EE')
                                    reg_ex = QRegExp("^[0-9]{1,10}$")
                                    input_validator = QRegExpValidator(reg_ex, self.q13Edit)
                                    self.q13Edit.setValidator(input_validator)
                                else:
                                    self.q13Edit = QLineEdit(str(rporderline[6]))
                                    self.q13Edit.setDisabled(True)
                                    self.q13Edit.setFixedWidth(100)
                                    self.q13Edit.setFont(QFont("Arial", 10))
                                    self.q13Edit.setStyleSheet('color: black')
                                if not(mconnect == 2 or mconnect == 5 or mconnect == 7):  
                                    #Company-name
                                    self.q14Edit = QLineEdit(rporderline[13])
                                    self.q14Edit.setFixedWidth(300)
                                    self.q14Edit.setFont(QFont("Arial", 10))
                                    self.q14Edit.setDisabled(True)
                                    self.q14Edit.setStyleSheet('color: black') 
                                    
                                    lbl14 = QLabel('Company name')
                                    lbl14.setFont(QFont("Arial",10))
                                    grid.addWidget(lbl14, 8, 0)
                                    grid.addWidget(self.q14Edit, 8, 1, 1, 3)
                                                                     
                                lbl1 = QLabel('Orderlinenr')
                                lbl1.setFont(QFont("Arial",10))
                                grid.addWidget(lbl1, 1, 0)
                                grid.addWidget(self.q1Edit, 1, 1)
                                
                                lbl2 = QLabel('Barcode')
                                lbl2.setFont(QFont("Arial",10))
                                grid.addWidget(lbl2, 1, 2)
                                grid.addWidget(self.q2Edit, 1, 3)
                                
                                lbl3 = QLabel('Description')
                                lbl3.setFont(QFont("Arial",10))
                                grid.addWidget(lbl3, 2, 0)
                                grid.addWidget(self.q3Edit, 2, 1, 1, 3)
                                    
                                lbl4 = QLabel('Item-price') 
                                lbl4.setFont(QFont("Arial",10))
                                grid.addWidget(lbl4, 3, 0)
                                grid.addWidget(self.q4Edit, 3, 1)
                                
                                lbl4a = QLabel('Item-unit') 
                                lbl4a.setFont(QFont("Arial",10))
                                grid.addWidget(lbl4a, 3, 2)
                                grid.addWidget(self.q4aEdit, 3, 3)
                                                                                            
                                lbl5 = QLabel('Order-size') 
                                lbl5.setFont(QFont("Arial",10))
                                grid.addWidget(lbl5, 4, 0)
                                grid.addWidget(self.q5Edit, 4, 1)
                                                                
                                lbl8 = QLabel('Booking date')
                                lbl8.setFont(QFont("Arial",10))
                                grid.addWidget(lbl8, 5, 0)
                                grid.addWidget(self.q8Edit, 5, 1)
                                
                                lbl9 = QLabel('Ordering amount')
                                lbl9.setFont(QFont("Arial",10))
                                grid.addWidget(lbl9, 5, 2)
                                grid.addWidget(self.q9Edit, 5, 3)
                                
                                lbl10 = QLabel('Order date')
                                lbl10.setFont(QFont("Arial",10))
                                grid.addWidget(lbl10, 6, 0)
                                grid.addWidget(self.q10Edit, 6, 1)
                                
                                lbl11 = QLabel('Delivered amount')
                                lbl11.setFont(QFont("Arial",10))
                                grid.addWidget(lbl11, 6, 2)
                                grid.addWidget(self.q11Edit, 6, 3)
                                
                                lbl12 = QLabel('Delivery date')
                                lbl12.setFont(QFont("Arial",10))
                                grid.addWidget(lbl12, 7, 0)
                                grid.addWidget(self.q12Edit, 7, 1)
                                
                                lbl13 = QLabel('Suppliernumber')
                                lbl13.setFont(QFont("Arial",10))
                                grid.addWidget(lbl13, 7, 2)
                                grid.addWidget(self.q13Edit, 7, 3)
                                
                                self.setLayout(grid)
                                self.setGeometry(900, 200, 150, 150)
 
                                def saveHandled(self):
                                    mnumber=float(self.q9Edit.text())
                                    mtoday = str(datetime.datetime.now())[0:10]
                                    if mconnect == 2:
                                        if not self.q13Edit.text():
                                            return
                                        msuppliernr=int(self.q13Edit.text())
                                        sel = select([suppliers]).where(suppliers.c.supplierID ==msuppliernr)
                                        rp = con.execute(sel).first()
                                        if not rp:
                                            message = 'SupplierID does not exist!'
                                            alertText(message)
                                            return
                                        msupplier = rp[1]
                                        upd = update(purchase_orderlines)\
                                          .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                          .values(supplierID=msuppliernr,order_date=mtoday)
                                        con.execute(upd)
                                        updart = update(articles).where(articles.c.barcode==rporderline[1])\
                                           .values(supplierID=msuppliernr)
                                        con.execute(updart)
                                        mpage = 0
                                        rgl = 0
                                        if sys.platform == 'win32':
                                            fpurchase_order = '.\\forms\\Purchasing\\Purchase_Order_Supplier_Supplier_'+str(msuppliernr)+'_'+mtoday+'.txt'
                                        else:
                                            fpurchase_order = './forms//Purchasing/Purchase_Order_Supplier_Supplier_'+str(msuppliernr)+'_'+mtoday+'.txt'
                                        def heading(self, mpage):
                                            head=\
                                        ('Purchase Order Supplier '+str(msuppliernr)+'  '+str(msupplier)+' Date : '+str(mtoday)+' Pagenumber '+str(mpage)+' \n'+
                                        '==================================================================================================\n'+
                                        'Order  Barcode       Description                      Number Unit               Price    Subtotal \n'+
                                        '==================================================================================================\n')
                                            return(head)
                                        updline = update(purchase_orderlines)\
                                            .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                             .values(ordered=row[5],order_date=mtoday)
                                        con.execute(updline) 
                                        morderline = rporderline[0]
                                        mbarcode = rporderline[1]
                                        mdescr = str(rporderline[2])[0:30]
                                        mprice = float(rporderline[3])
                                        munit = str(rporderline[4])
                                        mnumber = float(rporderline[5])
                                        mtotal = mprice*mnumber
                                        rgl += 1
                                        if rgl == 1:
                                            mpage += 1
                                            open(fpurchase_order, 'w').write(heading(self, mpage))
                                            rgl += 4
                                                                                          
                                        open(fpurchase_order,'a').write('{:>6s}'.format(str(morderline))+' '+str(mbarcode)\
                                             +' '+'{:<30s}'.format(mdescr)+' '+'{:>8.2f}'.format(mnumber)\
                                             +' '+'{:<16s}'.format(munit)+'{:>8.2f}'.format(mprice)+'    '\
                                             +'{:>8.2f}'.format(mprice*mnumber)+'\n')
                                                                                                                     
                                        tail=\
                                        ('===================================================================================================\n'+
                                         'Total price orders                                                                   '+'{:>12.2f}'.format(mtotal)+'\n'+
                                         '===================================================================================================\n')
                                        open(fpurchase_order,'a').write(tail) 
                                        if sys.platform == 'win32':
                                            from os import startfile
                                            startfile(fpurchase_order, "print")
                                        else:
                                            from os import system
                                            system("lpr "+fpurchase_order)
                                        message ='Update Ok - Printing of purchase order!'
                                        actionOK(message)
                                        self.close()
                                    elif mconnect == 3:
                                        if self.q11Edit.text() == '0.0':
                                            return
                                        mdelivered = float(self.q11Edit.text())
                                        upd = update(purchase_orderlines)\
                                          .where(purchase_orderlines.c.orderlineID==rporderline[0])\
                                          .values(delivery=mdelivered,delivery_date=mtoday)
                                        con.execute(upd)
                                        updart = update(articles).where(articles.c.barcode == rporderline[1])\
                                          .values(item_stock = articles.c.item_stock+mdelivered,\
                                          order_balance=articles.c.order_balance-mdelivered,\
                                          order_status=True)
                                        con.execute(updart)
                                        try:
                                            paynr = (con.execute(select([func.max(invoices.c.invoiceID, type_=Integer)])).scalar())
                                            paynr += 1
                                        except:
                                            paynr = 1
                                        inspay = insert(invoices).values(invoiceID=paynr,\
                                           barcode=rporderline[1],supplierID=rporderline[6],\
                                           description=rporderline[2],item_price=rporderline[3],\
                                           delivery=rporderline[10],bookdate=rporderline[11],\
                                           orderlineID=rporderline[0],item_unit=rporderline[4])
                                        con.execute(inspay)
                                        message = 'Updates and invoice booking succeeded!'
                                        actionOK(message)
                                        self.close()
              
                                if mconnect == 3:
                                    applyBtn = QPushButton('Processing')
                                    applyBtn.clicked.connect(lambda: saveHandled(self))
                                    applyBtn.setFont(QFont("Arial",10))
                                    applyBtn.setFixedWidth(180)
                                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                    grid.addWidget(applyBtn, 10, 3, 1, 1, Qt.AlignRight)
                                elif mconnect < 3:
                                    applyBtn = QPushButton('Process - Printing')
                                    applyBtn.clicked.connect(lambda: saveHandled(self))
                                    applyBtn.setFont(QFont("Arial",10))
                                    applyBtn.setFixedWidth(180)
                                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                    grid.addWidget(applyBtn, 10, 3, 1, 1, Qt.AlignRight)
                                    
                                cancelBtn = QPushButton('Close')
                                cancelBtn.clicked.connect(self.close)
                                cancelBtn.setFont(QFont("Arial",10))
                                cancelBtn.setFixedWidth(100)
                                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                if mconnect < 4:
                                    grid.addWidget(cancelBtn, 10, 2, 1, 1, Qt.AlignRight)
                                else:
                                    grid.addWidget(cancelBtn, 10, 3, 1, 1, Qt.AlignRight)  
  
                                reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                                reglbl.setFont(QFont("Arial",10))                               
                                grid.addWidget(reglbl, 11, 0, 1, 4, Qt.AlignCenter)   
                                                    
                        window = MainWindow()
                        window.exec_()
 
                win = Widget(data_list, header)
                win.exec_()  
             
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice())
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
        
def paramChange():
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setWindowTitle('Parameters requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                    Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setColumnHidden(2, True)
            table_view.setColumnHidden(3, True)
            table_view.setColumnHidden(4, True)
            table_view.setColumnHidden(5, True)
            table_view.setColumnHidden(6, True)
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0)
                       
            reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            reglbl.setFont(QFont("Arial", 10))
            grid.addWidget(reglbl, 1, 0)
            
            self.setLayout(grid)
            self.setGeometry(900, 50, 300, 700)
            self.setLayout(grid)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['ParamID', 'Item', 'Value', 'Button-Text', 'Foregroundcolor','Backgroundcolor']
    
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('value', Float),
        Column('buttongroup', String),
        Column('fg_color', String),
        Column('bg_color', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
        
    sel = select([params]).where(params.c.paramID != 16).order_by(params.c.paramID)
    
    rp = con.execute(sel)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        paramnr = idx.data()
        if idx.column() == 0: 
            selpar = select([params]).where(params.c.paramID==paramnr)
            rppar = con.execute(selpar).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Parameters changing")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setStyleSheet("background-color: #D9E1DF")
                    self.setFont(QFont('Arial', 10))  
                    
                    #item
                    self.q1Edit = QLineEdit(rppar[1])
                    self.q1Edit.setCursorPosition(0)
                    self.q1Edit.setFixedWidth(220)
                    self.q1Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q1Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{0,20}$")
                    input_validator = QRegExpValidator(reg_ex, self.q1Edit)
                    self.q1Edit.setValidator(input_validator)
                                    
                    #value
                    self.q2Edit = QLineEdit(str(round(float(rppar[2]),2)))
                    self.q2Edit.setFixedWidth(100)
                    self.q2Edit.setAlignment(Qt.AlignRight)
                    if rppar[0] == 3 or rppar[0] == 4:
                        self.q2Edit.setDisabled(True)
                        self.q2Edit.setStyleSheet('color: black')
                    else:
                        self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #buttongroup
                    self.q3Edit = QPlainTextEdit(rppar[3])
                    self.q3Edit.setFixedSize(110,65)
                    if rppar[0] < 8:
                        self.q3Edit.setHidden(True)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Arial",10))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                        
                    #foreground color
                    self.q4Edit = QLineEdit(str(rppar[4]))
                    self.q4Edit.setFixedWidth(80)
                    if rppar[0] < 8:
                        self.q4Edit.setHidden(True)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q4Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[#]{1}[a-fA-F0-9]{6}$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                    
                    #background color
                    self.q5Edit = QLineEdit(str(rppar[5]))
                    self.q5Edit.setFixedWidth(80)
                    if rppar[0] < 8:
                        self.q5Edit.setHidden(True)
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q5Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[#]{1}[a-fA-F0-9]{6}$")
                    input_validator = QRegExpValidator(reg_ex, self.q5Edit)
                    self.q5Edit.setValidator(input_validator)
                    
                    def q1Changed():
                        self.q1Edit.setText(self.q1Edit.text())
                    self.q1Edit.textChanged.connect(q1Changed)
                    
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                    
                    def q5Changed():
                        self.q5Edit.setText(self.q5Edit.text())
                    self.q5Edit.textChanged.connect(q5Changed)
                                     
                    def updparams(self):
                         mitem = self.q1Edit.text()   
                         mvalue = self.q2Edit.text()
                         mbuttontext = self.q3Edit.toPlainText()
                         mfgcolor = self.q4Edit.text()
                         mbgcolor = self.q5Edit.text()
                         mlist = mbuttontext.split('\n')
                         for line in mlist:
                             if len(line) > 10:
                                 message = 'No more then 10 characters per line allowed'
                                 alertText(message)
                                 break
                             elif len(mlist) > 3:
                                 message= 'No more then 3 lines allowed'
                                 alertText(message)
                                 break
                         else:
                             updpar = update(params).where(params.c.paramID == paramnr).\
                               values(item = mitem, value = float(mvalue),\
                               buttongroup = mbuttontext,fg_color=mfgcolor,bg_color=mbgcolor)
                             con.execute(updpar)
                             message = 'Update succeeded!'
                             actionOK(message)
                             self.close()
                                                      
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Parameter')
                    lbl1.setFont(QFont("Arial",10))
                    grid.addWidget(lbl1, 1, 0)
                    lbl2 = QLabel(str(paramnr))
                    lbl2.setFont(QFont("Arial",10))
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Item') 
                    lbl3.setFont(QFont("Arial",10))
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(self.q1Edit, 2, 1, 1, 2) 
                                                         
                    lbl4 = QLabel('Value') 
                    lbl4.setFont(QFont("Arial",10))
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(self.q2Edit, 3, 1)
                    
                    lbl5 = QLabel('Buttongroup-text')
                    lbl5.setFont(QFont("Arial",10))
                    if rppar[0] < 8:
                        lbl5.setHidden(True)
                    grid.addWidget(lbl5, 4, 0, 3, 1, Qt.AlignVCenter)
                    grid.addWidget(self.q3Edit, 4, 1, 3, 1)
                    
                    lbl6 = QLabel('Foreground color') 
                    lbl6.setFont(QFont("Arial",10))
                    if rppar[0] < 8:
                        lbl6.setHidden(True)
                    grid.addWidget(lbl6, 8, 0)
                    grid.addWidget(self.q4Edit, 8, 1)
                    
                    lbl7 = QLabel('Background Color') 
                    lbl7.setFont(QFont("Arial",10))
                    if rppar[0] < 8:
                        lbl7.setHidden(True)
                    grid.addWidget(lbl7, 9, 0)
                    grid.addWidget(self.q5Edit, 9, 1)
            
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 , 0 , 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
                    
                    reglbl = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    reglbl.setFont(QFont("Arial",10))                               
                    grid.addWidget(reglbl, 11, 0, 1, 3, Qt.AlignCenter)                  
                    
                    self.setLayout(grid)
                    self.setGeometry(900, 200, 150, 150)
            
                    applyBtn = QPushButton('Change')
                    applyBtn.clicked.connect(lambda: updparams(self))
            
                    grid.addWidget(applyBtn, 10, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
 
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
            
                    grid.addWidget(cancelBtn, 10, 1, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                      
            window = MainWindow()
            window.exec_()
            
    win = Widget(data_list, header)
    win.exec_()
    
def adminMenu():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Administrator Menu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
  
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(280)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE') 
            self.k0Edit.addItem('Accounts Submenu')
            self.k0Edit.addItem('Articles Submenu')
            self.k0Edit.addItem('Imports Submenu')
            self.k0Edit.addItem('Sales - View')
            self.k0Edit.addItem('Payments - View / Pay')
            self.k0Edit.addItem('Suppliers submenu')
            self.k0Edit.addItem('Purchases Submenu')
            self.k0Edit.addItem('Parameters - View / Change')
            self.k0Edit.addItem('Turnover Submenu')
            self.k0Edit.addItem('Reprint purchase orders')
            self.k0Edit.addItem('Reprint sales receipts')
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
            
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                
                if mindex == 0:
                    accountMenu()
                elif mindex == 1:
                    articleMenu()
                elif mindex == 2:
                    importMenu()
                elif mindex == 3:
                    salesRequest()
                elif mindex == 4:
                    paymentsRequest()
                elif mindex == 5:
                    supplierMenu()
                elif mindex == 6:
                    purchaseMenu()
                elif mindex == 7:
                    paramChange()
                elif mindex == 8:
                    turnoverMenu()
                elif mindex == 9:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Purchasing\\'
                    else:
                        path = './forms/Purchasing/'
                    reprintForms(path)
                elif mindex == 10:
                    if sys.platform == 'win32':
                        path = '.\\forms\\Sales\\'
                    else:
                        path = './forms/Sales/'
                    reprintForms(path)
 
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()  
    
def emplRequest():
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(500, 50, 600, 800)
            self.setWindowTitle('Accounts requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
            table_view.clicked.connect(changeAccounts)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
        
    metadata = MetaData()
    accounts = Table('accounts', metadata,
         Column('barcodeID', String, primary_key=True),
         Column('firstname', String),
         Column('lastname', String),
         Column('access', Integer),
         Column('callname', String))
        
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/cashregister')
    con = engine.connect()
        
    selacc = select([accounts]).order_by(accounts.c.lastname)
    rpacc = con.execute(selacc)
        
    header = ['AccountID','Firstname','Lastname','Acceslevel','Callname']                                       
        
    data_list=[]
    for row in rpacc:
        data_list += [(row)] 
        
    def changeAccounts(idx):
        emplnr = idx.data()
        selempl = select([accounts]).where(accounts.c.barcodeID == emplnr)
        rpempl = con.execute(selempl).first()
        if idx.column() == 0:
            class Window(QDialog):
                def __init__(self, parent=None):
                    super(Window, self).__init__(parent)
                    
                    self.setWindowTitle("Account changing")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF")  
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                   
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
                    
                    q1Edit = QLineEdit(emplnr)
                    q1Edit.setFixedWidth(100)
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.setStyleSheet("color: black")
                    q1Edit.setDisabled(True)
                                    
                    q2Edit = QLineEdit(rpempl[1])     #firstname
                    q2Edit.setFixedWidth(200)
                    q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, q2Edit)
                    q2Edit.setValidator(input_validator)
                     
                    q3Edit = QLineEdit(rpempl[2])   #lastname
                    q3Edit.setFixedWidth(200)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, q3Edit)
                    q3Edit.setValidator(input_validator)
                     
                    q4Edit = QLineEdit(rpempl[4])   #callname
                    q4Edit.setFixedWidth(200)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, q4Edit)
                    q4Edit.setValidator(input_validator)
                    
                    q5Edit = QLineEdit(str(rpempl[3]))   #access
                    q5Edit.setFixedWidth(30)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0123]{1}$")
                    input_validator = QRegExpValidator(reg_ex, q5Edit)
                    q5Edit.setValidator(input_validator)
                    
                    def q2Changed():
                        q2Edit.setText(q2Edit.text())
                    q2Edit.textChanged.connect(q2Changed)
                     
                    def q3Changed():
                        q3Edit.setText(q3Edit.text())
                    q3Edit.textChanged.connect(q3Changed)  
                    
                    def q4Changed():
                        q4Edit.setText(q4Edit.text())
                    q4Edit.textChanged.connect(q4Changed)  
                    
                    def q5Changed():
                        q5Edit.setText(q5Edit.text())
                    q5Edit.textChanged.connect(q5Changed)
        
                    lbl1 = QLabel('Accountbarcode')
                    lbl1.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl1, 4, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q1Edit, 4, 1)
                              
                    lbl2 = QLabel('First name')
                    lbl2.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl2, 5, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q2Edit, 5, 1)
                    
                    lbl3 = QLabel('Last name')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 6, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q3Edit, 6, 1)
                    
                    lbl4 = QLabel('Call name')
                    lbl4.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl4, 7, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q4Edit, 7, 1)
                    
                    lbl5 = QLabel('Access level')
                    lbl5.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl5, 8, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(q5Edit, 8, 1)
                    
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updateAcc())
                       
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(applyBtn,9, 2, 1 , 1, Qt.AlignRight)
                    
                    def prepareEan(self):
                        ean = barcode.get('ean8', str(emplnr[:8]), writer=ImageWriter()) # for barcode as png
                        self.mbarcode = ean.get_fullcode()
                        self.path = './Barcodes/Accounts/'
                        if rpempl:
                            if sys.platform == 'win32':
                                ean.save('.\\Barcodes\\Accounts\\'+emplnr)
                            else:
                                ean.save('./Barcodes/Accounts/'+emplnr)
                        x1 = 267.3
                        y1 = 213.1
                        printEan(self, x1 , y1)
                        
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
            
                    grid.addWidget(cancelBtn, 9, 1, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
                                        
                    printBtn = QPushButton('Print Barcode')
                    printBtn.clicked.connect(lambda: prepareEan(self))
                       
                    printBtn.setFont(QFont("Arial",10))
                    printBtn.setFixedWidth(120)
                    printBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(printBtn,9, 0, 1, 1, Qt.AlignRight)
                  
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 10, 0, 1, 3, Qt.AlignCenter)
                  
                    def updateAcc():
                        fname = q2Edit.text()
                        lname = q3Edit.text()
                        cname = q4Edit.text()
                        maccess = q5Edit.text()
                        updacc = update(accounts).where(accounts.c.barcodeID == emplnr).\
                        values(firstname = fname,lastname = lname, callname = cname,\
                               access = int(maccess))
                        con.execute(updacc)
                        message = 'Update succeeded!'
                        actionOK(message)
                        self.close()
                                          
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 100)
                    
            window = Window()
            window.exec_()
           
    win = Widget(data_list, header)
    win.exec_()

def importMenu():
    import csv
    msep = ','
    metadata=MetaData()
    articles = Table('articles', metadata,
       Column('barcode', String, primary_key=True),
       Column('description', String),
       Column('short_descr', String),
       Column('item_price', Float),
       Column('item_unit', String),
       Column('article_group', String),
       Column('thumbnail', String),
       Column('category', Integer),
       Column('VAT', String),
       Column('order_status', Boolean),
       Column('supplierID', Integer),
       Column('item_stock', Float),
       Column('order_balance', Float))
    purchase_orderlines = Table('purchase_orderlines', metadata,
       Column('orderlineID', Integer,primary_key=True),
       Column('barcode', String),
       Column('supplierID', Integer),
       Column('delivery', Float),
       Column('delivery_date', String))
    invoices = Table('invoices', metadata,
       Column('invoiceID', Integer, primary_key=True),
       Column('barcode', String),
       Column('description', String),
       Column('delivery', Float),
       Column('item_price', Float),
       Column('supplierID', Integer),
       Column('orderlineID', Integer),
       Column('paydate', String),
       Column('bookdate', String),
       Column('item_unit', String))
    loss = Table('loss', metadata,
       Column('lossID', Integer, primary_key=True),
       Column('barcode', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
         
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Importmenu")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(400)
            self.k0Edit.setFont(QFont("Arial",12))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Import new articles')
            self.k0Edit.addItem('Import price changes')
            self.k0Edit.addItem('Import expired articles')
            self.k0Edit.addItem('Import deliveries articles')
                                         
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mtoday = str(datetime.datetime.now())[0:10]
                home = os.path.expanduser("~")
                log = open(str(home)+'/sales_import.log', 'a+')
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    path = "./forms/Imports/New/"
                    newpath = "./forms/ImportsDone/New/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0] 
                                    mdescr = line[1] 
                                    mshort = line[2]
                                    mprice =  float(line[3])
                                    munit = line[4]          
                                    mgroup = line[5]         
                                    mthumb = line[6]       
                                    mcat = line[7]    
                                    mvat = line[8]
                                    msupplier = int(line[9])
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    if con.execute(sel).fetchone():
                                        message = mtoday+' new items Barcode '+mbarcode+' exists!\n'
                                        log = open(str(home)+'/sales_import.log', 'a')
                                        log.write(message)
                                        continue
                                    elif not checkEan13(mbarcode):
                                        message = mtoday+' new items Barcode '+mbarcode+' is invalid!\n'
                                        log = open(str(home)+'/sales_import.log', 'a')
                                        log.write(message)
                                        continue
                                    else:
                                        insart = insert(articles).values(barcode=mbarcode,\
                                         description=mdescr,short_descr=mshort,\
                                         item_price=mprice,item_unit=munit,\
                                         article_group=mgroup,thumbnail=mthumb,\
                                         category=mcat,VAT=mvat,supplierID=msupplier)
                                        con.execute(insart)
                                        ean = barcode.get('ean13',mbarcode, writer=ImageWriter())
                                        if sys.platform == 'win32':
                                            ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                                        else:
                                            ean.save('./Barcodes/Articles/'+str(mbarcode))
                            message = 'Import done!'                
                            actionOK(message)
                            filename.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message)   
                elif mindex == 1:
                    path = "./forms/Imports/Prices/"
                    newpath = "./forms/ImportsDone/Prices/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0] 
                                    mprice =  float(line[1])
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    if con.execute(sel).fetchone():                    
                                        updart = update(articles).where(articles.c.barcode == mbarcode)\
                                          .values(item_price=mprice)
                                        con.execute(updart)
                                    else:
                                        message = mtoday+' Article price changes Barcode '+mbarcode+' not found!\n'
                                        log = open(str(home)+'/sales_import.log', 'a')
                                        log.write(message)
                                        continue
                            message = 'Import done!'
                            actionOK(message)
                            filename.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message)     
                elif mindex == 2:
                    path = "./forms/Imports/Expired/"
                    newpath = "./forms/ImportsDone/Expired/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0] 
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    rp = con.execute(sel).first()
                                    if rp:
                                        try:
                                            lossnr = con.execute(select([func.max(loss.c.lossID, type_=Integer)])).scalar()
                                            lossnr += 1
                                        except:
                                            lossnr = 1
                                        insloss = insert(loss).values(lossID=lossnr,barcode=rp[0],number=rp[11],\
                                          item_price=rp[3],category='Obsolete',bookdate=mtoday)
                                        con.execute(insloss)
                                        delart = delete(articles).where(articles.c.barcode == mbarcode)
                                        con.execute(delart)
                                    else:
                                        message = mtoday+' Article expired items Barcode '+mbarcode+' not found!\n'
                                        log = open(str(home)+'/sales_import.log', 'a')
                                        log.write(message)
                                        continue
                            message = 'Import done!'
                            actionOK(message)
                            filename.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message)   
                elif mindex == 3:
                    path = "./forms/Imports/Deliveries/"
                    newpath = "./forms/ImportsDone/Deliveries/"
                    x = 0
                    for file in os.listdir(path):
                        filename = open(path+file,'r')
                        with filename:
                            reader = csv.reader(filename, delimiter=msep)
                            for line in reader:
                                if line[0].isnumeric():
                                    mbarcode = line[0]
                                    selart = select([articles]).where(articles.c.barcode==mbarcode)
                                    rpart = con.execute(selart).first()
                                    if not rpart:
                                        message = mtoday+' Delivery items: Barcode '+mbarcode+' not found!\n'
                                        log = open(str(home)+'/sales_import.log', 'a')
                                        log.write(message)
                                        continue
                                    mdescription = rpart[1]
                                    mprice = rpart[3]
                                    msupplier = rpart[10]
                                    mdelivery = float(line[1])
                                    sel = select([articles]).where(articles.c.barcode == mbarcode)
                                    if con.execute(sel).fetchone():
                                        selord = select([purchase_orderlines]).where(purchase_orderlines\
                                          .c.barcode==mbarcode)
                                        if not con.execute(selord).fetchone():
                                            message = 'Collect purchases in menu "Purchasing" first!'
                                            alertText(message)
                                            return
                                        updart = update(articles).where(articles.c.barcode == mbarcode)\
                                         .values(item_stock=articles.c.item_stock+float(line[1]),order_status=True,\
                                           order_balance = articles.c.order_balance-float(line[1]))
                                        con.execute(updart)
                                        updord = update(purchase_orderlines).where(purchase_orderlines\
                                          .c.barcode==mbarcode).values(delivery=mdelivery,delivery_date=mtoday)
                                        con.execute(updord)
                                        try:
                                            paynr = (con.execute(select([func.max(invoices.c.invoiceID, type_=Integer)])).scalar())
                                            paynr += 1
                                        except:
                                            paynr = 1
                                        inspay = insert(invoices).values(invoiceID=paynr,\
                                           barcode=mbarcode,supplierID=msupplier,\
                                           description=mdescription,item_price=mprice,\
                                           delivery=mdelivery,bookdate=mtoday,\
                                           orderlineID=int(line[2]))
                                        con.execute(inspay)
                            message = 'Import done!'
                            actionOK(message)
                            filename.close()
                            log.close()
                            shutil.move(path+file,newpath+file)
                        x += 1
                    if x == 0:
                        message = 'No imports available!'
                        actionOK(message) 
                        
            lbllog = QLabel('View sales_import.log in your home folder!')  
            lbllog.setFont(QFont("Arial", 10))
            grid.addWidget(lbllog, 2, 0, 1, 3, Qt.AlignCenter)
                        
            applyBtn = QPushButton('Import')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 3, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 3, 1, 1, 1, Qt.AlignRight)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 4, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(900, 200, 150, 100)
                
    window = Widget()
    window.exec_()
   
def calculationStock():
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('value', Float))
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('category', Integer),
        Column('annual_consumption_1', Float),
        Column('annual_consumption_2', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
           
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    myear = int(str(datetime.date.today())[0:4])
    if myear%2 == 1 and int(rppar[3][2]) == 0:
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
        updpar = update(params).where(params.c.paramID == 4).values(value = 1)
        con.execute(updpar)
                     
        for row in rparticles:
            mordersize = round(sqrt(2*row[5]*rppar[4][2])/(row[1]*rppar[5][2]),0)
            mjrverbr = row[4]
            if row[3] == 1:
                minstock = round(mjrverbr*1/104, 0) # < 3 days deliverytime
            elif row[3] == 2:
                minstock = round(mjrverbr*1/52, 0) # < 1 week deliverytime
            elif row[3] == 3:
                minstock = round(mjrverbr*1/26, 0) # < 2 weeks deliverytime
            elif row[3] == 4:
                minstock = round(mjrverbr*1/17, 0) # < 3 weeks deliverytime
            elif row[3] == 5:
                minstock = round(mjrverbr*2/17, 0) # < 6 weeks deliverytime
            elif row[3] == 6:
                minstock = round(mjrverbr*4/17, 0) # < 12 weeks deliverytime
            elif row[3] == 7: 
                minstock = round(mjrverbr*8/17, 0) # < 26 weeks deliverytime
            elif row[3] == 8: 
                minstock = round(mjrverbr*16/17,0) # < 52 weeks deliverytime
                
            updart = update(articles).where(articles.c.barcode == row[0]).\
                values(annual_consumption_2 = 0, minimum_stock = minstock, order_size = mordersize)
            con.execute(updart)
    elif myear%2 == 0 and int(rppar[3][2]) == 1:
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
        updpar = update(params).where(params.c.paramID == 4).values(value = 0)
        con.execute(updpar)
                   
        for row in rparticles:
            mordersize = round(sqrt(2*row[5]*rppar[4][2])/(row[1]*rppar[5][2]),0)
            mjrverbr = row[5]
            if row[3] == 1:
                minstock = round(mjrverbr*1/104, 0) # < 3 days deliverytime
            elif row[3] == 2:
                minstock = round(mjrverbr*1/52, 0) # < 1 week deliverytime
            elif row[3] == 3:
                minstock = round(mjrverbr*1/26, 0) # < 2 weeks deliverytime
            elif row[3] == 4:
                minstock = round(mjrverbr*1/17, 0) # < 3 weeks deliverytime
            elif row[3] == 5:
                minstock = round(mjrverbr*2/17, 0) # < 6 weeks deliverytime
            elif row[3] == 6:
                minstock = round(mjrverbr*4/17, 0) # < 12 weeks deliverytime
            elif row[3] == 7: 
                minstock = round(mjrverbr*8/17, 0) # < 26 weeks deliverytime
            elif row[3] == 8: 
                minstock = round(mjrverbr*16/17,0) # < 52 weeks deliverytime
                
            updart = update(articles).where(articles.c.barcode == row[0]).\
                values(annual_consumption_1 = 0, minimum_stock = minstock, order_size = mordersize)
            con.execute(updart)
  
def articleRequest(mflag, btn):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('short_descr', String),
        Column('item_price', Float),
        Column('selling_price', Float),
        Column('item_stock', Float),
        Column('item_unit', String),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('location_warehouse', String),
        Column('article_group', String),
        Column('thumbnail', String),
        Column('category', Integer),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('mutation_date', String),
        Column('annual_consumption_1', Float),
        Column('annual_consumption_2', Float),
        Column('VAT', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
     
    sel = select([articles])
    if con.execute(sel).fetchone():
        selarticles = select([articles]).order_by(articles.c.barcode)
        rparticles = con.execute(selarticles)
    else:
        message = "no records found!"
        alertText(message)
        return
             
    class Mainwindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Articles requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setItemDelegateForColumn(11, showImage(self))
            table_view.setColumnWidth(11, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            if mflag == 1:
                table_view.clicked.connect(defineButton)
            elif mflag == 2:
                table_view.clicked.connect(bookingLoss)
            else:
                table_view.clicked.connect(changeArticle)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
       
    class showImage(QStyledItemDelegate):  
           def __init__(self, parent):
               QStyledItemDelegate.__init__(self, parent)
           def paint(self, painter, option, index):        
                painter.fillRect(option.rect,QColor(255,255,255))
                image = QImage(index.data())
                pixmap = QPixmap(image)
                pixmap.scaled(256,256) 
                return(painter.drawPixmap(option.rect, pixmap))
                                       
    header = ['Barcode','Description', 'Short-description', 'Item-Price','Selling-Price',\
              'Item-Stock', 'Item-Unit','Mininum-Stock', 'Order-Size', 'Location',\
              'Article_Group', 'Thumbnail','Category', 'Order-Balance', 'Order-Status',\
              'Mutation-Date','Annual-Consumption_1','Annual-Consumption_2', 'VAT']    
        
    data_list=[]
    for row in rparticles:
        data_list += [(row)] 
    
    def defineButton(idx):
        mbarcode = idx.data()
        if idx.column() == 0:
            metadata = MetaData()
            buttons = Table('buttons', metadata,
                Column('buttonID', Integer, primary_key=True),
                Column('barcode', String),
                Column('buttontext', String),
                Column('fg_color', String),
                Column('bg_color', String))
            
            selbtn = select([buttons]).where(buttons.c.buttonID == btn)
            rpbtn = con.execute(selbtn).first()
                        
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    
                    self.setWindowTitle("Button Text")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF")  
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 1)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                    
                    #barcode
                    self.q1Edit = QLineEdit(str(mbarcode)) 
                    self.q1Edit.setFixedWidth(130)
                    self.q1Edit.setFont(QFont("Arial",10))
                    self.q1Edit.setStyleSheet("color: black")
                    self.q1Edit.setDisabled(True)
                    
                    #button-number
                    self.q2Edit = QLineEdit(btn)
                    self.q2Edit.setFixedWidth(40)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[1-9]{1}|[1-9]{1}[0-9]{1}|[1]{1}[0-9]{1}[0-9]{1}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #button-text
                    self.q3Edit = QPlainTextEdit(rpbtn[2])
                    self.q3Edit.setFixedSize(110,65)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Arial",10))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                        
                    #foreground color
                    self.q4Edit = QLineEdit(str(rpbtn[3]))
                    self.q4Edit.setFixedWidth(80)
                    self.q4Edit.setFont(QFont("Arial",10))
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[#]{1}[a-fA-F0-9]{6}$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                      
                    #background color
                    self.q5Edit = QLineEdit(str(rpbtn[4])) 
                    self.q5Edit.setFixedWidth(80)
                    self.q5Edit.setFont(QFont("Arial",10))
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[#]{1}[a-fA-F0-9]{6}$")
                    input_validator = QRegExpValidator(reg_ex, self.q5Edit)
                    self.q5Edit.setValidator(input_validator)
                                             
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)   
                    
                    def q5Changed():
                        self.q5Edit.setText(self.q5Edit.text())
                    self.q5Edit.textChanged.connect(q5Changed)    
                
                    lbl1 = QLabel('Barcodenummer')
                    lbl1.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl1, 1, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q1Edit, 1, 1)
                     
                    lbl2 = QLabel('Button-Number')
                    lbl2.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl2, 2, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q2Edit, 2, 1)
                    
                    lbl3 = QLabel('Button-Text')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 3, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    lbl4 = QLabel('Foreground color')
                    lbl4.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl4, 4, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q4Edit, 4, 1)
                    
                    lbl5 = QLabel('Background color')
                    lbl5.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl5, 5, 0, 1, 1, Qt.AlignRight)
                    grid.addWidget(self.q5Edit, 5, 1)
                                 
                    applyBtn = QPushButton('Insert')
                    applyBtn.clicked.connect(lambda: insBtnText())
                       
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(applyBtn, 6, 1 , 1, 1, Qt.AlignRight)
                        
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
                    grid.addWidget(cancelBtn, 6, 0, 1, 2, Qt.AlignCenter)
                    
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 7, 0, 1, 3, Qt.AlignCenter)
                   
                    def insBtnText():
                        mbtnnr = int(self.q2Edit.text())
                        mbtntext = self.q3Edit.toPlainText()
                        mlist = mbtntext.split('\n')
                        mfgcolor = self.q4Edit.text()
                        mbgcolor = self.q5Edit.text()
                        for line in mlist:
                             if len(line) > 10:
                                 message = 'No more then 10 characters per line allowed'
                                 alertText(message)
                                 break
                             elif len(mlist) > 3:
                                 message= 'No more then 3 lines allowed'
                                 alertText(message)
                                 break
                        else:
                            updbtn = update(buttons).where(buttons.c.buttonID==mbtnnr).\
                             values(barcode=str(mbarcode), buttontext=mbtntext,
                             fg_color=mfgcolor, bg_color=mbgcolor)
                            con.execute(updbtn)
                            message = 'Update succeeded!'
                            actionOK(message)
                            self.close()
                                            
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 100)
    
            window = Widget()
            window.exec_()
            
    def changeArticle(idx):
        mbarcode = idx.data() 
        selarticle = select([articles]).where(articles.c.barcode == mbarcode)
        rparticle = con.execute(selarticle).first()
        if idx.column() == 0:
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    
                    self.setWindowTitle("Article Change")
                    self.setWindowIcon(QIcon('./logos/logo.jpg'))
                    self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                    self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                           
                    self.setFont(QFont('Arial', 10))
                    self.setStyleSheet("background-color: #D9E1DF")  
            
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 3, 1 ,1, Qt.AlignRight)
                    
                    #barcode
                    self.q1Edit = QLineEdit(str(mbarcode)) 
                    self.q1Edit.setFixedWidth(130)
                    self.q1Edit.setFont(QFont("Arial",10))
                    self.q1Edit.setStyleSheet("color: black")
                    self.q1Edit.setDisabled(True)
        
                    #description
                    self.q2Edit = QLineEdit(rparticle[1])    
                    self.q2Edit.setFixedWidth(400)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,50}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #short-description
                    self.q2aEdit = QLineEdit(rparticle[2])    
                    self.q2aEdit.setFixedWidth(200)
                    self.q2aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2aEdit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{1,20}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2aEdit)
                    self.q2aEdit.setValidator(input_validator)
                    
                    #item_price
                    self.q3Edit = QLineEdit(str(round(rparticle[3],2)))
                    self.q3Edit.setAlignment(Qt.AlignRight)
                    self.q3Edit.setFixedWidth(100)
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q3Edit)
                    self.q3Edit.setValidator(input_validator)
                    
                    #selling-price
                    self.q3aEdit = QLineEdit(str(round(rparticle[4],2)))
                    self.q3aEdit.setAlignment(Qt.AlignRight)
                    self.q3aEdit.setFixedWidth(100)
                    self.q3aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q3aEdit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q3aEdit)
                    self.q3aEdit.setValidator(input_validator)
                    
                    #item_stock
                    self.q4Edit = QLineEdit(str(round(rparticle[5],2)))
                    self.q4Edit.setAlignment(Qt.AlignRight)
                    self.q4Edit.setFixedWidth(100)
                    self.q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q4Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q4Edit)
                    self.q4Edit.setValidator(input_validator)
                    
                    #item_unit
                    self.q5Edit = QComboBox()
                    self.q5Edit.setFixedWidth(170)
                    self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q5Edit.setFont(QFont("Arial",10))
                    self.q5Edit.addItem('stuk')
                    self.q5Edit.addItem('100')
                    self.q5Edit.addItem('meter')
                    self.q5Edit.addItem('kg')
                    self.q5Edit.addItem('liter')
                    self.q5Edit.addItem('m²')
                    self.q5Edit.addItem('m³')
                    self.q5Edit.setCurrentIndex(self.q5Edit.findText(rparticle[6]))
                    
                    #minimum stock
                    self.q6Edit = QLineEdit(str(round(rparticle[7],2)))
                    self.q6Edit.setAlignment(Qt.AlignRight)
                    self.q6Edit.setFixedWidth(100)
                    self.q6Edit.setFont(QFont("Arial",10))
                    self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q6Edit)
                    self.q6Edit.setValidator(input_validator)
        
                    #order_size
                    self.q7Edit = QLineEdit(str(round(rparticle[8],2)))
                    self.q7Edit.setAlignment(Qt.AlignRight)
                    self.q7Edit.setFixedWidth(100)
                    self.q7Edit.setFont(QFont("Arial",10))
                    self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q7Edit)
                    self.q7Edit.setValidator(input_validator)
                                 
                    #location
                    self.q8Edit = QLineEdit(rparticle[9])
                    self.q8Edit.setFixedWidth(100)
                    self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q8Edit.setFont(QFont("Arial",10))
                                
                    # article_group
                    self.q9Edit = QLineEdit(rparticle[10])
                    self.q9Edit.setFixedWidth(200)
                    self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q9Edit.setFont(QFont("Arial",10))
                        
                    #thumbnail
                    self.q10Edit = QLineEdit(rparticle[11])
                    self.q10Edit.setFixedWidth(200)
                    self.q10Edit.setFont(QFont("Arial",10))
                    self.q10Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                                
                    #category
                    self.q11Edit = QComboBox()
                    self.q11Edit.setFixedWidth(260)
                    self.q11Edit.setFont(QFont("Arial",10))
                    self.q11Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q11Edit.addItem('0. Daily fresh products.')
                    self.q11Edit.addItem('1. Stock-driven < 3 days.')
                    self.q11Edit.addItem('2. Stock-driven < 1 weeks.')
                    self.q11Edit.addItem('3. Stock-driven < 2 weeks.')
                    self.q11Edit.addItem('4. Stock-driven < 3 weeks.')
                    self.q11Edit.addItem('5. Stock-driven < 6 weken')
                    self.q11Edit.addItem('6. Stock-driven < 12 weeks')
                    self.q11Edit.addItem('7. Stock-driven < 26 weeks')
                    self.q11Edit.addItem('8. Stock-driven < 52 weeks')
                    self.q11Edit.setCurrentIndex(rparticle[13]-1)
         
                    #vat
                    self.q12Edit = QComboBox()
                    self.q12Edit.setFixedWidth(100)
                    self.q12Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q12Edit.setFont(QFont("Arial",10))
                    self.q12Edit.addItem('high')
                    self.q12Edit.addItem('low')
                    self.q12Edit.addItem('zero')
                    self.q12Edit.setCurrentIndex(self.q12Edit.findText(rparticle[18]))
                    
                    #order-balance
                    self.q13Edit = QLineEdit(str(round(rparticle[13],2)))
                    self.q13Edit.setFixedWidth(100)
                    self.q13Edit.setAlignment(Qt.AlignRight)
                    self.q13Edit.setStyleSheet('color: black')
                    self.q13Edit.setFont(QFont("Arial",10))
                    self.q13Edit.setDisabled(True)
                    
                    #order_status
                    self.q14Edit = QLineEdit(str(bool(rparticle[14])))
                    self.q14Edit.setFixedWidth(100)
                    self.q14Edit.setStyleSheet('color: black')
                    self.q14Edit.setFont(QFont("Arial",10))
                    self.q14Edit.setDisabled(True)
                   
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def q2aChanged():
                        self.q2aEdit.setText(self.q2aEdit.text())
                    self.q2aEdit.textChanged.connect(q2aChanged)
                    
                    def q3Changed():
                        self.q3Edit.setText(self.q3Edit.text())
                    self.q3Edit.textChanged.connect(q3Changed)
                    
                    def q3aChanged():
                        self.q3aEdit.setText(self.q3aEdit.text())
                    self.q3aEdit.textChanged.connect(q3aChanged)
                    
                    def q4Changed():
                        self.q4Edit.setText(self.q4Edit.text())
                    self.q4Edit.textChanged.connect(q4Changed)
                    
                    def q5Changed():
                        self.q5Edit.setCurrentText(self.q5Edit.currentText()) 
                    self.q5Edit.currentIndexChanged.connect(q5Changed)
                    
                    def q6Changed():
                        self.q6Edit.setText(self.q6Edit.text())
                    self.q6Edit.textChanged.connect(q6Changed)
                    
                    def q7Changed():
                        self.q7Edit.setText(self.q7Edit.text())
                    self.q7Edit.textChanged.connect(q7Changed)
                    
                    def q8Changed():
                        self.q8Edit.setText(self.q8Edit.text())
                    self.q8Edit.textChanged.connect(q8Changed)
                    
                    def q9Changed():
                        self.q9Edit.setText(self.q9Edit.text())
                    self.q9Edit.textChanged.connect(q9Changed)
                    
                    def q10Changed():
                        self.q10Edit.setText(self.q10Edit.text())
                    self.q10Edit.textChanged.connect(q10Changed)
                    
                    def q11Changed():
                        self.q11Edit.setCurrentIndex(self.q11Edit.currentIndex())
                    self.q11Edit.currentIndexChanged.connect(q11Changed)
                    
                    def q12Changed():
                        self.q5Edit.setCurrentText(self.q12Edit.currentText()) 
                    self.q12Edit.currentIndexChanged.connect(q12Changed)
                   
                    grid.addWidget(QLabel('Barcodenumber'), 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                    
                    grid.addWidget(QLabel('Description'), 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1 ,1 ,2)
                    
                    grid.addWidget(QLabel('Item_Price'), 3, 0)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    grid.addWidget(QLabel('Item-Unit'), 3, 2)
                    grid.addWidget(self.q5Edit, 3, 3)
                    
                    grid.addWidget(QLabel('Minimum_Stock'), 4, 0)
                    grid.addWidget(self.q6Edit, 4, 1)
                    
                    grid.addWidget(QLabel('Item-Stock'), 4, 2)
                    grid.addWidget(self.q4Edit, 4, 3)
                    
                    grid.addWidget(QLabel('Order-Size'), 5, 2)
                    grid.addWidget(self.q7Edit, 5, 3)
                      
                    grid.addWidget(QLabel('Location'), 5, 0)
                    grid.addWidget(self.q8Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Articlegroup'), 6, 2)
                    grid.addWidget(self.q9Edit, 6, 3)
                    
                    grid.addWidget(QLabel('Thumbnail'), 6, 0)
                    grid.addWidget(self.q10Edit, 6, 1)
                    
                    grid.addWidget(QLabel('Category'), 7, 2 )
                    grid.addWidget(self.q11Edit, 7, 3)
                    
                    grid.addWidget(QLabel('VAT'), 7, 0 )
                    grid.addWidget(self.q12Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Order_Balance'), 8, 0 )
                    grid.addWidget(self.q13Edit, 8, 1)
                    
                    grid.addWidget(QLabel('Order-Status'), 8, 2 )
                    grid.addWidget(self.q14Edit, 8, 3)  
                    
                    grid.addWidget(QLabel('Short-Descr'), 9, 0)
                    grid.addWidget(self.q2aEdit, 9, 1)
                    
                    grid.addWidget(QLabel('Selling_Price'), 9, 2)
                    grid.addWidget(self.q3aEdit, 9, 3)
          
                    def updArticle(self):
                        mdescr = self.q2Edit.text()
                        mshort = self.q2aEdit.text()
                        mprice = float(self.q3Edit.text())
                        msellprice = float(self.q3aEdit.text())
                        mstock = float(self.q4Edit.text())
                        munit = self.q5Edit.currentText()
                        mminstock = float(self.q6Edit.text())
                        morder_size = float(self.q7Edit.text())
                        mlocation = self.q8Edit.text()
                        martgroup = self.q9Edit.text()
                        mthumb = self.q10Edit.text()
                        mcategory = self.q11Edit.currentIndex()+1
                        mvat = self.q12Edit.currentText()
                        updarticle = update(articles).where(articles.c.barcode==mbarcode)\
                          .values(barcode=mbarcode,description=mdescr,short_descr = mshort,\
                            item_price=mprice,selling_price=msellprice,item_stock=mstock,\
                            item_unit=munit,minimum_stock=mminstock,order_size=morder_size,\
                            location_warehouse=mlocation,article_group=martgroup,\
                            thumbnail=mthumb,category=mcategory,VAT=mvat)
                        con.execute(updarticle)
                        message = 'Update succeeded!'
                        actionOK(message)
                        self.close()
                        
                    def prepareEan(self):
                        ean = barcode.get('ean13', str(mbarcode[:13]), writer=ImageWriter()) # for barcode as png
                        self.mbarcode = ean.get_fullcode()
                        self.path = '.\\Barcodes\\Articles\\'
                        if sys.platform == 'win32':
                            self.path = '.\\Barcodes\\Articles\\'
                            ean.save(self.path+self.mbarcode)
                        else:
                            self.path ='./Barcodes/Articles/'
                            ean.save(self.path+self.mbarcode)
                        x1 = 372.9
                        y1 = 228.5
                        printEan(self, x1 , y1)
                                 
                    applyBtn = QPushButton('Update')
                    applyBtn.clicked.connect(lambda: updArticle(self))
            
                    grid.addWidget(applyBtn, 10, 3, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
                    
                    grid.addWidget(cancelBtn, 10, 3)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                    printBtn = QPushButton('Print Barcode')
                    printBtn.clicked.connect(lambda: prepareEan(self))
                    
                    grid.addWidget(printBtn, 10, 2)
                    printBtn.setFont(QFont("Arial",10))
                    printBtn.setFixedWidth(120)
                    printBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 11, 0, 1, 4, Qt.AlignCenter)
             
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 150, 100)
         
            window = Widget()
            window.exec_()
            
    def bookingLoss(idx):
        mbarcode = idx.data()
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
                self.setWindowTitle("Booking loss articles")
                self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                        Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                self.setFont(QFont('Arial', 10))
                
                q1Edit = QLineEdit(mbarcode)
                q1Edit.setFixedWidth(130)
                q1Edit.setFont(QFont("Arial", 10))
                q1Edit.setStyleSheet("color: black")
                q1Edit.setDisabled(True)
                                
                #Loss description
                qloss = QComboBox()
                qloss.setFixedWidth(230)
                qloss.setFont(QFont("Arial", 10))
                qloss.setStyleSheet("color: black;  background-color: #F8F7EE")
                qloss.addItem('Obsolete')
                qloss.addItem('Warehouse differences.')
                qloss.addItem('Damaged')
                qloss.addItem('Shelf Life')
                       
                #number
                qnumber = QLineEdit('0')
                qnumber.setFixedWidth(150)
                qnumber.setFont(QFont("Arial",10))
                qnumber.setStyleSheet("color: black;  background-color: #F8F7EE")
                reg_ex = QRegExp("^[+]?[0-9]*\.?[0-9]+$")
                input_validator = QRegExpValidator(reg_ex, qnumber)
                qnumber.setValidator(input_validator)
                
                grid = QGridLayout()
                grid.setSpacing(20)
                              
                pyqt = QLabel()
                movie = QMovie('./logos/pyqt.gif')
                pyqt.setMovie(movie)
                movie.setScaledSize(QSize(240,80))
                movie.start()
                grid.addWidget(pyqt, 0 ,0, 1, 2)
           
                logo = QLabel()
                pixmap = QPixmap('./logos/logo.jpg')
                logo.setPixmap(pixmap.scaled(70,70))
                grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                
                lbl1 = QLabel('Barcodenumber')  
                lbl1.setFont(QFont("Arial",10))
                grid.addWidget(lbl1, 1, 0)
                grid.addWidget(q1Edit, 1, 1)
                
                lbl2 = QLabel('Loss description')  
                lbl2.setFont(QFont("Arial",10))
                grid.addWidget(lbl2, 2, 0)
                grid.addWidget(qloss, 2, 1)
                        
                lbl3 = QLabel('Number')  
                lbl3.setFont(QFont("Arial",10))
                grid.addWidget(lbl3, 3, 0)
                grid.addWidget(qnumber, 3, 1)
                       
                def qlossChanged():
                    qloss.setCurrentText(qloss.currentText())
                qloss.currentIndexChanged.connect(qlossChanged)
                
                def qnumberChanged():
                    qnumber.setText(qnumber.text())
                qnumber.textChanged.connect(qnumberChanged)
                
                def insertLoss():
                    metadata = MetaData()
                    loss = Table('loss', metadata,
                       Column('lossID', Integer, primary_key=True),
                       Column('barcode', None, ForeignKey('articles.barcode')),
                       Column('number', Float),
                       Column('bookdate', String),
                       Column('category', String))
                    
                    mdescr = qloss.currentText()
                    mnumber = qnumber.text()
                    try:
                        lossnr = con.execute(select([func.max(loss.c.lossID, type_=Integer)])).scalar()
                        lossnr += 1
                    except:
                        lossnr = 1
                    mbookdate= str(datetime.datetime.now())[0:10]
                    if float(mnumber) > 0:                 
                        ins = insert(loss).values(lossID = lossnr, barcode = mbarcode,\
                            number = mnumber, category = mdescr, bookdate = mbookdate)
                        con.execute(ins)
                        upd = update(articles).where(articles.c.barcode == mbarcode).\
                          values(item_stock = articles.c.item_stock - mnumber)
                        con.execute(upd)
                        message = 'Update succeeded!'
                        actionOK(message)
                        self.close()
                    else:
                        message = 'Not all fields are filled in!'
                        alertText(message)
                        self.close()
                                                 
                self.setLayout(grid)
                self.setGeometry(600, 200, 150, 150)
        
                applyBtn = QPushButton('Change')
                applyBtn.clicked.connect(lambda: insertLoss())
        
                grid.addWidget(applyBtn, 4, 1, 1, 1, Qt.AlignRight)
                applyBtn.setFont(QFont("Arial",10))
                applyBtn.setFixedWidth(100)
                applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
               
                cancelBtn = QPushButton('Close')
                cancelBtn.clicked.connect(self.close) 
                
                grid.addWidget(cancelBtn, 4, 1)
                cancelBtn.setFont(QFont("Arial",10))
                cancelBtn.setFixedWidth(100)
                cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                lbl4 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                lbl4.setFont(QFont("Arial", 10))
                grid.addWidget(lbl4, 6, 0, 1, 2, Qt.AlignCenter)     
          
        win = Widget()
        win.exec_()
        
    win = Mainwindow(data_list, header)
    win.exec_()
    
def salesRequest():
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('ID', Integer, primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('item_price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String),
        Column('mutation_date', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
     
    sel = select([sales])
    if con.execute(sel).fetchone():
        selsales = select([sales]).order_by(sales.c.receiptnumber)
        rpsales = con.execute(selsales)
    else:
        message = "No records found!"
        alertText(message)
        return
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(100, 50, 1300, 900)
            
            self.setWindowTitle('Sales requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
                                       
    header = ['ID','Receiptnummber','Barcode','Description','Number',\
              'Item-Price','Sub-Total','Sub-Vat','Callname','Mutation-date']      
        
    data_list=[]
    for row in rpsales:
        data_list += [(row)] 
                                   
    win = MyWindow(data_list, header)
    win.exec_()
               
def paymentsRequest():
    metadata = MetaData()
    payments = Table('payments', metadata,
        Column('payID', Integer, primary_key=True),
        Column('kind', String),
        Column('amount', Float),
        Column('bookdate', String),
        Column('paydate', String),
        Column('instance', String),
        Column('accountnumber', String),
        Column('ovorderID', Integer))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
    
    sel = select([payments])
    if con.execute(sel).fetchone():
        selpay = select([payments]).order_by(payments.c.paydate, payments.c.ovorderID)
        rppay = con.execute(selpay)
    else:
        message = 'No records found!'
        alertText(message)
        return
     
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(500, 50, 900, 900)
            self.setWindowTitle('Sales requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
            table_view.clicked.connect(showSelection)

    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
    
    header = ['payID','Kind','Amount','Bookdate','Paydate',\
              'Instance','Accountnumber','Receiptnumber']                                       
        
    data_list=[]
    for row in rppay:
        data_list += [(row)] 
        
    def showSelection(idx):
        mpaynr = idx.data()
        selp = select([payments]).where(payments.c.payID == mpaynr)
        rpp = con.execute(selp).first()
                  
        class MainWindow(QDialog):
            def __init__(self):
                QDialog.__init__(self)
                self.setWindowTitle("Payments instances")
                self.setWindowIcon(QIcon('./logos/logo.jpg'))
                self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                    Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
                self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                       
                self.setFont(QFont('Arial', 10))
                self.setStyleSheet("background-color: #D9E1DF") 
            
                grid = QGridLayout()
                grid.setSpacing(20)
                                                    
                pyqt = QLabel()
                movie = QMovie('./logos/pyqt.gif')
                pyqt.setMovie(movie)
                movie.setScaledSize(QSize(240,80))
                movie.start()
                grid.addWidget(pyqt, 0 ,0, 1, 2)
           
                logo = QLabel()
                pixmap = QPixmap('./logos/logo.jpg')
                logo.setPixmap(pixmap.scaled(70,70))
                grid.addWidget(logo , 0, 1, 1 ,1, Qt.AlignRight)
                
                #kind
                q1Edit = QLineEdit(rpp[1])
                q1Edit.setFixedWidth(250)
                q1Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q1Edit.setDisabled(True)
                                
                #amount
                q2Edit = QLineEdit(str(round(float(rpp[2]),2)))
                q2Edit.setAlignment(Qt.AlignRight)
                q2Edit.setFixedWidth(150)
                q2Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q2Edit.setDisabled(True)
                 
                #bookdate
                q3Edit = QLineEdit(str(rpp[3]))
                q3Edit.setFixedWidth(150)
                q3Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q3Edit.setDisabled(True)
                
                #paydate
                q4Edit = QLineEdit(str(rpp[4]))
                q4Edit.setFixedWidth(150)
                q4Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q4Edit.setDisabled(True)
                             
                #instance
                q5Edit = QLineEdit(rpp[5])
                q5Edit.setFixedWidth(250)
                q5Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q5Edit.setDisabled(True)
                  
                #accountnumber
                q9Edit = QLineEdit(str(rpp[6]))
                q9Edit.setFixedWidth(250)
                q9Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q9Edit.setDisabled(True)
                                 
                #receiptnumber)
                q12Edit = QLineEdit(str(rpp[7]))
                q12Edit.setAlignment(Qt.AlignRight)
                q12Edit.setFixedWidth(150)
                q12Edit.setStyleSheet("QLineEdit { font-size: 10pt; font-family: Arial; color: black }")
                q12Edit.setDisabled(True)    
                        
                lbl3 = QLabel('Kind')  
                lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl3, 2, 0)
                grid.addWidget(q1Edit, 2, 1)
                                                     
                lbl4 = QLabel('Amount')  
                lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl4, 3, 0)
                grid.addWidget(q2Edit, 3, 1)
                
                lbl5 = QLabel('Bookdate')  
                lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl5, 4, 0)
                grid.addWidget(q3Edit, 4, 1)
                
                lbl6 = QLabel('Paydate')  
                lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl6, 5, 0)
                grid.addWidget(q4Edit, 5, 1)
                
                lbl7 = QLabel('Pay')
                lbl7.setFont(QFont("Arial",10))
                grid.addWidget(lbl7, 6, 0, 1, 1, Qt.AlignRight)
                     
                self.cBox = QCheckBox()
                self.cBox.setStyleSheet('color: black; background-color: #F8F7EE')
                grid.addWidget(self.cBox, 6, 1)
                if len(rpp[4])==10:
                    lbl7 = QLabel('Payed')
                    lbl7.setFont(QFont("Arial",10))
                    grid.addWidget(lbl7, 6, 0, 1, 1, Qt.AlignRight)
                    self.cBox.setStyleSheet('color: black')
                    self.cBox.setEnabled(False)
                    
                def cboxChanged():
                    self.cBox.setCheckState(self.cBox.checkState())
                self.cBox.stateChanged.connect(cboxChanged)
                
                def  updPayment(self):
                    mstatus = self.cBox.checkState()
                    if mstatus:
                        mpaydate = str(datetime.datetime.now())[0:10]
                        updpay = update(payments).where(payments.c.payID == mpaynr).\
                        values(paydate = mpaydate)
                        con.execute(updpay)
                        paySuccess()  
                        self.close()
                    else:
                        message = 'Not all fields are filled in!'
                        alertText(message)
                        self.close()
                                                                           
                lbl7 = QLabel('Instance')  
                lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl7, 7, 0)
                grid.addWidget(q5Edit, 7, 1, 1, 2)
                 
                lbl20 = QLabel('Accountnumber')  
                lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl20, 10, 0)
                grid.addWidget(q9Edit, 10, 1, 1, 2)
                      
                lbl23 = QLabel('Receiptnumber')  
                lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                grid.addWidget(lbl23, 13, 0)
                grid.addWidget(q12Edit, 13, 1)
               
                payBtn = QPushButton('Paying')
                payBtn.clicked.connect(lambda: updPayment(self))
        
                grid.addWidget(payBtn, 14, 1, 1 , 1, Qt.AlignRight)
                payBtn.setFont(QFont("Arial",10))
                payBtn.setFixedWidth(100)
                payBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                closeBtn = QPushButton('Close')
                closeBtn.clicked.connect(self.close)
        
                grid.addWidget(closeBtn, 14, 1)
                closeBtn.setFont(QFont("Arial",10))
                closeBtn.setFixedWidth(100)
                closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 15, 0, 1, 2, Qt.AlignCenter)
                
                self.setLayout(grid)
                self.setGeometry(600, 200, 150, 150)
                
        window = MainWindow()
        window.exec_()
                                     
    win = MyWindow(data_list, header)
    win.exec_()
    
def emplAccess():
    metadata = MetaData()
    accounts = Table('accounts', metadata,
         Column('barcodeID', String, primary_key=True),
         Column('firstname', String),
         Column('lastname', String),
         Column('access', Integer),
         Column('callname', String))
        
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/cashregister')
    con = engine.connect()
    while True:
        inlognr = random.randint(0, 99999)
        inlogstr = str(int(2400000+inlognr))
        ean = barcode.get('ean8', inlogstr, writer=ImageWriter()) # for barcode as png
        mbarcode = ean.get_fullcode()
        
        selbarc = select([accounts]).where(accounts.c.barcodeID==mbarcode)
        rpbarc = con.execute(selbarc).first()
        if not rpbarc:
            if sys.platform == 'win32':
               ean.save('.\\Barcodes\\Accounts\\'+str(mbarcode))
               break
            else:
               ean.save('./Barcodes/Accounts/'+str(mbarcode))
               break
           
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            
            self.setWindowTitle("Access Accounts")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")  
    
            grid = QGridLayout()
            grid.setSpacing(20)
            
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            q1Edit = QLineEdit(str(mbarcode))
            q1Edit.setFixedWidth(100)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.setStyleSheet("color: black")
            q1Edit.setDisabled(True)
                            
            q2Edit = QLineEdit()     #firstname
            q2Edit.setFixedWidth(200)
            q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            q2Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^.{1,20}$")
            input_validator = QRegExpValidator(reg_ex, q2Edit)
            q2Edit.setValidator(input_validator)
             
            q3Edit = QLineEdit()   #lastname
            q3Edit.setFixedWidth(200)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^.{1,20}$")
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)
             
            q4Edit = QLineEdit()   #callname
            q4Edit.setFixedWidth(200)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^.{1,20}$")
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)
            
            q5Edit = QLineEdit('1')   #access
            q5Edit.setFixedWidth(30)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0123]{1}$")
            input_validator = QRegExpValidator(reg_ex, q5Edit)
            q5Edit.setValidator(input_validator)
            
            def q2Changed():
                q2Edit.setText(q2Edit.text())
            q2Edit.textChanged.connect(q2Changed)
             
            def q3Changed():
                q3Edit.setText(q3Edit.text())
            q3Edit.textChanged.connect(q3Changed)  
            
            def q4Changed():
                q4Edit.setText(q4Edit.text())
            q4Edit.textChanged.connect(q4Changed)  
            
            def q5Changed():
                q5Edit.setText(q5Edit.text())
            q5Edit.textChanged.connect(q5Changed)

            lbl1 = QLabel('Accountbarcode')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 4, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q1Edit, 4, 1)
                      
            lbl2 = QLabel('First name')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 5, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q2Edit, 5, 1)
            
            lbl3 = QLabel('Last name')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q3Edit, 6, 1)
            
            lbl4 = QLabel('Call name')
            lbl4.setFont(QFont("Arial", 10))
            grid.addWidget(lbl4, 7, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q4Edit, 7, 1)
            
            lbl5 = QLabel('Access level')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 8, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(q5Edit, 8, 1)
            
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insertacc())
               
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(applyBtn,9, 2, 1 , 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close) 
    
            grid.addWidget(cancelBtn, 9, 1, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 10, 0, 1, 3, Qt.AlignCenter)
          
            def insertacc():
                fname = q2Edit.text()
                lname = q3Edit.text()
                cname = q4Edit.text()
                maccess = q5Edit.text()
                if fname and lname and cname:
                    insacc = insert(accounts).values(barcodeID = str(mbarcode),\
                       firstname = fname, lastname = lname,\
                       callname = cname, access = int(maccess))
                    con.execute(insacc)
                    message = 'Update succeeded!'
                    actionOK(message)
                    self.close()
                else:
                    message = 'Not all fields are filled in!'
                    alertText(message)
                    self.close() 
           
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
            
    window = Widget()
    window.exec_()
    
def insertArticles():
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('short_descr', String),
        Column('item_price', Float),
        Column('selling_price', Float),
        Column('item_stock', Float),
        Column('item_unit', String),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('location_warehouse', String),
        Column('article_group', String),
        Column('thumbnail', String),
        Column('category', Integer),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('mutation_date', String),
        Column('annual_consumption_1', Float),
        Column('annual_consumption_2', Float),
        Column('VAT', String))
 
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
    try:
        mbarcode=(con.execute(select([func.max(articles.c.barcode, type_=String)])\
                        .where(articles.c.barcode.like('28'+'%'))).scalar())
        mbarcode = int(str(mbarcode[:12]))+1
        ean = barcode.get('ean13',str(mbarcode), writer=ImageWriter()) #for barcode as png
        mbarcode = ean.get_fullcode()
    except:
        mbarcode = 280000000001
        ean = barcode.get('ean13',str(mbarcode), writer=ImageWriter()) #for barcode as png
        mbarcode = ean.get_fullcode()
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            
            self.setWindowTitle("Articles new insert")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF")  
    
            grid = QGridLayout()
            grid.setSpacing(20)
            
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 3, 1 ,1, Qt.AlignRight)
              
            #barcode
            self.q1Edit = QLineEdit(str(mbarcode)) 
            self.q1Edit.setFixedWidth(130)
            self.q1Edit.setFont(QFont("Arial",10))
            self.q1Edit.setStyleSheet("color: black")
            self.q1Edit.setDisabled(True)

            #description
            self.q2Edit = QLineEdit()    
            self.q2Edit.setFixedWidth(400)
            self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q2Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, self.q2Edit)
            self.q2Edit.setValidator(input_validator)
            
            #short-description
            self.q2aEdit = QLineEdit()    
            self.q2aEdit.setFixedWidth(200)
            self.q2aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q2aEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^.{1,50}$")
            input_validator = QRegExpValidator(reg_ex, self.q2aEdit)
            self.q2Edit.setValidator(input_validator)
            
            #item_price
            self.q3Edit = QLineEdit('0')
            self.q3Edit.setFixedWidth(100)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
            self.q3Edit.setValidator(input_validator)
            
            #selling-price
            self.q3aEdit = QLineEdit('0')
            self.q3aEdit.setFixedWidth(100)
            self.q3aEdit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3aEdit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3aEdit)
            self.q3Edit.setValidator(input_validator)
          
            #item_unit
            self.q5Edit = QComboBox()
            self.q5Edit.setFixedWidth(170)
            self.q5Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q5Edit.setFont(QFont("Arial",10))
            self.q5Edit.addItem('stuk')
            self.q5Edit.addItem('100')
            self.q5Edit.addItem('meter')
            self.q5Edit.addItem('kg')
            self.q5Edit.addItem('liter')
            self.q5Edit.addItem('m²')
            self.q5Edit.addItem('m³')
            
            #minimum stock
            self.q6Edit = QLineEdit('0')
            self.q6Edit.setFixedWidth(100)
            self.q6Edit.setFont(QFont("Arial",10))
            self.q6Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q6Edit)
            self.q6Edit.setValidator(input_validator)

            #order_size
            self.q7Edit = QLineEdit('0')
            self.q7Edit.setFixedWidth(100)
            self.q7Edit.setFont(QFont("Arial",10))
            self.q7Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            reg_ex = QRegExp("^[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q7Edit)
            self.q7Edit.setValidator(input_validator)
                         
            #location
            self.q8Edit = QLineEdit()
            self.q8Edit.setFixedWidth(100)
            self.q8Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q8Edit.setFont(QFont("Arial",10))
                        
            # article_group
            self.q9Edit = QLineEdit()
            self.q9Edit.setFixedWidth(200)
            self.q9Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q9Edit.setFont(QFont("Arial",10))
                
            #thumbnail
            self.q10Edit = QLineEdit('./thumbs/')
            self.q10Edit.setFixedWidth(200)
            self.q10Edit.setFont(QFont("Arial",10))
            self.q10Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                        
            #category
            self.q11Edit = QComboBox()
            self.q11Edit.setFixedWidth(260)
            self.q11Edit.setFont(QFont("Arial",10))
            self.q11Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q11Edit.addItem('0. Daily fresh products.')
            self.q11Edit.addItem('1. Stock-driven < 3 days.')
            self.q11Edit.addItem('2. Stock-driven < 1 weeks.')
            self.q11Edit.addItem('3. Stock-driven < 2 weeks.')
            self.q11Edit.addItem('4. Stock-driven < 3 weeks.')
            self.q11Edit.addItem('5. Stock-driven < 6 weken')
            self.q11Edit.addItem('6. Stock-driven < 12 weeks')
            self.q11Edit.addItem('7. Stock-driven < 26 weeks')
            self.q11Edit.addItem('8. Stock-driven < 52 weeks') 
 
            #vat
            self.q12Edit = QComboBox()
            self.q12Edit.setFixedWidth(100)
            self.q12Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q12Edit.setFont(QFont("Arial",10))
            self.q12Edit.addItem('high')
            self.q12Edit.addItem('low')
            self.q12Edit.addItem('zero')
            
            #barcode overruled
            self.q13Edit = QLineEdit() 
            self.q13Edit.setFixedWidth(130)
            self.q13Edit.setFont(QFont("Arial",10))
            self.q13Edit.setStyleSheet("color: black; background-color: #F8F7EE")
            self.q13Edit.setSelection(0,13)
            
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            def q2aChanged():
                self.q2aEdit.setText(self.q2aEdit.text())
            self.q2aEdit.textChanged.connect(q2aChanged)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            def q3aChanged():
                self.q3aEdit.setText(self.q3aEdit.text())
            self.q3aEdit.textChanged.connect(q3aChanged)
            
            def q5Changed():
                self.q5Edit.setCurrentText(self.q5Edit.currentText()) #+1
            self.q5Edit.currentIndexChanged.connect(q5Changed)
            
            def q6Changed():
                self.q6Edit.setText(self.q6Edit.text())
            self.q6Edit.textChanged.connect(q6Changed)
            
            def q7Changed():
                self.q7Edit.setText(self.q7Edit.text())
            self.q7Edit.textChanged.connect(q7Changed)
            
            def q8Changed():
                self.q8Edit.setText(self.q8Edit.text())
            self.q8Edit.textChanged.connect(q8Changed)
            
            def q9Changed():
                self.q9Edit.setText(self.q9Edit.text())
            self.q9Edit.textChanged.connect(q9Changed)
            
            def q10Changed():
                self.q10Edit.setText(self.q10Edit.text())
            self.q10Edit.textChanged.connect(q10Changed)
            
            def q11Changed():
                self.q11Edit.setCurrentIndex(self.q11Edit.currentIndex())
            self.q11Edit.currentIndexChanged.connect(q11Changed)
            
            def q12Changed():
                self.q5Edit.setCurrentText(self.q12Edit.currentText()) 
            self.q12Edit.currentIndexChanged.connect(q12Changed)
            
            def q13Changed():
                self.q13Edit.setText(self.q13Edit.text()) 
            self.q13Edit.textChanged.connect(q13Changed)
           
            grid.addWidget(QLabel('Barcodenumber'), 1, 0)
            grid.addWidget(self.q1Edit, 1, 1)
            
            grid.addWidget(QLabel('Description'), 2, 0)
            grid.addWidget(self.q2Edit, 2, 1 ,1 ,2)
            
            grid.addWidget(QLabel('Item_Price'), 3, 0)
            grid.addWidget(self.q3Edit, 3, 1)
            
            grid.addWidget(QLabel('Item-Unit'), 3, 2)
            grid.addWidget(self.q5Edit, 3, 3)
            
            grid.addWidget(QLabel('Minimum_Stock'), 4, 0)
            grid.addWidget(self.q6Edit, 4, 1)
            
            grid.addWidget(QLabel('Order-Size'), 4, 2)
            grid.addWidget(self.q7Edit, 4, 3)
              
            grid.addWidget(QLabel('Location'), 5, 0)
            grid.addWidget(self.q8Edit, 5, 1)
            
            grid.addWidget(QLabel('Articlegroup'), 5, 2)
            grid.addWidget(self.q9Edit, 5, 3)
            
            grid.addWidget(QLabel('Thumbnail'), 6, 0)
            grid.addWidget(self.q10Edit, 6, 1)
            
            grid.addWidget(QLabel('Category'), 6, 2 )
            grid.addWidget(self.q11Edit, 6, 3)
            
            grid.addWidget(QLabel('VAT'), 7, 0 )
            grid.addWidget(self.q12Edit, 7, 1)
            
            grid.addWidget(QLabel('Short-Descr'), 8, 0)
            grid.addWidget(self.q2aEdit, 8, 1)
            
            grid.addWidget(QLabel('Selling-Price'), 8, 2)
            grid.addWidget(self.q3aEdit, 8, 3)
            
            grid.addWidget(QLabel('Barcode overruled by scanning'), 9, 0)
            grid.addWidget(self.q13Edit, 9, 1)
            grid.addWidget(QLabel('Fill all fields before scanning'), 9, 2)
  
            def insArticle(self):
                if len(self.q13Edit.text())==13 and checkEan13(self.q13Edit.text()):
                    mbarcode = str(self.q13Edit.text())
                else:
                    mbarcode = str(self.q1Edit.text())
                mdescr = self.q2Edit.text()
                mshort = self.q2aEdit.text()
                mprice = float(self.q3Edit.text())
                mselprice = float(self.q3aEdit.text())
                munit = self.q5Edit.currentText()
                mminstock = float(self.q6Edit.text())
                morder_size = float(self.q7Edit.text())
                mlocation = self.q8Edit.text()
                martgroup = self.q9Edit.text()
                mthumb = self.q10Edit.text()
                mcategory = self.q11Edit.currentIndex()+1
                mvat = self.q12Edit.currentText()
                if mdescr and mprice and morder_size and mlocation and mcategory:
                    insart = insert(articles).values(barcode=mbarcode,description=mdescr,\
                        short_descr=mshort,item_price=mprice,selling_price=mselprice,\
                        item_unit=munit, minimum_stock = mminstock,order_size=morder_size,\
                        location_warehouse=mlocation,article_group=martgroup,\
                        thumbnail=mthumb,category=mcategory,VAT=mvat)
                    con.execute(insart)
                    if sys.platform == 'win32':
                        ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                    else:
                        ean.save('./Barcodes/Articles/'+str(mbarcode))
                    message = 'Update succeeded!'
                    actionOK(message)
                    self.close()
                else:
                    message = 'Not all fields are filled in!'
                    alertText(message)
                    self.close()
 
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insArticle(self))
    
            grid.addWidget(applyBtn, 10, 3, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)
            
            grid.addWidget(cancelBtn, 10, 3)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 11, 0, 1, 4, Qt.AlignCenter)
    
            self.setLayout(grid)
            self.setGeometry(500, 200, 150, 100)
 
    window = Widget()
    window.exec_()
     
def requestLoss():
    metadata = MetaData()
    loss = Table('loss', metadata,
       Column('lossID', Integer, primary_key=True),
       Column('barcode', None, ForeignKey('articles.barcode')),
       Column('number', Float),
       Column('bookdate', String),
       Column('category', String))
    articles = Table('articles', metadata,
       Column('barcode', String, primary_key=True),
       Column('description', String),
       Column('item_price', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
    
    sel = select([loss, articles]).where(articles.c.barcode==loss.c.barcode).\
        order_by(loss.c.category, loss.c.bookdate)
    if con.execute(sel).fetchone():
        selloss = select([loss, articles]).where(articles.c.barcode==loss.c.barcode).\
            order_by(loss.c.category, loss.c.bookdate)
        rploss = con.execute(selloss)
    else:
        message = "No records found!"
        alertText(message)
        return
    
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args)
            self.setGeometry(600, 50, 1000, 800)
            self.setWindowTitle('Loss articles requesting')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setColumnHidden(5,True)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
                
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            veld = self.mylist[index.row()][index.column()]
            if not index.isValid():
                return None
            elif role == Qt.TextAlignmentRole and (type(veld) == float or type(veld) == int):
                return Qt.AlignRight | Qt.AlignVCenter
            elif role != Qt.DisplayRole:
                return None
            if type(veld) == float:
                return '{:12.2f}'.format(veld)
            else:
                return veld
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None

    header = ['ID','Barcode','Amount','Bookdate','Category','','Description','Item-Price']                                       
    
    data_list=[]
    for row in rploss:
        data_list += [(row)] 

    win = Widget(data_list, header)
    win.exec_()
    
def bookingLoss():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Booking loss articles")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
                   
            self.setFont(QFont('Arial', 10))
            self.setStyleSheet("background-color: #D9E1DF") 
                
            grid = QGridLayout()
            grid.setSpacing(20)      
                
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
            self.k0Edit = QComboBox()
            self.k0Edit.setFixedWidth(230)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Booking loss')
            self.k0Edit.addItem('Request loss items')
                           
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    mflag = 2
                    articleRequest(mflag, 0)
                elif mindex == 1:
                    requestLoss()
     
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
             
            grid.addWidget(closeBtn, 2, 1)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
                
    window = Widget()
    window.exec_() 
    
def purchaseCollect(self):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
        Column('item_stock', Float),
        Column('item_unit', String),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('order_balance', Float),
        Column('order_status', Boolean),
        Column('supplierID', Integer))
    purchase_orderlines = Table('purchase_orderlines', metadata,
        Column('orderlineID', Integer, primary_key=True),
        Column('barcode', String),
        Column('description', String),
        Column('item_price', Float),
        Column('item_unit', String),
        Column('item_stock', Float),
        Column('minimum_stock', Float),
        Column('order_size', Float),
        Column('supplierID', Integer),
        Column('bookdate', String))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
     
    selarticles = select([articles]).order_by(articles.c.barcode).\
      where(and_(articles.c.item_stock + articles.c.order_balance \
             < articles.c.minimum_stock, articles.c.order_status == True))
    rparticles = con.execute(selarticles)
    mbookdate = str(datetime.datetime.now())[0:10]
    mflag = 0
    for row in rparticles:
        try:
            mordnr = (con.execute(select([func.max(purchase_orderlines.c.orderlineID,\
                            type_=Integer)])).scalar())
            mordnr += 1
        except:
            mflag = 1
            mordnr = 1
        mbarcode = row[0]
        mdescr= row[1]
        mprice = row[2]
        mstock = row[3]
        munit = row[4]
        minstock =row[5]
        mordersize = row[6]
        msupplier = row[9]
        inssup = insert(purchase_orderlines).values(orderlineID=mordnr,barcode=mbarcode,\
            description=mdescr,item_price=mprice,item_unit=munit,item_stock=mstock,\
            minimum_stock=minstock,order_size=mordersize,supplierID=msupplier,bookdate=mbookdate)
        con.execute(inssup)
        updart = update(articles).where(articles.c.barcode==row[0]).values(order_status=False,\
            order_balance=articles.c.order_balance+row[6])
        con.execute(updart)
    if mflag:
        message = 'Orderlines inserts processed successful!'
        actionOK(message)
    else:
        message = "No matching records found!"
        alertText(message) 
    self.close()

def logon(self, barcodenr):
    metadata = MetaData()
    accounts = Table('accounts', metadata,
        Column('barcodeID', String, primary_key=True),
        Column('callname', String),
        Column('access', Integer))
    engine = create_engine('postgresql+psycopg2://postgres:@localhost/cashregister')
    con = engine.connect()
    selacc = select([accounts]).where(accounts.c.barcodeID == barcodenr)
    rpacc = con.execute(selacc).first()
    self.mbarcode = rpacc[0]
    self.mcallname = rpacc[1]
    self.maccess = rpacc[2]
    self.logon = self.q1Edit.text()
    self.q1Edit.setText('')
    self.pixmap = QPixmap('./logos/green.png')
    self.logonstate.setPixmap(self.pixmap.scaled(30,30))
    self.plusminBtn.setStyleSheet("color: black;  background-color: #FFD700")
    if self.maccess < 2:
        self.plusminBtn.setText('+')
        self.plusminBtn.setChecked(False)
        self.plusminBtn.setHidden(True)
        self.qspin.setRange(1, 99)
        self.adminBtn.setHidden(True)
    elif self.maccess == 2:
        self.plusminBtn.setHidden(False)
        self.adminBtn.setHidden(True)
    elif self.maccess == 3:
        self.plusminBtn.setHidden(False)
        self.adminBtn.setHidden(False)
             
def info():
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Information Barcodescan")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblinfo = QLabel('Cashregister System')
            grid.addWidget(lblinfo, 0, 0, 1, 2, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgba(45, 83, 115, 255); font: 25pt Comic Sans MS")
            
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 0, 1, 1, Qt.AlignRight)
        
            lbl = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            
            infoEdit = QPlainTextEdit('''\t\t\t\tInstruction barcode scan.
        
        Logging in takes place with a barcode card with 4 access levels.
        Level 1. Selling, scanning, printing (normal cash register usage).
        Level 2. Return bookings, a checkable ± button is shown, with which return bookings can be made.
        Level 3. Administration, a button Adminstration is shown, for assigning productbuttons,
                 creating accounts, administration, perform stock management and imports.
        level 0. Employee is not allowed for operation.
        Employee first time scan barcode  = logon, second time = logout.
        Other employee scanning = switching employee (for return booking, or replacement).
                         
        Article scanning:
        By default, scanning is performed with a number of 1.
        With the spinbox the correct number can be chosen for scanning, this can be done by the arrows of 
        the spinbox or with the mouse wheel. After every scan, the number is reset to 1.
        Selecting can also been done with the productbuttons for unpackaged products.
        When scanning is started, the "Exit" button is blocked until the button "Next customer" is pressed.
        The print button and the customer button are blocked until the first transaction is posted.
        In the following cases, an error message appears in red below the display screen. An acoustic alarm 
        will also sound for the following 5 cases.  
        
        1. If a read error occurs when scanning the barcode.
        2. If there is insufficient stock to deliver the order, current stock will also been showed.
        3. If the product is not (yet) included in the range.
        4. If not logged in.
        5. If the employee is not allowed for operation.
             
        If the item cannot be scanned, it is possible to insert the barcode manually after inserting press 
        <Enter> on the keyboard.
                           
        The receipt can be printed after scanning is finished.
        Before exiting the program, first press the customer button, so the close button is released.
        This will make the necessary bookings and prepare the order for the next customer.
        ''')
            grid.addWidget(infoEdit, 1, 0)
                           
            infoEdit.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 100, 1000, 800)
            
    window = Widget()
    window.exec_()

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setFont(QFont("Arial", 10))
    msg.setText('Just a moment printing is starting!')
    msg.setWindowTitle('Printing')
    msg.exec_()

def printBon(self):
    msgBox=QMessageBox()
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msgBox.setWindowTitle("Printing receipt")
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setFont(QFont("Arial", 10))
    msgBox.setText("Do you want to print the receipt?");
    msgBox.setStandardButtons(QMessageBox.Yes)
    msgBox.addButton(QMessageBox.No)
    msgBox.setStyleSheet("color: black;  background-color: gainsboro")
    msgBox.setDefaultButton(QMessageBox.Yes)
    if(msgBox.exec_() == QMessageBox.Yes):
        metadata = MetaData()
        sales = Table('sales', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('receiptnumber', Integer),
            Column('barcode', String),
            Column('description', String),
            Column('number', Float),
            Column('item_price', Float),
            Column('sub_total', Float),
            Column('sub_vat', Float))
        
        engine = create_engine('postgresql+psycopg2://postgres:@localhost/cashregister')
        con = engine.connect()
        delbal = delete(sales).where(and_(sales.c.number == 0,\
                       sales.c.receiptnumber == self.mreceipt))
        con.execute(delbal)
        selb = select([sales]).where(sales.c.receiptnumber == self.mreceipt).order_by(sales.c.barcode)
        rpb = con.execute(selb)
        def heading(self, mpage):
            head=\
    ('Sales - Ordernumber: '+ str(self.mreceipt)+' Date : '+str(datetime.datetime.now())[0:10]+' Pagenumber '+str(mpage)+' \n'+
    '==================================================================================================\n'+
    'Artikelnr  Description                                  Number  Item_price    Subtotal         VAT\n'+
    '==================================================================================================\n')
            return(head) 
        mpage = 0
        rgl = 0
        if sys.platform == 'win32':
            fbarc = '.\\forms\\Sales\\'+str(self.mreceipt)+'.txt'
        else:
            fbarc = './forms//Sales/'+str(self.mreceipt)+'.txt'
        
        for row in rpb:
            rgl += 1
            if rgl == 1 :
                mpage += 1
                open(fbarc, 'w').write(heading(self, mpage))
                rgl += 4
            elif rgl%58 == 1:
                mpage += 1
                open(fbarc, 'a').write(heading(self, mpage))
                rgl += 4
                
            martnr = row[2]
            mdescr = row[3]
            mnumber = row[4]
            mprice = row[5]
            msubtotal = row[6]
            msubtotvat = row[7]
            open(fbarc,'a').write(str(martnr) +'  '+'{:<40s}'.format(mdescr)+' '+'{:>6d}'\
                     .format(int(mnumber))+'{:>12.2f}'.format(float(mprice))+'{:>12.2f}'\
                     .format(float(msubtotal))+'{:>12.2f}'\
                     .format(float(msubtotvat))+'\n')
             
        tail=\
        ('===================================================================================================\n'+
         'Total  amount to pay inclusive VAT and amount VAT                         '+'{:>12.2f}'.format(self.mtotal)+'{:>12.2f}'.format(self.mtotvat)+' \n'+
         '===================================================================================================\n'+\
         'Employee : '+self.mcallname+' *** Thank you for visiting us ***\n')
        if rgl > 0:
            open(fbarc,'a').write(tail) 
            if sys.platform == 'win32':
                from os import startfile
                startfile(fbarc, "print")
            else:
                from os import system
                system("lpr "+fbarc)
            printing()
        else:
            message = 'There are no transactions yet!'
            alertText(message)
    
def nextClient(self):
    mbookd = str(datetime.datetime.now())[0:10]
    metadata = MetaData()
    sales = Table('sales', metadata,
        Column('ID', Integer(), primary_key=True),
        Column('receiptnumber', Integer),
        Column('barcode', String),
        Column('description', String),
        Column('number', Float),
        Column('price', Float),
        Column('sub_total', Float),
        Column('sub_vat', Float),
        Column('callname', String))
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('value', Float))
             
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
 
    delbal = delete(sales).where(and_(sales.c.number == 0,\
               sales.c.receiptnumber == self.mreceipt))
    con.execute(delbal)
    if self.mtotvat != int(0):
        metadata = MetaData() 
        payments = Table('payments', metadata,
            Column('payID', Integer(), primary_key=True),
            Column('kind', String),
            Column('amount', Float),
            Column('bookdate', String),
            Column('paydate', String),
            Column('instance', String),
            Column('accountnumber', String),
            Column('ovorderID', Integer))
               
        self.mreceipt += 1
        updpar = update(params).where(params.c.paramID == 3).values(value = self.mreceipt)
        con.execute(updpar)
        try:
            paynr = (con.execute(select([func.max(payments.c.payID, type_=Integer)])).scalar())
            paynr += 1
        except:
            paynr = 1        
        insdr = insert(payments).values(payID = paynr, bookdate = mbookd,\
          kind = 'VAT payment    ', amount = self.mtotvat, instance = 'Tax authorities',\
          ovorderID = int(self.mreceipt), accountnumber = 'NL10 ABNA 9999999977')
        con.execute(insdr)
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color:  #B0C4DE")
        self.printBtn.setDisabled(True)
        self.printBtn.setStyleSheet("color: grey; background-color: #00FFFF")
        self.nextBtn.setDisabled(True)
        self.nextBtn.setStyleSheet("color: grey; background-color: #00FFFF")
        
        self.mtotal = 0.00
        self.mtotvat = 0.00
        self.mlist = []
        self.view.setText('')
        self.qtailtext = 'Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(self.mtotal)+'{:\u2000>12.2f}'.format(self.mtotvat)
        self.qtailEdit.setText(self.qtailtext)
    else:
        message = 'There are no transactions yet!'
        alertText(message)
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color:  #B0C4DE")

def giveAlarm():
    if sys.platform == 'win32':
        import winsound
        winsound.Beep(2300,250)
        winsound.Beep(2300,250)
    else:
        #sudo apt install sox
        from os import system
        system('play -nq -t alsa synth {} sine {}'.format(0.25, 2300))
        system('play -nq -t alsa synth {} sine {}'.format(0.25, 2300))

def plusminChange(self):
    if self.plusminBtn.isChecked():
        self.plusminBtn.setText('-')
        self.qspin.setRange(-99, -1)
    else:
        self.plusminBtn.setText('+')
        self.qspin.setRange(1, 99)
        
def checkEan8(c):
    checksum = (int(c[0])+int(c[2])+int(c[4])+int(c[6]))*3+(int(c[1])+
                int(c[3])+int(c[5]))
    checkdigit = (10-(checksum%10))
    if checkdigit == int(c[7]):
        return True
    else:
        return False
        
def checkEan13(c):
    checksum = int(c[0])+int(c[2])+int(c[4])+int(c[6])+int(c[8])+int(c[10])+(int(c[1])+
                int(c[3])+int(c[5])+int(c[7])+int(c[9])+int(c[11]))*3
    checkdigit = (10-(checksum%10))%10
    if checkdigit == int(c[12]):
        return True
    else:
        return False
    
def set_barcodenr(self):
    barcodenr = self.q1Edit.text()
    mnumber = float(self.qspin.value())
    if len(barcodenr) == 8:
        self.q1Edit.setStyleSheet("color:#F8F7EE;  background-color: #F8F7EE")
    else:
        self.q1Edit.setStyleSheet("color:black;  background-color: #F8F7EE")
    self.albl.setText('')
    myear = int(str(datetime.datetime.now())[0:4])
    if len(barcodenr) == 13 and checkEan13(barcodenr) and self.mcallname:
        metadata = MetaData()
        articles = Table('articles', metadata,
            Column('barcode', String, primary_key=True),
            Column('description', String),
            Column('item_price', Float),
            Column('item_stock', Float),
            Column('VAT', String),
            Column('annual_consumption_1', Float),
            Column('annual_consumption_2', Float),
            Column('short_descr', String),
            Column('selling_price', Float))
        sales = Table('sales', metadata,
            Column('ID', Integer(), primary_key=True),
            Column('receiptnumber', Integer),
            Column('barcode', String),
            Column('description', String),
            Column('number', Float),
            Column('item_price', Float),
            Column('sub_total', Float),
            Column('sub_vat', Float),
            Column('callname', String),
            Column('mutation_date', String))
 
        engine = create_engine('postgresql+psycopg2://postgres:@localhost/cashregister')
        con = engine.connect()

        selart = select([articles]).where(articles.c.barcode == barcodenr)
        selbal = select([sales]).where(and_(sales.c.barcode == barcodenr,\
                sales.c.receiptnumber == self.mreceipt))
        rpart = con.execute(selart).first()
        rpbal = con.execute(selbal).first()
        if rpart and rpart[3] < mnumber:
            self.albl.setText('Error message: '+str(int(rpart[3]))+' in stock!')
            giveAlarm()
        elif rpart and self.maccess:
            if rpart[4] == 'high':      
                self.mvat = self.mvath
            elif rpart[4] == 'low': 
                self.mvat = self.mvatl
            else:
                self.mvat = self.mvatz
            martnr = rpart[0]
            mdescr = rpart[1]
            mdescr = mdescr[:40] if len(mdescr) > 40 else mdescr
            mselprice = rpart[8]
            mutdate = str(datetime.datetime.now())[0:10]
            if rpbal:
                updbal = update(sales).where(and_(sales.c.barcode == barcodenr,\
                  sales.c.receiptnumber == self.mreceipt)).values(number = sales.c.number+mnumber,\
                  sub_total = (sales.c.number+mnumber)*mselprice,\
                  sub_vat = (sales.c.number+mnumber)*mselprice*self.mvat, callname = self.mcallname,\
                  mutation_date = mutdate)
                con.execute(updbal)
            else:
                try:
                    midnr = (con.execute(select([func.max(sales.c.ID, type_=Integer)])).scalar())
                    midnr += 1
                except:
                    midnr = 1
                insbal = insert(sales).values(ID = midnr, receiptnumber = self.mreceipt,\
                  barcode = barcodenr, description = mdescr, number = mnumber, item_price = mselprice,\
                  sub_total = mnumber*mselprice, sub_vat = mnumber*mselprice*self.mvat,\
                  callname = self.mcallname, mutation_date = mutdate)
                con.execute(insbal)
            if myear%2 == 1:     #odd year
                updart = update(articles).where(articles.c.barcode == rpart[0])\
                    .values(item_stock = articles.c.item_stock - mnumber,\
                     annual_consumption_2 = articles.c.annual_consumption_2 + mnumber)
                con.execute(updart)
            elif myear%2 == 0:   #even year
                updart = update(articles).where(articles.c.barcode == rpart[0])\
                    .values(item_stock = articles.c.item_stock - mnumber,\
                     annual_consumption_1 = articles.c.annual_consumption_1 + mnumber)
                con.execute(updart)
            
            self.mlist.append('{:\u2000<14s}'.format(martnr)+'{:\u2000<40s}'.format(mdescr)+' {:\u2000>6d}'\
             .format(int(mnumber))+'{:\u2000>12.2f}'.format(mselprice)+'{:\u2000>12.2f}'\
             .format(float(mselprice)*float(mnumber))+'{:\u2000>12.2f}'\
             .format(float(mselprice)*float(mnumber)*self.mvat))
            self.mtotal += float(mselprice)*float(mnumber)
            self.mtotvat += float(mselprice)*float(mnumber)*self.mvat
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(self.mtotal)+'{:\u2000>12.2f}'.format(self.mtotvat)
            self.qtailEdit.setText(self.qtailtext)
            self.qtotalEdit.setText('{:>12.2f}'.format(self.mtotal))
            
            self.view.append(self.mlist[-1])
        elif self.maccess == 0 and self.mcallname:
            self.albl.setText('Errormessage: No permission to execute!')
            giveAlarm()   
        elif self.maccess == 0:
            self.albl.setText('Errormessage:  Please logon with your barcodecard!')
            giveAlarm() 
        else:
            self.albl.setText('Errormessage:  Article not in assortment!')
            giveAlarm()
                  
        self.closeBtn.setDisabled(True)
        self.closeBtn.setStyleSheet("color: grey; background-color: #B0C4DE")
        self.printBtn.setEnabled(True)
        self.printBtn.setStyleSheet("color: black;  background-color: #00FFFF")
        self.nextBtn.setEnabled(True)
        self.nextBtn.setStyleSheet("font: 12pt Arial; color: black; background-color: #00BFFF")
    elif len(barcodenr) == 8 and checkEan8(barcodenr):
        self.q1Edit.setText('')
        if barcodenr == self.checknr and self.maccess > 0:
            self.maccess = 0
            self.plusminBtn.setHidden(True)
            self.adminBtn.setHidden(True)
            self.pixmap = QPixmap('./logos/red.png')
            self.logonstate.setPixmap(self.pixmap.scaled(30,30))
        else:
            self.checknr = barcodenr
            logon(self, barcodenr)
    elif not self.mcallname:
        self.albl.setText('Errormessage:  Please logon with your barcodecard!')
        giveAlarm()
    else:
        #alarm if barcode scan failed
        self.albl.setText('Error Message: Scanning error barcode!')
        giveAlarm()
    
    self.q1Edit.setSelection(0,13)
    self.qspin.setValue(1)
      
def barcodeScan():
    #check order_sizes and minimum_stock
    calculationStock()
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Cashregister Sales")
            self.setWindowIcon(QIcon('./logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                Qt.WindowMinimizeButtonHint) #Qt.WindowMinMaxButtonsHint
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
            
            self.setStyleSheet("background-color: #D9E1DF")
            self.setFont(QFont('Arial', 10))
             
            metadata = MetaData()
            params = Table('params', metadata,
                Column('paramID', Integer(), primary_key=True),
                Column('item', String),
                Column('value', Float),
                Column('buttongroup', String),
                Column('fg_color', String),
                Column('bg_color', String))
                          
            engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
            con = engine.connect()
            selpar = select([params]).order_by(params.c.paramID)
            rppar = con.execute(selpar).fetchall()
                 
            self.mreceipt = int(rppar[2][2])
            self.mvath = rppar[1][2]
            self.mvatl = rppar[0][2]
            self.mvatz = 0
            self.mcallname = '' 
            self.maccess = 0
            self.checknr = ''
            rounding = rppar[6][2]
            
            grid = QGridLayout()
            grid.setSpacing(0)
            
            self.qtotalEdit = QLineEdit('')
            self.qtotalEdit.setPlaceholderText("TOTAL")
            self.qtotalEdit.setFixedSize(150, 45)
            self.qtotalEdit.setDisabled(True)
            self.qtotalEdit.setAlignment(Qt.AlignRight)
            self.qtotalEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
                           
            grid.addWidget(self.qtotalEdit, 9, 10, 1, 1, Qt.AlignTop | Qt.AlignRight)
              
            self.text = ''
            self.qcashEdit = QLineEdit(self.text)
            self.qcashEdit.setPlaceholderText("CASH")
            self.qcashEdit.setFixedSize(150, 48)
            self.qcashEdit.setAlignment(Qt.AlignRight)
            self.qcashEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")  
            self.qcashEdit.setFocusPolicy(Qt.NoFocus)
            grid.addWidget(self.qcashEdit, 9, 10, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
              
            self.qchangeEdit = QLineEdit('')
            self.qchangeEdit.setFixedSize(150, 47)
            self.qchangeEdit.setPlaceholderText("CHANGE")
            self.qchangeEdit.setDisabled(True)
            self.qchangeEdit.setAlignment(Qt.AlignRight)
            self.qchangeEdit.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            grid.addWidget(self.qchangeEdit, 10, 10, 1, 1, Qt.AlignVCenter | Qt.AlignRight)
            
            self.qlbl = QLabel("TRANSFER DATA")
            self.qlbl.setFixedSize(270, 46)
            self.qlbl.setStyleSheet("font: bold 24px; color: lightgrey;  background-color: #7f8371")
            self.qlbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(self.qlbl, 10, 6, 1, 5, Qt.AlignBottom)
            
            self.qlbl1 = QLabel("PAYING")
            self.qlbl1.setFixedSize(150, 46)
            self.qlbl1.setStyleSheet("font: bold 24px; color: lightgrey;  background-color: #7f8371")
            self.qlbl1.setAlignment(Qt.AlignCenter)
            grid.addWidget(self.qlbl1, 10, 10, 1, 1, Qt.AlignBottom)        
            
            def calcChange(self):
                self.qcashEdit.setText(self.text)
                if self.qtotalEdit.text():
                    total = float(self.qtotalEdit.text())
                else:
                    total = 0
                if not (self.qcashEdit.text() == '.' or self.qcashEdit.text() == ''):
                    cash = float(self.qcashEdit.text())
                else:
                    cash = 0
                change = cash-total
                
                def round_nearest(change, rounding):
                    return round(change/rounding) * rounding
               
                self.qchangeEdit.setText('{:>12.2f}'.format(round_nearest(change, rounding)))
                
            calcBtn = QPushButton('REFUND')
            calcBtn.setFocusPolicy(Qt.NoFocus)
            calcBtn.setFixedSize(150, 90)
            calcBtn.setStyleSheet("font: bold 24px; color: white;  background-color: #7f8371")
            
            calcBtn.clicked.connect(lambda: calcChange(self))
            grid.addWidget(calcBtn, 9, 10, 2, 1, Qt.AlignVCenter | Qt.AlignRight)
            
            rlist = ['1','2','3','4','5','6','7','8','9','0','.','DEL']
            for t in range(0,12):
                rBtn = QPushButton()
                rBtn.setFixedSize(90,94)
                rBtn.setFont(QFont("Times", 14, 75))
                rBtn.setStyleSheet("color: white;  background-color: #7f8371")
                rBtn.setFocusPolicy(Qt.NoFocus)
                rBtn.setText(rlist[t])
                if t == 0:
                   grid.addWidget(rBtn, 8, 6, 1, 3, Qt.AlignTop)
                elif t == 1:
                   grid.addWidget(rBtn, 8, 6, 1, 3, Qt.AlignTop | Qt.AlignCenter)
                elif t == 2:
                   grid.addWidget(rBtn, 8, 6, 1, 3, Qt.AlignTop | Qt.AlignRight)
                elif t == 3:
                   grid.addWidget(rBtn, 8, 6, 2, 3, Qt.AlignVCenter)
                elif t == 4:
                   grid.addWidget(rBtn, 8, 6, 2, 3, Qt.AlignVCenter | Qt.AlignCenter)
                elif t == 5:
                   grid.addWidget(rBtn, 8, 6, 2, 3, Qt.AlignVCenter | Qt.AlignRight)
                elif t == 6:
                   grid.addWidget(rBtn, 8, 6, 2, 3, Qt.AlignBottom)
                elif t == 7:
                   grid.addWidget(rBtn, 8, 6, 2, 3, Qt.AlignBottom | Qt.AlignCenter)
                elif t == 8:
                   grid.addWidget(rBtn, 8, 6, 2, 3, Qt.AlignBottom | Qt.AlignRight)
                elif t == 9:
                   grid.addWidget(rBtn, 10, 6, 2, 3, Qt.AlignTop)
                elif t == 10:
                   grid.addWidget(rBtn, 10, 6, 2, 3, Qt.AlignTop | Qt.AlignCenter)
                elif t == 11:
                   grid.addWidget(rBtn, 10, 6, 2, 3, Qt.AlignTop | Qt.AlignRight)
 
                rBtn.clicked.connect(lambda checked, nr = rlist[t] : getnumber(nr))
                
            def getnumber(nr):
                if nr == '.' and '.' in self.text:
                    return
                elif nr == 'DEL':
                    nr = ''
                    self.text = nr
                self.text += nr
                self.qcashEdit.setText(self.text)

            self.q1Edit = QLineEdit('')
            self.q1Edit.setStyleSheet("color: #F8F7EE;  background-color: #F8F7EE")
            self.q1Edit.setFont(QFont("Arial", 12))
            self.q1Edit.setFixedSize(155, 30)
            self.q1Edit.setFocus(True)
            reg_ex = QRegExp("^[0-9]{8}|^[0-9]{13}$")
            input_validator = QRegExpValidator(reg_ex, self.q1Edit)
            self.q1Edit.setValidator(input_validator)
            self.q1Edit.returnPressed.connect(lambda: set_barcodenr(self))
                       
            self.qspin = QSpinBox()
            self.qspin.setRange(1, 99)
            self.qspin.setValue(1)
            self.qspin.setFocusPolicy(Qt.NoFocus)
            self.qspin.lineEdit().setReadOnly(True)
            self.qspin.setFrame(True)
            self.qspin.setFont(QFont('Arial', 12))
            self.qspin.setStyleSheet("color: black;  background-color: #F8F7EE")
            self.qspin.setFixedSize(60, 30)
             
            def valuechange():
                self.qspin.setValue(self.qspin.value())
            self.qspin.valueChanged.connect(valuechange)
            
            self.logonstate = QLabel()
            self.pixmap = QPixmap('./logos/red.png')
            self.logonstate.setPixmap(self.pixmap.scaled(30,30))
            grid.addWidget(self.logonstate, 5, 8, 1, 1, Qt.AlignRight | Qt.AlignVCenter)
                     
            mkop = QLineEdit()
            mkoptext = 'Articlenumber Description                              Number  Item_price    Subtotal         VAT'
            mkop.setText(mkoptext)
            mkop.setReadOnly(True)
            mkop.setFont(QFont("Consolas", 12, 75))
            mkop.setStyleSheet("color: black; background-color: #F8F7EE")  
            mkop.setFocusPolicy(Qt.NoFocus)
            mkop.setFixedWidth(1110)  
            
            self.view = QTextEdit()
            self.view.setStyleSheet('color: black; background-color: #F8F7EE')  
            self.mlist = []
            self.view.setText('')
            self.view.setFont(QFont("Consolas", 12, 75))
            self.view.setFocusPolicy(Qt.NoFocus)
            self.view.setFixedSize(1110, 180)  
            
            self.mtotal = 0.00
            self.mtotvat = 0.00
            self.qtailEdit = QLineEdit()
            self.qtailEdit.setFont(QFont("Consolas", 12, 75))
            self.qtailEdit.setStyleSheet('color: black; background-color: #F8F7EE') 
            self.qtailEdit.setReadOnly(True)
            self.qtailEdit.setFixedWidth(1110)
            self.qtailEdit.setFocusPolicy(Qt.NoFocus)
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(self.mtotal)+'{:\u2000>12.2f}'.format(self.mtotvat)
            self.qtailEdit.setText(self.qtailtext)
            
            grid .addWidget(mkop, 2, 0, 1, 9, Qt.AlignCenter)           
            grid.addWidget(self.view, 3 ,0, 1, 9, Qt.AlignCenter)
            grid.addWidget(self.qtailEdit, 4, 0, 1, 9, Qt.AlignCenter)
            
            self.albl = QLabel()
            self.albl.setFont(QFont("Arial", 12, 75))
            self.albl.setStyleSheet("color: red ; background-color : #39CCCC")
            self.albl.setText("Notification Bar")
            self.albl.setAlignment(Qt.AlignCenter)
            self.albl.setFixedSize(1080, 30)

            grid.addWidget(self.albl, 5, 0, 1, 9)

            lbl1 = QLabel('Barcodescan')
            lbl1.setFont(QFont("Arial", 12))
            grid.addWidget(lbl1, 7, 6, 1, 1, Qt.AlignTop)
            grid.addWidget(self.q1Edit, 7, 7, 1, 2, Qt.AlignRight | Qt.AlignTop)
            
            lbl2 = QLabel('Number')
            lbl2.setFont(QFont("Arial", 12))
            grid.addWidget(lbl2, 7, 6, 1, 1, Qt.AlignVCenter)
            grid.addWidget(self.qspin, 7, 8, 1, 1, Qt.AlignRight | Qt.AlignVCenter)
                    
            metadata = MetaData()
            buttons = Table('buttons', metadata,
                Column('buttonID', Integer(), primary_key=True),
                Column('buttontext', String),
                Column('barcode',  String),
                Column('fg_color', String),
                Column('bg_color', String))
                        
            #choose next groupbutton (from 5) see line 4244 and start with group 1
            #see line 4274 and 4275
            def btngroupChange(btngroup):
                if btngroup == 1:
                    index = 0
                    hBtn = QPushButton(rppar[7][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[7][4]+';background-color:'+rppar[7][5])
                    btngroup = int(rppar[8][2])
                elif btngroup == 2:
                    index = 24
                    hBtn = QPushButton(rppar[8][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[8][4]+';background-color:'+rppar[8][5])
                    btngroup = int(rppar[9][2])
                elif btngroup == 3:
                    index = 48
                    hBtn = QPushButton(rppar[9][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[9][4]+';background-color:'+rppar[9][5])
                    btngroup = int(rppar[10][2])
                elif btngroup == 4:
                    index = 72
                    hBtn = QPushButton(rppar[10][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[10][4]+';background-color:'+rppar[10][5])
                    btngroup = int(rppar[11][2])
                elif btngroup == 5:
                    index = 96
                    hBtn = QPushButton(rppar[11][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[11][4]+';background-color:'+rppar[11][5])
                    btngroup = int(rppar[12][2])
                elif btngroup == 6:
                    index = 120
                    hBtn = QPushButton(rppar[12][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[12][4]+';background-color:'+rppar[12][5])
                    btngroup = int(rppar[13][2])
                elif btngroup == 7:
                    index = 144
                    hBtn = QPushButton(rppar[13][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[13][4]+';background-color:'+rppar[13][5])
                    btngroup = int(rppar[14][2])
                elif btngroup == 8:
                    index = 168
                    hBtn = QPushButton(rppar[14][3].strip())
                    hBtn.setStyleSheet('color: '+rppar[14][4]+';background-color:'+rppar[14][5])
                    btngroup = int(rppar[7][2])
                hBtn.setFont(QFont("Times", 10, 75))
                hBtn.setFocusPolicy(Qt.NoFocus)
                hBtn.setFixedSize(140, 140)
                grid.addWidget(hBtn, 7, 0) #position groupbutton on first position from thirst row
                                                            
                hBtn.clicked.connect(lambda: btngroupChange(btngroup)) # switch group if button 1 clicked
                          
                a = index   #freeze index at startposition and use a as pointer
                selbtn = select([buttons]).where(and_(buttons.c.buttonID>index-1,\
                     buttons.c.buttonID<index+24)).order_by(buttons.c.buttonID)
                rpbtn = con.execute(selbtn) #select buttonrange from chosen group
                
                #place 5 buttons on thirst row and 6 buttons on 2nd 3thrd and 4thd row
                #choose buttontext and position buttons on grid
                btnlist = []
                for row in rpbtn:
                    if self.maccess < 3:               
                        aBtn = QPushButton(row[1].strip()) #choose buttontext
                        btnlist.append(row[2].strip()) #compile list with barcodenumbers
                    else:    #showbuttonnumber and barcode for administrator
                        aBtn = QPushButton(str(row[0])+'\n'+row[2][0:6]+'\n'+row[2][6:13])
                        btnlist.append(str(row[0]))    #choose buttonnumber
                    aBtn.setFont(QFont("Times", 10, 75))
                    aBtn.setStyleSheet('color:'+row[3]+'; background-color:'+row[4])
                    aBtn.setFocusPolicy(Qt.NoFocus)
                    aBtn.setFixedSize(140, 140)
                    if a < index+6 and (a%6 > 0):
                        grid.addWidget(aBtn, 7, a%6) #row 1 buttons minus first position for buttongroup
                    elif a < index+12:
                        grid.addWidget(aBtn, 8, a%6) #row 2 buttons
                    elif a < index+18:
                        grid.addWidget(aBtn, 9, a%6) #row 3 buttons
                    elif a < index+24:
                        grid.addWidget(aBtn, 10, a%6) #row 4 buttons
                    
                    #choose barcodenumber linked with clicked button
                    if self.maccess < 3:
                        aBtn.clicked.connect(lambda checked, btn = btnlist[a%24] : getbarcode(btn))
                    else:  #or as administrator buttonnumber and barcode linked
                        aBtn.clicked.connect(lambda checked, btnnr = btnlist[a%24] : getbuttonnr(btnnr))
                                            
                    a += 1
            
            btngroup = 1     # start with buttongroup 1
            btngroupChange(btngroup)
                                                     
            def getbarcode(btn):
                self.q1Edit.setText(btn)   #set choosen barcode to variable and add return
                if sys.platform == 'win32':
                    import keyboard
                    keyboard.write('\n')                          #Windows
                else:
                    subprocess.call(["xdotool", "key", "Return"]) #Linux
                    
            def getbuttonnr(btn):
                mflag = 1
                articleRequest(mflag, btn)
                                
            self.plusminBtn = QPushButton('+')
            self.plusminBtn.setCheckable(True)
            self.plusminBtn.setFont(QFont("Arial", 12,75))
            self.plusminBtn.setStyleSheet("color: black;  background-color: #FFD700")
            self.plusminBtn.setHidden(True)
            self.plusminBtn.clicked.connect(lambda: plusminChange(self))
            self.plusminBtn.setFocusPolicy(Qt.NoFocus)
            self.plusminBtn.setFixedSize(30, 30)
                 
            grid.addWidget(self.plusminBtn, 7, 7, 1, 2)
            
            self.printBtn = QPushButton('Printing')
            self.printBtn.clicked.connect(lambda: printBon(self))
            self.printBtn.setFont(QFont("Arial",12))
            self.printBtn.setFocusPolicy(Qt.NoFocus)
            self.printBtn.setFixedSize(150,140)
            self.printBtn.setStyleSheet("color: black;  background-color: #00FFFF")
      
            grid.addWidget(self.printBtn, 6, 10, 4, 1, Qt.AlignTop)
            
            self.adminBtn = QPushButton('Administration')
            self.adminBtn.setFocusPolicy(Qt.NoFocus)
            self.adminBtn.setHidden(True)
            self.adminBtn.setFont(QFont("Arial",12))
            self.adminBtn.setFixedSize(150, 40) 
            self.adminBtn.setStyleSheet("color: black; background-color: #FFD700")
            self.adminBtn.clicked.connect(lambda: adminMenu()) 
    
            grid.addWidget(self.adminBtn, 7, 7, 1, 3, Qt.AlignBottom | Qt.AlignRight)
                                                   
            self.closeBtn = QPushButton('Exit')
            self.closeBtn.clicked.connect(lambda: windowClose(self))
            self.closeBtn.setFont(QFont("Arial",12))
            self.closeBtn.setFocusPolicy(Qt.NoFocus)
            self.closeBtn.setFixedSize(150,128)
            self.closeBtn.setStyleSheet("color: black; background-color:   #45b39d")

            grid.addWidget(self.closeBtn, 0, 10, 4, 1, Qt.AlignTop)
                                  
            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())
            infoBtn.setFont(QFont("Arial",12))
            infoBtn.setFocusPolicy(Qt.NoFocus)
            infoBtn.setFixedSize(150,140)
            infoBtn.setStyleSheet("color: black;  background-color: #00BFFF")
    
            grid.addWidget(infoBtn, 2, 10, 4, 1, Qt.AlignBottom)
           
            self.nextBtn = QPushButton('Next\nCustomer')
            self.nextBtn.clicked.connect(lambda: nextClient(self))
            self.nextBtn.setFont(QFont("Arial",12))
            self.nextBtn.setFocusPolicy(Qt.NoFocus)
            self.nextBtn.setFixedSize(150,140)            
            self.nextBtn.setStyleSheet("color:black; background-color: #3498db")
    
            grid.addWidget(self.nextBtn, 8, 10)   
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            lbl3.setFixedHeight(40)
            grid.addWidget(lbl3, 11, 0, 1, 11, Qt.AlignCenter)
                                      
            self.setLayout(grid)
            self.setGeometry(300, 60, 600, 300)
            
    window = widget()
    window.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    if sys.platform == "linux":
        os.system("../.usbkbd.sh")
    barcodeScan()
    app.exec_()
    
    