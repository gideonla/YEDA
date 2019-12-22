import PyQt5
from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

def text_file_error(fname:str):
    m = QtWidgets.QMessageBox()
    m.setText("File is not a text file\n" + fname)
    m.setIcon(QtWidgets.QMessageBox.Critical)
    m.setStandardButtons(QtWidgets.QMessageBox.Ok)

def file_not_found(fname:str):
    m = QtWidgets.QMessageBox()
    m.setText("File not found\n" + fname)
    m.setIcon(QtWidgets.QMessageBox.Critical)
    m.setStandardButtons(QtWidgets.QMessageBox.Ok)


def debug_trace():
  '''Set a tracepoint in the Python debugger that works with Qt'''
  from PyQt5.QtCore import pyqtRemoveInputHook

  # Or for Qt5
  #from PyQt5.QtCore import pyqtRemoveInputHook

  from pdb import set_trace
  pyqtRemoveInputHook()
  set_trace()
