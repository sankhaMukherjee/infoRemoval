from web import app
from flask import render_template, request
import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

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


