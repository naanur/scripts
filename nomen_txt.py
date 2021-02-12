# -*- coding: utf-8 -*-
import os
import uuid
from glob import glob

# генерация номенклатуры дел напрямую в БД.

if os.path.exists('nomenlist.txt'):
    os.remove('nomenlist.txt')

paths = glob(".\\src\\*.txt")

def do_shit(source, enterprise):
# УКАЗАТЬ ИСТОЧНИК ДАННЫХ в ФОРМАТЕ txt

    doc = open(source, 'r', encoding='utf-8')

    index = ''
    header = ''
    comment = ''
    f = open('nomenlist.txt', 'a', encoding='utf-8')
    for row in doc:
        guid = uuid.uuid4()
        row = row.split('\t')
        index = row[0].strip()
        header = row[1].replace('\n','').strip()
        query = """INSERT INTO "%s"."t_docflow_businessobjects"("id", "parent_id", "business_object_type", "typeof", "data", "user_id", "rec_date", "status", "del_rec", "json_data") VALUES ('%s', '%s', 500, 'Avrora.Objects.Modules.Docflow.DocflowObjects.Nomenclature', '<Nomenclature><Code>%s</Code><Header>%s</Header><LifeSpan>0</LifeSpan><BeginDate>01.01.2020 0:00:00</BeginDate><EndDate>31.12.2020 0:00:00</EndDate><DocumentType>Outgoing</DocumentType><RegistrationPlace reference="СЭД_Место_регистрации">1</RegistrationPlace><LifePeriod reference="СЭД_Срок_хранения">0</LifePeriod><IsClosed>False</IsClosed><IsTransit>False</IsTransit><Comment>%s</Comment></Nomenclature>', '606fab99-f9c7-4e1b-95ca-1d81d6e2167a', '2020-03-19 19:50:15.702839', 0, 'f', '{"Code": "%s", "Header": "%s", "Comment": "%s", "EndDate": "31.12.2020", "IsClosed": 0, "LifeSpan": 0, "BeginDate": "01.01.2020", "IsTransit": 0, "LifePeriod": 0, "DocumentType": 4, "RegistrationPlace": 1}');\n""" % (enterprise, guid, enterprise, index, header, comment, index, header, comment)    
        f.write(query)
            
    f.close()

for path in paths:
    enterprise = os.path.basename(path).replace('.txt','')
    print(path)
    do_shit(path, enterprise)