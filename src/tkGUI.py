import json, argparse

import tkinter as tk

from importlib      import util
from logs           import logDecorator  as lD
from lib.testLib    import simpleLib     as sL
from lib.argParsers import addAllParsers as aP

config   = json.load(open('../config/config.json'))
logBase  = config['logging']['logBase']
logLevel = config['logging']['level']
logSpecs = config['logging']['specs']

def main(logger, resultsDict):
    '''main program
    
    This is the place where the entire program is going
    to be generated.
    '''

    root = tk.Tk()
    logo = tk.PhotoImage(file="../data/img/python_logo_small.gif")

    w1 = tk.Label(root, image=logo).pack(side="right")

    explanation = """At present, only GIF and PPM/PGM
    formats are supported, but an interface 
    exists to allow additional image file
    formats to be added easily."""

    w2 = tk.Label(root, 
                  justify=tk.LEFT,
                  padx = 10, 
                  text=explanation).pack(side="left")
    root.mainloop()


    return

if __name__ == '__main__':

    # Let us add an argument parser here
    parser = argparse.ArgumentParser(description='infoRemoval command line arguments')
    parser = aP.parsersAdd(parser)
    results = parser.parse_args()
    resultsDict = aP.decodeParsers(results)

    # ---------------------------------------------------
    # We need to explicitely define the logging here
    # rather than as a decorator, bacause we have
    # fundamentally changed the way in which logging 
    # is done here
    # ---------------------------------------------------
    logSpecs = aP.updateArgs(logSpecs, resultsDict['config']['logging']['specs'])
    try:
        logLevel = resultsDict['config']['logging']['level']
    except Exception as e:
        print('Logging level taking from the config file: {}'.format(logLevel))

    logInit  = lD.logInit(logBase, logLevel, logSpecs)
    main     = logInit(main)

    main(resultsDict)