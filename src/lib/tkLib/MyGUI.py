from logs import logDecorator as lD
import json, os

import tkinter as tk
from tkinter import filedialog

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.tkLib.MyGUI'

class MyGUI:

    def __init__(self):


        self.root = tk.Tk()

        # Input for the folder
        #----------------------------
        self.folderName = tk.StringVar()
        self.folderName.set("Name of the folder")

        self.folderFrame = tk.Frame(self.root)
        self.folderFrame.pack( side=tk.TOP, expand=True  )
        self.folderLabel = tk.Label(self.folderFrame, text='Folder', width=10);                self.folderLabel.pack( side = tk.LEFT )
        self.folderInput = tk.Entry(self.folderFrame, textvariable=self.folderName, width=50); self.folderInput.pack( side = tk.LEFT )
        self.folderButton = tk.Button(self.folderFrame, text='...', command=self.getFolder);   self.folderButton.pack( side = tk.LEFT )

        # Get the example fileName
        #----------------------------
        self.fileName = tk.StringVar()
        self.fileName.set("Name of the example file")

        self.fileFrame = tk.Frame(self.root)
        self.fileFrame.pack( side=tk.TOP, expand=True, fill=tk.X )
        self.fileLabel  = tk.Label(self.fileFrame, text='Example File', width=10);        self.fileLabel.pack( side = tk.LEFT )
        self.fileInput  = tk.Entry(self.fileFrame, textvariable=self.fileName, width=50); self.fileInput.pack( side = tk.LEFT )
        self.fileButton = tk.Button(self.fileFrame, text='...', command=self.getFile);    self.fileButton.pack( side = tk.LEFT )

        # This is the quit frame 
        #----------------------------
        self.quitFrame = tk.Frame(self.root)
        self.quitFrame.pack( side=tk.TOP, expand=True, fill=tk.X )
        self.quitButton = tk.Button(self.quitFrame, text = 'Quit', command=self.root.quit)
        self.quitButton.pack( side = tk.LEFT, expand = True, fill = tk.X )
        
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
            self.fileName.set( fileName )
        except Exception as e:
            logger.error('Unable to set the folder Name ...: {e}')

        return fileName

