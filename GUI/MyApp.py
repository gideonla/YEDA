# MyApp.py
# D. Thiebaut
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from GUI_params import Ui_Form
import sys
from model import *
import magic
from error_handling import *
import sys
sys.path.insert(0, "../")
from EmailSender2 import *


class Ui_FormClass(Ui_Form):
    def __init__(self):
        '''Initialize the super class
        '''
        super().__init__()
        self.model = Model()


    def setupUi(self, MW):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi(MW)

    def refreshAll(self):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.CurrentList_3.setText(self.model.getFileName())
    # slot
    def returnPressedSlot(self):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        print("RETURN key pressed in LineEdit widget")

    # slot
    def writeDocSlot(self):
        ''' Called when the user presses the Write-Doc button.
        '''
        print("Write-Doc button pressed")

    # slot
    def load_email_template(self):
        '''
        Called when the user presses the Browse button
        '''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        if not ('text' in magic.from_file(fileName, mime=True)):
            text_file_error(fileName)
        else:
            self.model.setFileName( fileName )
            self.refreshAll()

    def load_email_template(self):
        '''
        Called when the user presses the email template browse button
        '''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        if fileName=="":
            return
        if not ('text' in magic.from_file(fileName, mime=True)):
            text_file_error(fileName)
        else:
            self.model.setTemplateFileName( fileName )
            self.CurrentList_3.setText(self.model.getTemplateFileName())

    def load_email_private_template(self):
        '''
        Called when the user presses the email template browse button
        '''
        # self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;Python Files (*.py)",
            options=options)
        if fileName=="":
            return
        if not ('text' in magic.from_file(fileName, mime=True)):
            text_file_error(fileName)
        else:
            self.model.setPrivateFileName(fileName)
            self.CurrentList_4.setText(self.model.getPrivateFileName())

    def load_attachments(self):
        '''
                Called when the user presses the email template browse button
                '''
        # self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*);;Python Files (*.py)",
            options=options)
        print (fileName)
        if fileName == "":
            return
        else:
            self.model.setPrivateFileName(fileName)
            self.CurrentList_4.setText(self.model.getPrivateFileName())

    def submit_form(self):
        Email_sender(self.MasterList.text(),self.CurrentList.text(), self.PiName.text(), self.Desc.text(), self.model.getTemplateFileName(),
                     self.model.getPrivateFileName(), self.cc.text(), self.bcc.text(), self.email_subject.text(), self.loadattachments)

def main():
    """
    This is the MAIN ENTRY POINT of our application.
    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_FormClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


main()