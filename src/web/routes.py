from web import app
from flask import render_template, request
import json, os

from lib.dicomIO import dicomIO as dIO

@app.route('/')
@app.route('/index')
def index():
    return render_template('mainApp.html')

@app.route('/inpFile', methods=['GET', 'POST'])
def inpFile():

    label = '[get a folder and file]'
    if request.method == 'POST':
        images = request.form.getlist('dicom')
        folder = request.form.getlist('folderName')

        print('----------------------')
        print(images)
        print(request.form)
        print(folder)
        print('----------------------')

        if type(images) == list:
            fileName = images[0]
        else:
            fileName = images

        fileName = os.path.join(folder[0], fileName)
        print(fileName)
        if not os.path.exists(fileName):
            label = f'[Error: file does not exist: {fileName}'
        else:
            label = f'[Success: The selected file exists: {fileName}. You can proceed to select redaction list ...'

            # Save the name of the folder for redaction
            folderName = json.dumps({
                "folderName":folder[0], 
                "sampleFile": fileName })

            with open('../config/webCache/folderName.json', 'w') as fOut:
                fOut.write( folderName )

            metaData = dIO.readFileMetaData(fileName)
            toSave = []
            for k in metaData:
                toSave.append({
                    "item": k,
                    "checked": "",
                    "text" : metaData[k] })

            toSave = json.dumps(toSave)
            print(toSave)
            with open('../config/webCache/showList.json', 'w') as fOut:
                fOut.write(toSave)

    return render_template('openFile.html', label=label)

@app.route('/showList', methods=['GET', 'POST'])
def showList():

    cachedVals = json.load(open('../config/webCache/showList.json'))
    print(cachedVals)
    
    if request.method == 'POST':
        itemList = request.form.getlist('checkedItems')
        for i, k in enumerate(cachedVals):
            if k['item'] in itemList:
                cachedVals[i]['checked'] = 'checked'
            else:
                cachedVals[i]['checked'] = ''

        json.dump(cachedVals, open('../config/webCache/showList.json', 'w'))


    return render_template('showList.html', items=cachedVals)

@app.route('/redact', methods=['GET', 'POST'])
def redact():

    cachedVals = json.load(open('../config/webCache/showList.json'))
    folder     = json.load(open('../config/webCache/folderName.json'))
    print(cachedVals)
    print(folder)

    items  = [ c['item'] for c in cachedVals if c['checked'] == 'checked']
    others = [ c['item'] for c in cachedVals if c['checked'] != 'checked']
    
    if request.method == 'POST':
        print('Redacting things ....')


    return render_template('redact.html', folder=folder['folderName'], items = items, others=others)



