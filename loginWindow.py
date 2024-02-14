"""
File loginWindow.py handles all related jobs to login and will pass 
process to fileWindow.py if user is validated 
"""
from PyQt5.QtWidgets import *
from mysql.connector import connect, Error, MySQLConnection
import dbCredentials
from fileWindow import FileWindow

# Window size
H = 600
W = 900

class LoginWindow(QMainWindow):
    """
    Window for logging in and validating user info
    """
    def __init__(self) -> None:
        super().__init__()
        
        connectDB = self.setupDB()

        # Qt components
        frm = QFrame()
        frm.setFrameShape(6)
        frm.setFrameShadow(10)
        layout = QFormLayout()

        userField = QLineEdit()
        userField.setPlaceholderText('johnsmith@example.com')

        passField = QLineEdit()
        passField.setEchoMode(2)
        submitBtn = QPushButton('Submit')
        submitBtn.clicked.connect(lambda: self.validate(connectDB, userField.text, passField.text))

        layout.addRow('Username:', userField)
        layout.addRow('Password:', passField)
        layout.addWidget(submitBtn)
        frm.setLayout(layout)

        self.setCentralWidget(frm)
        self.resize(W, H)

    def setupDB(self) -> MySQLConnection:
        '''
        Setups the mysql database and handles connection errors. Look
        at dbCredentials.py to change database credentials
        '''
        try:
            db = connect(
                host=dbCredentials.host,
                user=dbCredentials.username,
                password=dbCredentials.password,
                database=dbCredentials.db
            )

            return db
        except Error as e:
            print(e)

    def validate(self, connectDB, username, password) -> None:
        '''
        Validates login information and returns whether credentials
        match the database
        '''
        query = "SELECT * FROM " + dbCredentials.db + " WHERE username=" + username + " && password=" + password
        
        with connectDB.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        if result.length == 0:
            pass # Add warning login failed
        
        else: # Turn over to S3 bucket screen
            connectDB.close()
            self.close()
            win = FileWindow()
            win.show()

# Comment if not debugging
# app = QApplication([])
# win = LoginWindow()
# win.show()
# app.exec()