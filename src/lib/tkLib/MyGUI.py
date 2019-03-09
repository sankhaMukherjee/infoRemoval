from logs import logDecorator as lD
import json, os

import tkinter as tk
from tkinter import filedialog

from lib.dicomIO import dicomIO

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.tkLib.MyGUI'


class MyGUI:

    def __init__(self):


        self.root = tk.Tk()

        self.redactionList = []
        self.allowSelection = False

        # Input for the folder
        #----------------------------
        self.folderName = tk.StringVar()
        self.folderName.set("Name of the folder")

        self.folderFrame = tk.Frame(self.root)
        self.folderFrame.pack( side=tk.TOP, fill=tk.X  )
        self.folderLabel = tk.Label(self.folderFrame, text='Folder', width=10);                self.folderLabel.pack( side = tk.LEFT )
        self.folderInput = tk.Entry(self.folderFrame, textvariable=self.folderName, width=50); self.folderInput.pack( side = tk.LEFT, expand=True, fill=tk.X )
        self.folderButton = tk.Button(self.folderFrame, text='...', command=self.getFolder);   self.folderButton.pack( side = tk.LEFT )

        # Get the example fileName
        #----------------------------
        self.fileName = tk.StringVar()
        self.fileName.set("Name of the example file")

        self.fileFrame = tk.Frame(self.root)
        self.fileFrame.pack( side=tk.TOP, fill=tk.X )
        self.fileLabel  = tk.Label(self.fileFrame, text='Example File', width=10);        self.fileLabel.pack( side = tk.LEFT )
        self.fileInput  = tk.Entry(self.fileFrame, textvariable=self.fileName, width=50); self.fileInput.pack( side = tk.LEFT, expand=True, fill=tk.X )
        self.fileButton = tk.Button(self.fileFrame, text='...', command=self.getFile);    self.fileButton.pack( side = tk.LEFT )

        # This is the quit frame 
        #----------------------------
        self.miscButtonsFrame = tk.Frame(self.root)
        self.miscButtonsFrame.pack( side=tk.TOP, fill=tk.X )
        self.loadButton = tk.Button(self.miscButtonsFrame, text = 'load DICOM File', command=self.loadDicomFeatures)
        self.loadButton.pack( side = tk.LEFT)
        self.getSelectionButton = tk.Button(self.miscButtonsFrame, text = 'get Redaction List', command=self.__getSelected__)
        self.getSelectionButton.pack( side = tk.LEFT)

        self.__activateLoad__()

        # This is the status message frame
        #----------------------------------
        # self.statusMessage = tk.StringVar()
        # self.statusMessage.set( 'STATUS: Ok' )
        self.statusLabel = tk.Label(self.root, text='STATUS: Ok')
        self.statusLabel.pack( side = tk.TOP, fill=tk.X )


        # This is the quit frame 
        #----------------------------
        self.quitFrame = tk.Frame(self.root)
        self.quitFrame.pack( side=tk.TOP, fill=tk.X )
        self.quitButton = tk.Button(self.quitFrame, text = 'Quit', command=self.root.quit)
        self.quitButton.pack( side = tk.LEFT, expand = True, fill = tk.X )


        # This is the quit frame 
        #----------------------------
        self.infoFrame = tk.Frame(self.root)
        self.infoFrame.pack( side=tk.TOP, expand=True, fill=tk.BOTH )

        self.metaList = tk.Listbox(self.infoFrame, selectmode=tk.MULTIPLE)
        self.metaList.pack( side=tk.LEFT, expand=True, fill=tk.BOTH )

        self.metaData = {f'a_{i}':f'{i}' for i in range(10)}
        self.__updateMetaData__( self.metaData )

        
        
        return

    def mainloop(self):
        self.root.mainloop()
        return

    @lD.log( logBase + '.getFolder' )
    def getFolder(logger, self):

        try:
            folderName = filedialog.askdirectory(initialdir = os.getcwd())
            print(f'Folder Name obtained: {folderName}')
            self.folderName.set( folderName )
        except Exception as e:
            logger.error('Unable to set the folder Name ...: {e}')

        return folderName

    @lD.log( logBase + '.getFile' )
    def getFile(logger, self):

        try:
            fileName = filedialog.askopenfilename(initialdir = os.getcwd())
            print(f'Folder Name obtained: {fileName}')

            if os.path.exists(fileName):
                self.statusLabel['text'] = f'STATUS: [OK] - A proper filename obtained: {fileName}'
                self.fileName.set( fileName )
        except Exception as e:
            self.statusLabel['text'] = f'STATUS: [ERROR] - Not a proper file: {fileName}'
            logger.error('Unable to set the folder Name ...: {e}')

        return fileName

    @lD.log( logBase + '.getFile' )
    def loadDicomFeatures(logger, self):
        '''[summary]
        
        [description]
        
        Parameters
        ----------
        logger : {[type]}
            [description]
        self : {[type]}
            [description]
        '''


        try:

            fileName = self.fileName.get()
            if not os.path.exists(fileName):
                self.statusLabel['text'] = 'STATUS: [ERROR] - File not found ...'

            metaData = dicomIO.readFileMetaData( fileName )
            print(metaData)
            if metaData == {}:
                self.statusLabel['text'] = 'STATUS: [ERROR] - Probably not a good DICOM file ...'
                self.allowSelection = False
                self.__activateLoad__()
                return

            self.statusLabel['text'] = f'STATUS: [OK] - DICOM file {fileName} loaded'

            # Update the metadata and allow selection
            self.metaData = metaData
            self.__updateMetaData__( metaData )
            
            self.allowSelection = True
            self.__activateLoad__()
            

        except Exception as e:
            logger.error(f'Unable to load the DICOM file: {e}')
            self.statusLabel['text'] = f'STATUS: [ERROR] - Unable to load the dicom file: {e}'

    @lD.log( logBase + '.__updateMetaData__' )
    def __updateMetaData__(logger, self, metaData):

        try:
            self.metaList.delete(0, tk.END)
            for k, v in metaData.items():
                t = f'[{k.rjust(30)}] -> [{v[:30].ljust(30)}]'
                self.metaList.insert(tk.END, t)
        except Exception as e:
            self.statusLabel['text'] = f'STATUS: [ERROR] - Unable to update metadata: {e}'
            logger.error(f'Unable to update the maetData: {e}')

        return

    @lD.log( logBase + '.__getSelected__' )
    def __getSelected__(logger, self):

        try:
            selected = [self.metaList.get(idx) for idx in self.metaList.curselection()]
            selected = [s[1:].split(']')[0].strip()  for s in selected]
            print(selected)
        except Exception as e:
            self.statusLabel['text'] = f'STATUS: [ERROR] - Unable to get fields: {e}'
            logger.error(f'Unable to obtain selected fields: {e}')

        return

    @lD.log( logBase + '.__activateLoad__' )
    def __activateLoad__(logger, self):
        '''[summary]
        
        [description]
        
        Parameters
        ----------
        logger : {[type]}
            [description]
        self : {[type]}
            [description]
        '''

        if self.allowSelection:
            self.getSelectionButton['state'] = tk.NORMAL
        else:
            self.getSelectionButton['state'] = tk.DISABLED

        return


