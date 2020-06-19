import datetime
import sys, random, barcode
import keyboard
from barcode.writer import ImageWriter 

from PyQt5.QtCore import Qt, QSize, QRegExp, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie, QRegExpValidator, QColor, QImage
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QDialog, QLabel, QPushButton,\
        QMessageBox, QSpinBox, QComboBox, QTextEdit, QApplication, QWidget,\
        QVBoxLayout, QTableView, QStyledItemDelegate, QCheckBox
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, create_engine,\
                     Float, select, update,insert, delete, func, and_, ForeignKey

def paySuccess():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Payment succeeded!')
    msg.setWindowTitle('Payments instances')
    msg.exec_() 
 
def alertText():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Buttontext to long, no records inserted!')
    msg.setWindowTitle('Transactions')
    msg.exec_() 

def noData():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('There are no transactions yet!')
    msg.setWindowTitle('Transactions')
    msg.exec_() 
    
def insertOK():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Insert succeeded!')
    msg.setWindowTitle('Insert records')
    msg.exec_()
    
def notInserted():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg'))
    msg.setFont(QFont("Arial", 10))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Not all fields are filled in!')
    msg.setWindowTitle('Insert records')
    msg.exec_() 
            
def windowClose(self):
    self.close()
    sys.exit()
    
def refresh(self):
    self.close()
    defParams(self)
  
def artRequest(self, mflag):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
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
     
    selarticles = select([articles]).order_by(articles.c.barcode)
    rparticles = con.execute(selarticles)
            
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Artikelen opvragen')
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
            table_view.setItemDelegateForColumn(9, showImage(self))
            table_view.setColumnWidth(9, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            if mflag:
                table_view.clicked.connect(defineButton)
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
                                       
    header = ['Barcode','Description', 'Item-Price', 'Item-Stock', 'Item-Unit',\
          'Mininum-Stock', 'Order-Size', 'Location', 'Article_Group', 'Thumbnail',\
          'Category', 'Order-Balance', 'Order-Status' ,'Mutation-Date', \
          'Annual-Consumption_1','Annual-Consumption_2', 'VAT']    
        
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
                Column('buttontext', String))
            
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
                    grid.addWidget(pyqt, 0 ,0, 1, 2)
               
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
                    self.q2Edit = QLineEdit('0')
                    self.q2Edit.setFixedWidth(40)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[123]{1}[0-9]{0,1}$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    #button-text
                    self.q3Edit = QTextEdit()
                    self.q3Edit.setFixedSize(200,40)
                    self.q3Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.q3Edit.setFont(QFont("Arial",10))
                    self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                          
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    lbl1 = QLabel('Barcodenummer')
                    lbl1.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(self.q1Edit, 1, 1)
                     
                    lbl2 = QLabel('Button-Number')
                    lbl2.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl2, 2, 0)
                    grid.addWidget(self.q2Edit, 2, 1)
                    
                    lbl3 = QLabel('Button-Text')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 3, 0)
                    grid.addWidget(self.q3Edit, 3, 1)
                    
                    applyBtn = QPushButton('Insert')
                    applyBtn.clicked.connect(lambda: insBtnText())
                       
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                        
                    grid.addWidget(applyBtn, 4, 1 , 1, 1, Qt.AlignRight)
                        
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close) 
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
            
                    grid.addWidget(cancelBtn, 4, 0, 1, 2, Qt.AlignCenter)
                    
                    lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
                    lbl3.setFont(QFont("Arial", 10))
                    grid.addWidget(lbl3, 5, 0, 1, 3, Qt.AlignCenter)
                   
                    def insBtnText():
                        mbtnnr = int(self.q2Edit.text())
                        mbtntext = self.q3Edit.toPlainText()
                        if len(mbtntext) > 20:
                            alertText()
                        elif mbtnnr and mbtntext:
                            updbtn = update(buttons).where(buttons.c.buttonID==mbtnnr).\
                             values(barcode=str(mbarcode), buttontext=mbtntext)
                            con.execute(updbtn)
                            insertOK()
                            self.close()
                        else:
                            notInserted()
                            self.close() 
                    
                    self.setLayout(grid)
                    self.setGeometry(600, 200, 150, 100)
    
            window = Widget()
            window.exec_()
    
    win = MyWindow(data_list, header)
    win.exec_()
    
def salesRequest(self):
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
     
    selsales = select([sales]).order_by(sales.c.receiptnumber)
    rpsales = con.execute(selsales)
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
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
               
def paymentsRequest(self):
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
     
    selpay = select([payments]).order_by(payments.c.paydate, payments.c.ovorderID)
    rppay = con.execute(selpay)
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
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
                     
                cBox = QCheckBox()
                cBox.stateChanged.connect(self.cBoxChanged)
                cBox.setStyleSheet('color: black; background-color: #F8F7EE')
                grid.addWidget(cBox, 6, 1)
                if len(rpp[4])==10:
                    lbl7 = QLabel('Payed')
                    lbl7.setFont(QFont("Arial",10))
                    grid.addWidget(lbl7, 6, 0, 1, 1, Qt.AlignRight)
                    cBox.setStyleSheet('color: black')
                    cBox.setEnabled(False)
                                                                   
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
                payBtn.clicked.connect(self.accept)
        
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
                
            state = False  
            def cBoxChanged(self, state):
                if state == Qt.Checked:
                    self.state = True
                        
            def returncBox(self):
                return self.state
                       
            @staticmethod
            def getData(parent=None):
                dialog = MainWindow()
                dialog.exec_()
                return [dialog.returncBox()] 
                                           
        mainwin = MainWindow()
        data = mainwin.getData()
                 
        if data[0]:
            mstatus = True
        else:
            return
        if mstatus:
            mpaydate = str(datetime.datetime.now())[0:10]
            updpay = update(payments).where(payments.c.payID == mpaynr).\
                values(paydate = mpaydate)
            con.execute(updpay)
            paySuccess()    
                                    
    win = MyWindow(data_list, header)
    win.exec_()
    
def emplAccess(self):
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
        inlogstr = random.randint(1000000, 9999999)
        ean = barcode.get('ean8', str(inlogstr), writer=ImageWriter()) # for barcode as png
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
            
            self.setWindowTitle("Access Employees")
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
            reg_ex = QRegExp("^[123]{1}$")
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
                    insertOK()
                    self.close()
                else:
                    notInserted()
                    self.close() 
           
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)
            
    window = Widget()
    window.exec_()
    
def newBarcode(self):
    metadata = MetaData()
    articles = Table('articles', metadata,
        Column('barcode', String, primary_key=True),
        Column('description', String),
        Column('item_price', Float),
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
    buttons = Table('buttons', metadata,
        Column('buttonID', Integer, primary_key=True),
        Column('buttontext', String),
        Column('barcode', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
    mbarcode=(con.execute(select([func.max(articles.c.barcode, type_=String)])).scalar())
    # generate new barcode
    marticlenr = mbarcode[3:11]
    marticlenr = str((int(marticlenr[0:8]))+int(1))
    total = 0
    for i in range(int(8)):
        total += int(marticlenr[i])*(int(9)-i)
    checkdigit = total % 11 % 10
    marticlenr = marticlenr+str(checkdigit)
    ean = barcode.get('ean13','800'+str(marticlenr), writer=ImageWriter()) # for barcode as png
    mbarcode = ean.get_fullcode()
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
            grid.addWidget(pyqt, 0 ,0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 2, 1 ,1, Qt.AlignRight)
            
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
            
            #item_price
            self.q3Edit = QLineEdit('0')
            self.q3Edit.setFixedWidth(100)
            self.q3Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q3Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
            input_validator = QRegExpValidator(reg_ex, self.q3Edit)
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
            self.q11Edit.addItem('1. Stock-driven < 3 weken.')
            self.q11Edit.addItem('2. Stock-driven < 6 weken')
            self.q11Edit.addItem('3. Stock-driven < 12 weken')
            self.q11Edit.addItem('4. Stock-driven < 26 weken')
            self.q11Edit.addItem('5. Stock-driven < 52 weken')
 
            #vat
            self.q12Edit = QComboBox()
            self.q12Edit.setFixedWidth(100)
            self.q12Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q12Edit.setFont(QFont("Arial",10))
            self.q12Edit.addItem('high')
            self.q12Edit.addItem('low')
                        
            #button-number
            self.q13Edit = QLineEdit('0')
            self.q13Edit.setFixedWidth(40)
            self.q13Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.q13Edit.setFont(QFont("Arial",10))
            reg_ex = QRegExp("^[123]{1}[0-9]{0,1}$")
            input_validator = QRegExpValidator(reg_ex, self.q13Edit)
            self.q13Edit.setValidator(input_validator)
            
            #button-text
            self.q14Edit = QTextEdit()
            self.q14Edit.setFixedSize(200,40)
            self.q14Edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.q14Edit.setFont(QFont("Arial",10))
            self.q14Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                 
            def q2Changed():
                self.q2Edit.setText(self.q2Edit.text())
            self.q2Edit.textChanged.connect(q2Changed)
            
            def q3Changed():
                self.q3Edit.setText(self.q3Edit.text())
            self.q3Edit.textChanged.connect(q3Changed)
            
            def q5Changed():
                self.q5Edit.setCurrentText(self.q5Edit.currentText())
            self.q5Edit.currentIndexChanged.connect(q5Changed)
            
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
                self.q12Edit.setCurrentText(self.q12Edit.currentText())
            self.q12Edit.currentIndexChanged.connect(q12Changed)
            
            def q13Changed():
                self.q13Edit.setText(self.q13Edit.text())
            self.q13Edit.textChanged.connect(q13Changed)
                         
            lbl1 = QLabel('Barcode')
            lbl1.setFont(QFont("Arial", 10))
            grid.addWidget(lbl1, 3, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q1Edit, 3, 1)
                      
            lbl2 = QLabel('Description')
            lbl2.setFont(QFont("Arial", 10))
            grid.addWidget(lbl2, 4, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q2Edit, 4, 1, 1, 3)
            
            lbl3 = QLabel('Item-price')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 5, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q3Edit, 5, 1)
            
            lbl10 = QLabel('Thumbnail')
            lbl10.setFont(QFont("Arial", 10))
            grid.addWidget(lbl10, 5, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q10Edit, 5, 2, 1, 1, Qt.AlignRight)
               
            lbl5 = QLabel('Item-unit')
            lbl5.setFont(QFont("Arial", 10))
            grid.addWidget(lbl5, 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q5Edit, 6, 1)
               
            lbl7 = QLabel('Order-size')
            lbl7.setFont(QFont("Arial", 10))
            grid.addWidget(lbl7, 7, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q7Edit, 7, 1)
            
            lbl8 = QLabel('Location')
            lbl8.setFont(QFont("Arial", 10))
            grid.addWidget(lbl8, 7, 0, 1, 2, Qt.AlignRight)
            grid.addWidget(self.q8Edit, 7, 2, 1, 1, Qt.AlignRight)
            
            lbl9 = QLabel('Article-Group')
            lbl9.setFont(QFont("Arial", 10))
            grid.addWidget(lbl9, 8, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q9Edit, 8, 1)   
     
            lbl11 = QLabel('Category')
            lbl11.setFont(QFont("Arial", 10))
            grid.addWidget(lbl11, 9, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q11Edit, 9, 1, 1, 1, Qt.AlignRight)
         
            lbl12 = QLabel('VAT')
            lbl12.setFont(QFont("Arial", 10))
            grid.addWidget(lbl12, 9, 2)
            grid.addWidget(self.q12Edit, 9, 2, 1, 1, Qt.AlignRight)
            
            lbl13 = QLabel('Button-Number')
            lbl13.setFont(QFont("Arial", 10))
            grid.addWidget(lbl13, 10, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q13Edit, 10, 1)
            
            lbl14 = QLabel('Button-Text')
            lbl14.setFont(QFont("Arial", 10))
            grid.addWidget(lbl14, 10, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(self.q14Edit, 10, 2, 1, 1, Qt.AlignRight)
                        
            applyBtn = QPushButton('Insert')
            applyBtn.clicked.connect(lambda: insertart())
               
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
            grid.addWidget(applyBtn, 11, 2, 1, 1, Qt.AlignRight)
                
            cancelBtn = QPushButton('Close')
            cancelBtn.clicked.connect(self.close) 
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black; background-color: gainsboro") 
    
            grid.addWidget(cancelBtn, 11, 1, 1, 3, Qt.AlignCenter)
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 12, 0, 1, 3, Qt.AlignCenter)
          
            def insertart():
                mdescr = self.q2Edit.text()
                mprice = float(self.q3Edit.text())
                munit = self.q5Edit.currentText()
                msize = float(self.q7Edit.text())
                mloc = self.q8Edit.text()
                mgroup = self.q9Edit.text()
                mthumb = self.q10Edit.text()
                mcat = int(self.q11Edit.currentIndex())+1
                mvat = self.q12Edit.currentText()
                mbtnnr = int(self.q13Edit.text())
                mbtntext = self.q14Edit.toPlainText()
                if len(mbtntext) > 20:
                    alertText()
                elif mdescr and mprice and mcat and mbtnnr and mbtntext:
                    insart = insert(articles).values(barcode=str(mbarcode),\
                       description = mdescr,item_price=mprice, item_unit=munit,\
                       order_size=msize,location_warehouse=mloc, article_group=mgroup,\
                       thumbnail=mthumb,category=mcat,VAT=mvat)
                    con.execute(insart)
                    updbtn = update(buttons).where(buttons.c.buttonID==mbtnnr).\
                     values(barcode=str(mbarcode), buttontext=mbtntext)
                    con.execute(updbtn)
                        
                    if sys.platform == 'win32':
                        ean.save('.\\Barcodes\\Articles\\'+str(mbarcode))
                    else:
                        ean.save('./Barcodes/Articles/'+str(mbarcode))
                    insertOK()
                    self.close()
                else:
                    notInserted()
                    self.close() 
            
            self.setLayout(grid)
            self.setGeometry(600, 200, 150, 100)

    win = Widget()
    win.exec_()
    
def existingBarcode(self):
    mflag = 1
    artRequest(self, mflag)
        
def defButtons(self):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Define Buttons")
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
            self.k0Edit.setFixedWidth(220)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('New barcode')
            self.k0Edit.addItem('Existing barcode')
                           
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
                           
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()
                if mindex == 0:
                    newBarcode(self)
                elif mindex == 1:
                    existingBarcode(self)
                                   
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1)
                     
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(600, 400, 150, 100)
                
    window = Widget()
    window.exec_()  
    
def insertArticles(self):
    print('Insering articles')
    
def importArticles(self):
    print('Imports articles')
    
def bookingLoss(self):
    print('Loss products')
    
def purchaseArticles(self):
    print('Purchasing articles')
    
def defParams(self):
    class Widget(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setWindowTitle('Parameters changing')
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
            table_view.clicked.connect(showSelection)
            grid.addWidget(table_view, 0, 0, 1, 7)
            
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 1 , 0 , 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 1, 6, 1 ,1, Qt.AlignRight)
                  
            freshBtn = QPushButton('Verversen')
            freshBtn.clicked.connect(lambda: refresh(self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 5, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 4, 1, 1, Qt.AlignRight | Qt.AlignBottom)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 2, 1, 1, Qt.AlignBottom)
            
            self.setLayout(grid)
            self.setGeometry(300, 50, 900, 900)
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
             
    header = ['ParamID', 'Item', 'Tarief']
    
    metadata = MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer(), primary_key=True),
        Column('item', String),
        Column('value', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
    con = engine.connect()
        
    sel = select([params]).order_by(params.c.paramID)
    
    rp = con.execute(sel)
    
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        paramnr = idx.data()
        if idx.column() == 0: 
            selpar = select([params]).where(params.c.paramID == paramnr)
            rppar = con.execute(selpar).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Changing parameters")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                    
                    self.setStyleSheet("background-color: #D9E1DF")
                    self.setFont(QFont('Arial', 10))  
                    
                    #item
                    self.q1Edit = QLineEdit(rppar[1])
                    self.q1Edit.setCursorPosition(0)
                    self.q1Edit.setFixedWidth(150)
                    self.q1Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q1Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^.{0,20}$")
                    input_validator = QRegExpValidator(reg_ex, self.q1Edit)
                    self.q1Edit.setValidator(input_validator)
                                    
                    #value
                    self.q2Edit = QLineEdit(str(round(float(rppar[2]),2)))
                    self.q2Edit.setFixedWidth(100)
                    self.q2Edit.setAlignment(Qt.AlignRight)
                    self.q2Edit.setStyleSheet('color: black; background-color: #F8F7EE')
                    self.q2Edit.setFont(QFont("Arial",10))
                    reg_ex = QRegExp("^[-+]?[0-9]*\.?[0-9]+$")
                    input_validator = QRegExpValidator(reg_ex, self.q2Edit)
                    self.q2Edit.setValidator(input_validator)
                    
                    def q1Changed():
                        self.q1Edit.setText(self.q1Edit.text())
                    self.q1Edit.textChanged.connect(q1Changed)
                    
                    def q2Changed():
                        self.q2Edit.setText(self.q2Edit.text())
                    self.q2Edit.textChanged.connect(q2Changed)
                    
                    def updparams(self):
                         mitem = self.q1Edit.text()   
                         mvalue = self.q2Edit.text()
                         updpar = update(params).where(params.c.paramID == paramnr).\
                           values(item = mitem, value = float(mvalue))
                         con.execute(updpar)
                         insertOK()
                         self.close()
                                                      
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Parameter')  
                    grid.addWidget(lbl1, 1, 0)
                    lbl2 = QLabel(str(paramnr))
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Item')  
                    grid.addWidget(lbl3, 2, 0)
                    grid.addWidget(self.q1Edit, 2, 1, 1, 2) 
                                                         
                    lbl4 = QLabel('Value')  
                    grid.addWidget(lbl4, 3, 0)
                    grid.addWidget(self.q2Edit, 3, 1)
                    
                    pyqt = QLabel()
                    movie = QMovie('./logos/pyqt.gif')
                    pyqt.setMovie(movie)
                    movie.setScaledSize(QSize(240,80))
                    movie.start()
                    grid.addWidget(pyqt, 0 , 0 , 1, 2)
               
                    logo = QLabel()
                    pixmap = QPixmap('./logos/logo.jpg')
                    logo.setPixmap(pixmap.scaled(70,70))
                    grid.addWidget(logo , 0, 2)
                                                     
                    grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 3, Qt.AlignCenter)                  
                    self.setLayout(grid)
                    self.setGeometry(500, 300, 150, 150)
            
                    applyBtn = QPushButton('Change')
                    applyBtn.clicked.connect(lambda: updparams(self))
            
                    grid.addWidget(applyBtn, 4, 2, 1, 1, Qt.AlignRight)
                    applyBtn.setFont(QFont("Arial",10))
                    applyBtn.setFixedWidth(100)
                    applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
 
                    cancelBtn = QPushButton('Close')
                    cancelBtn.clicked.connect(self.close)
            
                    grid.addWidget(cancelBtn, 4, 1, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                      
            window = MainWindow()
            window.exec_()
            
    win = Widget(data_list, header)
    win.exec_()
    
def adminMenu(self):
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
            self.k0Edit.setFixedWidth(220)
            self.k0Edit.setFont(QFont("Arial",10))
            self.k0Edit.setStyleSheet('color: black; background-color: #F8F7EE')
            self.k0Edit.addItem('Articles request')
            self.k0Edit.addItem('Sales request')
            self.k0Edit.addItem('Payments request/Payments')
            self.k0Edit.addItem('Accounts insert')
            self.k0Edit.addItem('Buttons define')
            self.k0Edit.addItem('Articles insert')
            self.k0Edit.addItem('Articles-list import')
            self.k0Edit.addItem('Write off loss')
            self.k0Edit.addItem('Purchase products')
            self.k0Edit.addItem('Parameters change')
            
            def k0Changed():
                self.k0Edit.setCurrentIndex(self.k0Edit.currentIndex())
            self.k0Edit.currentIndexChanged.connect(k0Changed)
            
            grid.addWidget(self.k0Edit, 1, 1, 1, 2)
            
            def menuChoice(self):
                mindex = self.k0Edit.currentIndex()

                if mindex == 0:
                    mflag = 0
                    artRequest(self, mflag)
                elif mindex == 1:
                    salesRequest(self)                
                elif mindex == 2:
                    paymentsRequest(self)  
                elif mindex == 3:
                    emplAccess(self) 
                elif mindex == 4:
                    defButtons(self)
                elif mindex == 5:
                    insertArticles(self)
                elif mindex == 6:
                    importArticles(self)
                elif mindex == 7:
                    bookingLoss(self)
                elif mindex == 8:
                    purchaseArticles(self)
                elif mindex == 9:
                    defParams(self)
            
            closeBtn = QPushButton('Close')
            closeBtn.clicked.connect(self.close)  
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(closeBtn, 2, 1)
            
            applyBtn = QPushButton('Select')
            applyBtn.clicked.connect(lambda: menuChoice(self))  
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(applyBtn, 2, 2)
                 
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 3, 0, 1, 3, Qt.AlignCenter)
           
            self.setLayout(grid)
            self.setGeometry(600, 400, 150, 100)
                
    window = Widget()
    window.exec_()  
  
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
    self.logonstate.setText(self.mcallname +' logged in.')
    self.plusminBtn.setStyleSheet("color: black;  background-color: gainsboro")
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
            
            infolbl = QLabel('''\t\t\t\t\t\t\t\t\t\t\t
        Instruction barcode scan.
        
        A hand laser scanner of the type Nedis BCRLR100BK was used as test scanner. 
        Logging in takes place with a barcode card with 3 access levels.
        Level 1. Selling, scanning, printing (normal cash register usage).
        Level 2. Return bookings, a checkable ± button is shown, with which return bookings can be made.
        Level 3. Administration, a button Adminstration is shown, for assigning productbuttons,
                 creating accounts, administration, perform stock management and imports.
        Employee first time scan barcode  = logon, second time = logout.
        Other employee scanning = switching employee (for return booking, or replacement).
                         
        Article scanning:
        By default, scanning is performed with an number of 1.
        With the spinbox the correct number can be chosen for scanning, this can be done by the arrows of 
        the spinbox or with the mous wheel. After every scan, the number is reset to 1.
        When scanning is started, the close button is blocked until the button 'Next customer' is pressed.
        The print button and the customer button are blocked until the first transaction is posted.
        In the following cases, an error message appears in red below the display screen. An acoustic alarm 
        will also sound for the following 4 cases.  
        
        1. If a read error occurs when scanning the barcode.
        2. If there is insufficient stock to deliver the order, current stock will also been showed.
        3. If the product is not (yet) included in the range.
        4. If not logged in.
             
        If the item cannot be scanned, it is possible to insert the barcode manually after inserting press 
        <Enter> on the keyboard.
                           
        The receipt can be printed after scanning is finished.
        Before exiting the program, first press the customer button, so the close button is released.
        This will make the necessary bookings and prepare the order for the next customer.
        ''')
            grid.addWidget(infolbl, 1, 0)
                           
            infolbl.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF")   
            grid.addWidget(QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl'), 2, 0, 1, 2, Qt.AlignCenter)
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn, 2, 0, 1, 1,  Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(350, 50, 150, 100)
            
    window = Widget()
    window.exec_()

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setFont(QFont("Arial", 10))
    msg.setText('Just a moment printing is starting!')
    msg.setWindowTitle('Printing receipt')
    msg.exec_()
    
def heading(self, mpage):
    kop=\
    ('Sales - Ordernumber: '+ str(self.mreceipt)+' Date : '+str(datetime.datetime.now())[0:10]+' Pagenumber '+str(mpage)+' \n'+
    '==================================================================================================\n'+
    'Artikelnr  Description                                  Number  Item_price    Subtotal         VAT\n'+
    '==================================================================================================\n')
    return(kop)

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
        mpage = 0
        rgl = 0
        if sys.platform == 'win32':
            fbarc = '.\\forms\\Barcodelists\\'+str(self.mreceipt)+'.txt'
        else:
            fbarc = './forms//Barcodelists/'+str(self.mreceipt)+'.txt'
        
        for row in rpb:
            rgl += 1
            if rgl == 1 :
                mpage += 1
                open(fbarc, 'w').write(heading(self, mpage))
            elif rgl%57 == 1:
                mpage += 1
                open(fbarc, 'a').write(heading(self, mpage))
                
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
         'Employee : '+self.mcallname+' \n')
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
            noData()
    
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
               
        engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
        con = engine.connect()

        self.mreceipt += 1
        updpar = update(params).where(params.c.paramID == 3).values(value = self.mreceipt)
        con.execute(updpar)
        mpaynr = (con.execute(select([func.max(payments.c.payID, type_=Integer)])).scalar())
        mpaynr += 1
        insdr = insert(payments).values(payID = mpaynr, bookdate = mbookd,\
             kind = 'VAT payment    ', amount = self.mtotvat, instance = 'Tax authorities',\
             ovorderID = int(self.mreceipt), accountnumber = 'NL10 ABNA 9999999977')
        con.execute(insdr)
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color: gainsboro")
        self.printBtn.setDisabled(True)
        self.printBtn.setStyleSheet("color: grey; background-color: gainsboro")
        self.nextBtn.setDisabled(True)
        self.nextBtn.setStyleSheet("color: grey; background-color: gainsboro")
        
        self.mtotal = 0.00
        self.mtotvat = 0.00
        self.mlist = []
        self.view.setText('')
        self.qtailtext = 'Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(self.mtotal)+'{:\u2000>12.2f}'.format(self.mtotvat)
        self.qtailEdit.setText(self.qtailtext)
    else:
        noData()
        self.closeBtn.setEnabled(True)
        self.closeBtn.setStyleSheet("color: black; background-color: gainsboro")

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
        
def checkLogoncode(c):
    checksum = int(c[0])+int(c[2])+int(c[4])+int(c[6])+(int(c[1])+
                int(c[3])+int(c[5]))*3
    checkdigit = (10-(checksum%10))%10
    if checkdigit == int(c[7]):
        return True
    else:
        return False
        
def checkBarcode(c):
    checksum = int(c[0])+int(c[2])+int(c[4])+int(c[6])+int(c[8])+int(c[10])+(int(c[1])+
                int(c[3])+int(c[5])+int(c[7])+int(c[9])+int(c[11]))*3
    checkdigit = (10-(checksum%10))%10
    if checkdigit == int(c[12]):
        return True
    else:
        return False
    
def set_barcodenr(self):
    barcodenr = self.q1Edit.text()
    mnumber = self.qspin.value()
    self.albl.setText('')
    if len(barcodenr) == 13 and checkBarcode(barcodenr) and self.mcallname:
        metadata = MetaData()
        articles = Table('articles', metadata,
            Column('barcode', String, primary_key=True),
            Column('description', String),
            Column('item_price', Float),
            Column('item_stock', Float),
            Column('VAT', String))
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
        if rpart[4] == 'high':
            self.mvat = self.mvath
        else: 
            self.mvat = self.mvatl
        if rpart and rpart[3] < mnumber:
            self.albl.setText('Error message: '+str(int(rpart[3]))+' in stock!')
            giveAlarm()
        elif rpart and self.maccess:
            martnr = rpart[0]
            mdescr = rpart[1]
            mdescr = mdescr[:40] if len(mdescr) > 40 else mdescr
            mprice = rpart[2]
            mutdate = str(datetime.datetime.now())[0:10]
            if rpbal:
                updbal = update(sales).where(and_(sales.c.barcode == barcodenr,\
                  sales.c.receiptnumber == self.mreceipt)).values(number = sales.c.number+mnumber,\
                  sub_total = (sales.c.number+mnumber)*mprice,\
                  sub_vat = (sales.c.number+mnumber)*mprice*self.mvat, callname = self.mcallname,\
                  mutation_date = mutdate)
                con.execute(updbal)
            else:
                midnr = (con.execute(select([func.max(sales.c.ID, type_=Integer)])).scalar()) 
                midnr += 1
                insbal = insert(sales).values(ID = midnr, receiptnumber = self.mreceipt,\
                  barcode = barcodenr, description = mdescr, number = mnumber, item_price = mprice,\
                  sub_total = mnumber*mprice, sub_vat = mnumber*mprice*self.mvat,\
                  callname = self.mcallname, mutation_date = mutdate)
                con.execute(insbal)
                
            updart = update(articles).where(articles.c.barcode == rpart[0])\
                .values(item_stock = articles.c.item_stock - float(mnumber))
            con.execute(updart)
            
            self.mlist.append('{:\u2000<14s}'.format(martnr)+'{:\u2000<40s}'.format(mdescr)+' {:\u2000>6d}'\
             .format(int(mnumber))+'{:\u2000>12.2f}'.format(mprice)+'{:\u2000>12.2f}'\
             .format(float(mprice)*float(mnumber))+'{:\u2000>12.2f}'\
             .format(float(mprice)*float(mnumber)*self.mvat))
            self.mtotal += float(mprice)*float(mnumber)
            self.mtotvat += float(mprice)*float(mnumber)*self.mvat
            self.qtailtext = 'Total  incl. VAT'+'\u2000'*57+'{:\u2000>12.2f}'.format(self.mtotal)+'{:\u2000>12.2f}'.format(self.mtotvat)
            self.qtailEdit.setText(self.qtailtext)
            
            self.view.append(self.mlist[-1])
        elif self.maccess == 0:
            self.albl.setText('Errormessage:  Please logon with your barcodecard!')
            giveAlarm() 
        else:
            self.albl.setText('Errormessage:  Article not in assortment!')
            giveAlarm()
                  
        self.closeBtn.setDisabled(True)
        self.closeBtn.setStyleSheet("color: grey; background-color: gainsboro")
        self.printBtn.setEnabled(True)
        self.printBtn.setStyleSheet("color: black; background-color: gainsboro")
        self.nextBtn.setEnabled(True)
        self.nextBtn.setStyleSheet("font: 12pt Arial; color: black; background-color: gainsboro")
    elif len(barcodenr) == 8:
        if barcodenr == self.checknr:
            self.maccess = 0
            self.plusminBtn.setHidden(True)
            self.adminBtn.setHidden(True)
            self.q1Edit.setText('')
            self.logonstate.setText('Logged out')
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
    class widget(QDialog):
        def __init__(self):
            super(widget,self).__init__()
            
            self.setWindowTitle("Sales")
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
                Column('value', Float))
                        
            engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
            con = engine.connect()
            selpar = select([params])
            rppar = con.execute(selpar).fetchall()
            self.mreceipt = int(rppar[2][2])
            self.mvath = rppar[1][2]
            self.mvatl = rppar[0][2]
            self.mcallname = '' 
            self.maccess = 0
            self.checknr = ''
                      
            self.q1Edit = QLineEdit('')
            self.q1Edit.setStyleSheet("color: black;  background-color: #F8F7EE")
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
            
            grid = QGridLayout()
            grid.setSpacing(10)
          
            koplbl = QLabel('Cashregister System')
            koplbl.setStyleSheet("color:rgba(45, 83, 115, 255); font: 30pt Comic Sans MS")
            grid.addWidget(koplbl, 0, 0, 1, 12, Qt.AlignCenter)
        
            pyqt = QLabel()
            movie = QMovie('./logos/pyqt.gif')
            pyqt.setMovie(movie)
            movie.setScaledSize(QSize(240,80))
            movie.start()
            grid.addWidget(pyqt, 0 ,0, 1, 3)
       
            logo = QLabel()
            pixmap = QPixmap('./logos/logo.jpg')
            logo.setPixmap(pixmap.scaled(70,70))
            grid.addWidget(logo , 0, 11, 1 ,1, Qt.AlignRight)
            
            self.logtext = 'Logged out'
            self.logonstate = QLabel(self.logtext)
            self.logonstate.setFont(QFont("Arial", 12))
            grid.addWidget(self.logonstate, 9, 10, 1, 3)
            
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
            self.view.setFixedSize(1110, 450)  
            
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
            
            grid .addWidget(mkop, 2, 0, 1, 12, Qt.AlignCenter)           
            grid.addWidget(self.view, 3 ,0, 1, 12, Qt.AlignCenter)
            grid.addWidget(self.qtailEdit, 4, 0, 1, 12, Qt.AlignCenter)
            
            self.albl = QLabel('')
            self.albl.setStyleSheet("font: bold 18px; color: red")
            grid.addWidget(self.albl, 5, 0, 1, 12, Qt.AlignCenter)

            lbl1 = QLabel('Barcodescan')
            lbl1.setFont(QFont("Arial", 12))
            grid.addWidget(lbl1, 7, 9, 1, 4, Qt.AlignCenter)
            grid.addWidget(self.q1Edit , 7, 2, 1, 11, Qt.AlignRight)
            
            lbl2 = QLabel('      Number')
            lbl2.setFont(QFont("Arial", 12))
            grid.addWidget(lbl2, 8, 9, 1, 4, Qt.AlignCenter)
            grid.addWidget(self.qspin, 8, 11, 1, 1, Qt.AlignRight)
            
            metadata = MetaData()
            params = Table('params', metadata,
                Column('paramID', Integer(), primary_key=True),
                Column('item', String),
                Column('value', Float))
                        
            engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
            con = engine.connect()
            metadata = MetaData()
            buttons = Table('buttons', metadata,
                Column('buttonID', Integer(), primary_key=True),
                Column('buttontext', String),
                Column('barcode',  None, ForeignKey('articles.barcode')))
                                          
            engine = create_engine('postgresql+psycopg2://postgres@localhost/cashregister')
            con = engine.connect()
            selbtn = select([buttons]).order_by(buttons.c.buttonID)
            rpbtn = con.execute(selbtn)
  
            # insert 32 programmable articlebuttons
            btnlist = []
            a = 0
            for row in rpbtn:
                aBtn = QPushButton(row[1].strip())
                btnlist.append(row[2].strip())
                aBtn.setFont(QFont("Times", 8, 75))
                aBtn.setStyleSheet('color: black; background-color: gainsboro')
                aBtn.setFocusPolicy(Qt.NoFocus)
                aBtn.setFixedSize(65, 40)
                if a < 8:
                    grid.addWidget(aBtn, 7, a+1)
                elif a < 16:
                    grid.addWidget(aBtn, 8, a%8+1)
                elif a < 24:
                    grid.addWidget(aBtn, 9, a%8+1)
                elif a < 32:
                    grid.addWidget(aBtn, 10, a%8+1)
                 
                aBtn.clicked.connect(lambda checked, btn = btnlist[a] : getbarcode(btn))
                a += 1
                
            def getbarcode(btn):
                self.q1Edit.setText(btn)
                keyboard.write('\n')
                        
            kassa = QLabel()
            pixmap = QPixmap('./logos/register.png')
            kassa.setPixmap(pixmap.scaled(150, 150))
            grid.addWidget(kassa, 7, 0, 4, 1)
                
            self.plusminBtn = QPushButton('+')
            self.plusminBtn.setCheckable(True)
            self.plusminBtn.setHidden(True)
            self.plusminBtn.setStyleSheet("color: grey;  background-color: gainsboro")
            self.plusminBtn.clicked.connect(lambda: plusminChange(self))
            self.plusminBtn.setFocusPolicy(Qt.NoFocus)
            self.plusminBtn.setFixedSize(20, 30)
            self.plusminBtn.setStyleSheet("color: black;  background-color: gainsboro")
      
            grid.addWidget(self.plusminBtn, 8, 11)
            
            self.printBtn = QPushButton('Printing')
            self.printBtn.clicked.connect(lambda: printBon(self))
            self.printBtn.setFont(QFont("Arial",12))
            self.printBtn.setFocusPolicy(Qt.NoFocus)
            self.printBtn.setFixedWidth(120)
            self.printBtn.setStyleSheet("color: black;  background-color: gainsboro")
      
            grid.addWidget(self.printBtn, 10, 11, 1, 1, Qt.AlignRight)
            
            self.adminBtn = QPushButton('Administration')
            self.adminBtn.setFocusPolicy(Qt.NoFocus)
            self.adminBtn.setHidden(True)
            self.adminBtn.setFont(QFont("Arial",12))
            self.adminBtn.setFixedSize(160, 40) 
            self.adminBtn.setStyleSheet("color: black; background-color: gainsboro")
            self.adminBtn.clicked.connect(lambda: adminMenu(self)) 
    
            grid.addWidget(self.adminBtn, 9, 9, 1, 1, Qt.AlignRight)
                                                   
            self.closeBtn = QPushButton('Exit')
            self.closeBtn.clicked.connect(lambda: windowClose(self))
            self.closeBtn.setFont(QFont("Arial",12))
            self.closeBtn.setFocusPolicy(Qt.NoFocus)
            self.closeBtn.setFixedWidth(120)
            self.closeBtn.setStyleSheet("color: black; background-color: gainsboro")

            grid.addWidget(self.closeBtn, 10, 10, 1, 1, Qt.AlignCenter)
                                  
            infoBtn = QPushButton('Information')
            infoBtn.clicked.connect(lambda: info())
            infoBtn.setFont(QFont("Arial",12))
            infoBtn.setFocusPolicy(Qt.NoFocus)
            infoBtn.setFixedWidth(120)
            infoBtn.setStyleSheet("color: black;  background-color: gainsboro")
    
            grid.addWidget(infoBtn, 10, 9, 1, 1, Qt.AlignRight )
           
            self.nextBtn = QPushButton('Next customer')
            self.nextBtn.clicked.connect(lambda: nextClient(self))
            self.nextBtn.setFont(QFont("Arial",12))
            self.nextBtn.setFocusPolicy(Qt.NoFocus)
            self.nextBtn.setFixedSize(160, 60)            
            self.nextBtn.setStyleSheet("color:black; background-color: gainsboro")
    
            grid.addWidget(self.nextBtn, 8, 9, 1, 1, Qt.AlignRight)   
            
            lbl3 = QLabel('\u00A9 2020 all rights reserved dj.jansen@casema.nl')
            lbl3.setFont(QFont("Arial", 10))
            grid.addWidget(lbl3, 11, 0, 1, 12, Qt.AlignCenter)
                                      
            self.setLayout(grid)
            self.setGeometry(300, 60, 600, 300)
            
    window = widget()
    window.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    barcodeScan()
    app.exec_()
    
    