import requests
import random
from pprint import pformat
from flask import Flask, render_template, request, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
import requests
import json
from bs4 import BeautifulSoup
import re
import os
import logging

#setup basic config for logging
logging.basicConfig(filename='test.log', level=logging.INFO, 
    format='[%(asctime)s] [%(levelname)s] %(message)s')

app = Flask(__name__)
app.secret_key = os.environ.get('MySecretServerKey')

@app.route('/')
def index():
    """Homepage"""

    logging.info('Homepage served.')
    return render_template("fal.html")



@app.route('/poem')
def fale_hafez():
    """Return random Hafez poem"""

    #Sending live request to hafizonlove website
    base_url = 'https://www.hafizonlove.com/divan/'
    ghazaliat = {'01' : ('001','002','003','004','005','011','012','022','026','032','033','035','041','042','046','047'),
            '02' : ('051','053','057','059','060','062','067','071','073','079','080'),
            '03' : ('107','108','109','112','113','118','122','132','133','140','141','142'),
            '04' : ('152','164','169','177','178','181','183','184','187','194','196','197','198','199'),
            '05' : ('203','204','205','208','231','233','234','237','239','240','243','244','245'),
            '06' : ('254','270','271','279','282','293','294','295','298','299','300'),
            '07' : ('315','316','317','318','319','320','321','322','323','324','325','326','327','331','333','335','336','349'),
            '08' : ('351','353','354','357','358','360','367','369','374','380','390','393','398'),
            '09' : ('407','415','417','418','419','420','424','428','432','449','450'),
            '10' : ('453','456','464','482','483','490','492','495')
            }

    #Generating random key, value from ghazaliat dict
    section = random.choice(list(ghazaliat.keys()))
    ghazal = random.choice(ghazaliat.get(section))

    #Live request to hafiz website
    response = requests.get(f'{base_url}/{section}/{ghazal}.htm')

    
    if response.status_code == 200:

        logging.info(f'Ghazal response was successful with status_code: {response.status_code}')
    else:
        logging.warning(f'Unable to recieve Ghazal, status_code: {response.status_code}')
        logging.warning(f'Section: {section} Ghazal: {ghazal}')

        #Redirect user to homepage via temporary redirect 
        return redirect("/", code=307)
    
    data = response.text

    #Parsing the Html result
    soup = BeautifulSoup(data,'html.parser')
    english_ghazal = (soup.find(id='Eng')).get_text()
    farsi_ghazal = (soup.find(id='farsi')).get_text()
    
    #Cleanup text and remove whitespaces
    rm_english_ghazal = re.compile('[\n\t\r\xa0]+').split(english_ghazal)
    rm_farsi_ghazal = re.compile('[\n\t\r\xa0]+').split(farsi_ghazal)

    en_beit = ''
    for beit in rm_english_ghazal:
        e_beit = beit.strip()
        if len(e_beit) > 0: 
            en_beit += f'<br>{e_beit}' 

    fa_beit = ''
    for beit in rm_farsi_ghazal:
        f_beit = beit.strip()
        if len(f_beit) > 0:
            fa_beit += f'<br>{f_beit}'  

    logging.info('Poem page served.')
    return render_template("poem.html", 
                            e_beit=en_beit, 
                            f_beit=fa_beit,
                            )

@app.route('/about')
def about():
    """Homepage."""

    return render_template('about.html')

if __name__ == '__main__':
    # set debug=True here, to invoke the DebugToolbarExtension 
    app.debug = False
    app.config['SECRET_KEY'] = "<MySecretServerKey>"
    DebugToolbarExtension(app)        
    app.run(port=5001, host='0.0.0.0')