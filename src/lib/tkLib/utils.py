from logs import logDecorator as lD
import json, os

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.tkLib.utils'

@lD.log(logBase + '.initializeVars')
def initializeVars(logger):
    '''[summary]
    
    [description]
    
    Parameters
    ----------
    logger : {[type]}
        [description]
    '''

    results = {}
    results['folder'] = os.getcwd()

    return results

