from logs import logDecorator as lD
import json, os
import pydicom as pd

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.dicomIO.dicomIO'

@lD.log(logBase + '.saveAfterRedaction')
def saveAfterRedaction(logger, folderName, fileName, outFolderName, redactList):

    try:
        logger.info(f'attempting to do file: {folderName}/{fileName}')
        ds = pd.dcmread(os.path.join(folderName, fileName))
        for k in ds.dir():
            if k in redactList:
                ds.data_element(k).value = '**************[redacted]****************'
                logger.info(f'[Redacted] {k} from {folderName}/{fileName}')

        outFile = os.path.join(outFolderName, fileName)
        if not os.path.exists(outFolderName):
            os.makedirs(outFolderName)
            logger.info(f'folder {outFolderName} doesnt exist. Generating folder')

        ds.save_as(outFile)
        logger.info(f'Saved the result in {outFile}')

    except Exception as e:
        logger.error(f'Unable to save the file {folderName}/{fileName} to {outFolderName}: {e}')
        return False, f'STATUS: [ERROR] - Unable to save the file {folderName}/{fileName} to {outFolderName}: {e}' 

    return True, f'STATUS: [OK] - Able to save the file {folderName}/{fileName} to {outFolderName}'

@lD.log(logBase + '.readFileMetaData')
def readFileMetaData(logger, fileName):
    '''[summary]
    
    [description]
    
    Parameters
    ----------
    logger : {[type]}
        [description]
    fileName : {[type]}
        [description]
    
    Returns
    -------
    [type]
        [description]
    '''

    try:

        result = {}

        ds = pd.dcmread(fileName)
        
        for k in ds.dir():

            de = ds.data_element(k)

            # we want to escape pixel data and anything
            # that is dicom specific
            if k == 'PixelData':
                continue
                
            typeVal = str(type(de.value))
            if 'pydicom' in typeVal:
                continue

            if 'str' not in typeVal:
                continue

            result[k] = de.value

        return result
            

    except Exception as e:
        logger.error(f'Unable to read metadata from the file {fileName}: {e}')



    return result

