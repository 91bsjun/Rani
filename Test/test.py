import sys
import PyQt5.sip
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 500)
        self.setWindowTitle("by bjun")

        self.pushButton = QPushButton("File Open")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText("Loaded file: " + fname[0])
        lines = open(fname[0], "r").readlines()
        x = []
        y = []
        for i, l in enumerate(lines):
            if i >= 1:
                x.append(float(l.split(",")[0]))
                y.append(float(l.split(",")[1]))
        plt.plot(x, y, marker='o')
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
