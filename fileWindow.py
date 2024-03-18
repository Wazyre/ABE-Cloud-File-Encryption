"""
fileWindow.py shows the current contents of the logged in S3 bucket and
allows the user to download existing files or upload new ones. Uploaded
files are first encrypted in [] before being sent to S3.
"""

import os
from PyQt5.QtWidgets import *
import boto3
from dotenv import load_dotenv
import LWKPABE
from charm.toolbox.pairinggroup import PairingGroup

load_dotenv()

# S3 resource init
S3 = boto3.resource('s3',
         aws_access_key_id=os.environ.get("ACCESS_ID"),
         aws_secret_access_key= os.environ.get("ACCESS_KEY"))
BUCKET = S3.Bucket('abeencryption')
BUCKET_OBJECTS = []

# Window size
H = 600
W = 900

# ABE algorithm
ABE = LWKPABE.EKPabe(PairingGroup('MNT224'))
(PK, MK) = ()
KEY = {}
POLICY = ""

for obj in BUCKET.objects.all():
    BUCKET_OBJECTS.append({'key': obj.key, 'lmod': obj.last_modified})

class FileWindow(QMainWindow):
    """
    Window for S3 bucket contents, downloading, and uploading files
    """
    def __init__(self, user) -> None:
        super().__init__()
        self.attr = user[3:7]
        self.setupABE()

        # Qt components
        frm = QFrame()
        frm.setFrameShape(6)
        frm.setFrameShadow(10)
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(len(BUCKET_OBJECTS))
        table.setHorizontalHeaderLabels(['Name', 'Last Modified', ''])
    
        # Populate table with S3 bucket objects
        for row in range(table.rowCount()):
            keyItem = BUCKET_OBJECTS[row]['key']
            lmodItem = QTableWidgetItem(BUCKET_OBJECTS[row]['lmod'])
            table.setItem(row, 0, keyItem)
            table.setItem(row, 1, lmodItem)

            downloadBtn = QPushButton('Download')
            downloadBtn.clicked.connect(lambda: self.downloadFile(BUCKET_OBJECTS[row]['key']))
        
            table.setCellWidget(row, 2, downloadBtn)

        table.setSortingEnabled(True)

        uploadBtn = QPushButton('Upload New File')
        uploadBtn.clicked.connect(self.uploadFile)

        layout.addWidget(table)
        layout.addWidget(uploadBtn)
        frm.setLayout(layout)

        self.setCentralWidget(frm)
        self.resize(W, H)

    def setupABE(self) -> None:
        (PK, MK) = ABE.setup(self.attr)
        KEY = ABE.keygen(PK, MK, POLICY)

    def downloadFile(self, key) -> None:
        '''
        Handles downloading files selected in table
        '''
        # Use OS download manager to find location
        filePath = QFileDialog.getSaveFileName(None, 'Download', None)
        BUCKET.download_file(key, filePath)

        dFile = ABE.decrypt(filePath, KEY)

    def uploadFile(self) -> None:
        '''
        Handles uploading files and sends selected file to be
        encrypted.
        '''
        filePath = QFileDialog.getOpenFileName(None, 'Upload File', None)
        
        eFile = ABE.encrypt(PK, filePath, self.attr)

        fileName = filePath.split('/')
        BUCKET.put_object(eFile, fileName[-1])

# Comment if not debugging
# app = QApplication([])
# win = FileWindow()
# win.show()
# app.exec()
