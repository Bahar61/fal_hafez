

import requests
import random
from pprint import pformat
from flask import Flask, render_template, request, flash
import requests
import json
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
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
    data = response.text

    #Parsing the Html result
    soup = BeautifulSoup(data,'html.parser')
    english_ghazal = (soup.find(id='Eng')).get_text()
    farsi_ghazal = (soup.find(id='farsi')).get_text()
    
    #Cleanup text and remove whitespaces
    rm_english_ghazal = re.compile('[\n\t\r\xa0]+').split(english_ghazal)
    rm_farsi_ghazal = re.compile('[\n\t\r\xa0]+').split(farsi_ghazal)

    for beit in rm_english_ghazal:
        e_beit = beit.strip()
        if len(e_beit) > 0: 
            print(e_beit) 

    for beit in rm_farsi_ghazal:
        f_beit = beit.strip()
        if len(f_beit) > 0:
            print(f_beit)  
        
    
fale_hafez()