from error_handling import *


class Model:
    def __init__(self):
        '''
        Initializes the two members the class holds:
        the file name and its contents.
        '''
        self.EmailTemplate_fname = None
        self.PrivateEmailTemplate_fname = None
        self.attachments=[]
        self.fileContent = ""

    def isValid(self, fileName):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try:
            file = open(fileName, 'r')
            file.close()
            return True
        except:
            return False

    def setTemplateFileName(self, fileName):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid(fileName):
            self.EmailTemplate_fname = fileName
            try:
                self.fileContents = open(fileName, 'r').read()
            except UnicodeDecodeError:
                self.fileContents = ""
                self.EmailTemplate_fname = ""
                text_file_error(fileName)
        else:
            self.fileContents = ""
            self.EmailTemplate_fname = ""

    def setPrivateFileName(self, fileName):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid(fileName):
            self.PrivateEmailTemplate_fname = fileName
            try:
                self.fileContents = open(fileName, 'r').read()
            except UnicodeDecodeError:
                self.fileContents = ""
                self.PrivateEmailTemplate_fname = ""
                text_file_error(fileName)
        else:
            self.fileContents = ""
            self.PrivateEmailTemplate_fname = ""

    def setattachments(self, fnames):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        for i in fnames:
            if not self.isValid(i):
                file_not_found(i)
        self.attachments = fnames

    def getTemplateFileName(self):
        '''
        Returns the name of the file name member.
        '''
        return self.EmailTemplate_fname

    def getPrivateFileName(self):
        '''
        Returns the name of the file name member.
        '''
        return self.PrivateEmailTemplate_fname

    def getFileContents(self):
        '''
        Returns the contents of the file if it exists, otherwise
        returns an empty string.
        '''
        return self.fileContents

    def writeDoc(self, text):
        '''
        Writes the string that is passed as argument to a
        a text file with name equal to the name of the file
        that was read, plus the suffix ".bak"
        '''
        if self.isValid(self.EmailTemplate_fname):
            fileName = self.EmailTemplate_fname + ".bak"
            file = open(fileName, 'w')
            file.write(text)
            file.close()