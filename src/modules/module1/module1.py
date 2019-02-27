from logs import logDecorator as lD 
import json, pprint

from lib.dicomIO import dicomIO

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.module1.module1'


@lD.log(logBase + '.doSomething')
def doSomething(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    try:
        print('---------[Original Data]-----------------------')
        metaData = dicomIO.readFileMetaData('../data/raw_data/c002_250417/DICOM/00000001/00000002/00000016')
        pprint.pprint(metaData)

        print('---------[Redacting ]-----------------------')
        folderName     = '../data/raw_data/c002_250417/DICOM/00000001/00000002'
        fileName       = '00000016'
        outFolderName  = '../data/raw_data/intermediate'
        redactList     = [
            'InstitutionAddress', 
            'InstitutionName', 
            'PatientAddress', 
            'PatientAge',
            'PatientBirthDate',
            'PatientSex']
        dicomIO.saveAfterRedaction(folderName, fileName, outFolderName, redactList)

        print('---------[New Data]-----------------------')
        metaData = dicomIO.readFileMetaData('../data/raw_data/intermediate/00000016')
        pprint.pprint(metaData)



    except Exception as e:
        logger.error(f'Unable to perform the required tasks: {e}')

    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for module1
    
    This function finishes all the tasks for the
    main function. This is a way in which a 
    particular module is going to be executed. 
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    resultsDict: {dict}
        A dintionary containing information about the 
        command line arguments. These can be used for
        overwriting command line arguments as needed.
    '''

    print('='*30)
    print('Main function of module 1')
    print('='*30)
    print('We get a copy of the result dictionary over here ...')
    
    doSomething()

    print('Getting out of Module 1')
    print('-'*30)

    return

