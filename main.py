from PyQt5.QtWidgets import *
from loginWindow import LoginWindow

def main():
    app = QApplication([])
    win = LoginWindow()
    win.show()
    app.exec()  


if __name__ == "__main__":
    main()