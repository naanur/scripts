# -*- coding: utf-8 -*-
from docx import Document
import os
import uuid
from glob import glob

if os.path.exists('nomenlist.txt'):
    os.remove('nomenlist.txt')

paths = glob(".\\src\\*.docx")

def do_shit(source, enterprise):
# УКАЗАТЬ ИСТОЧНИК ДАННЫХ в ФОРМАТЕ docx

    doc = Document(source)

    index = ''
    header = ''
    comment = ''
    f = open('nomenlist.txt', 'a', encoding='utf-8')
    for table in doc.tables:
        for r, row in enumerate(table.rows):
            # а можно сделать список с данными и проверять наличие if not data in []: [].append(data)
            # иначе проверка на повторные столбцы
            # print(row.cells[0].text)
            try:
                index = row.cells[0].text.strip()
                if len(index) > 0:
                    
                    if index[0].isdigit() and not index in ['1', '2', '3']:
                        
                        if row.cells[1].text != row.cells[0].text :
                            header = row.cells[1].text.strip().replace('\n', '')
                        elif row.cells[2].text != row.cells[0].text and row.cells[2].text != row.cells[-1].text:
                            header = row.cells[2].text.strip().replace('\n', '')
                        elif row.cells[3].text != row.cells[0].text and row.cells[3].text != row.cells[-1].text:
                            header = row.cells[3].text.strip().replace('\n', '')
                        elif row.cells[4].text != row.cells[0].text and row.cells[4].text != row.cells[-1].text:
                            header = row.cells[4].text.strip().replace('\n', '')
                        else:
                            header = row.cells[1].text.strip().replace('\n', '')
                    
                        comment = row.cells[-1].text.strip().replace('\n', '')
                        guid = uuid.uuid4()

                        # print(r, index, header, comment)
                        if index != header:
                            query = """INSERT INTO "%s"."t_docflow_businessobjects"("id", "parent_id", "business_object_type", "typeof", "data", "user_id", "rec_date", "status", "del_rec", "json_data") VALUES ('%s', '%s', 500, 'Avrora.Objects.Modules.Docflow.DocflowObjects.Nomenclature', '<Nomenclature><Code>%s</Code><Header>%s</Header><LifeSpan>0</LifeSpan><BeginDate>01.01.2020 0:00:00</BeginDate><EndDate>31.12.2020 0:00:00</EndDate><DocumentType>Outgoing</DocumentType><RegistrationPlace reference="СЭД_Место_регистрации">1</RegistrationPlace><LifePeriod reference="СЭД_Срок_хранения">0</LifePeriod><IsClosed>False</IsClosed><IsTransit>False</IsTransit><Comment>%s</Comment></Nomenclature>', '606fab99-f9c7-4e1b-95ca-1d81d6e2167a', '2020-03-19 19:50:15.702839', 0, 'f', '{"Code": "%s", "Header": "%s", "Comment": "%s", "EndDate": "31.12.2020", "IsClosed": 0, "LifeSpan": 0, "BeginDate": "01.01.2020", "IsTransit": 0, "LifePeriod": 0, "DocumentType": 4, "RegistrationPlace": 1}');\n""" % (enterprise, guid, enterprise, index, header, comment, index, header, comment)    
                            f.write(query)
            except IndexError as ex:
                pass
    f.close()

for path in paths:
    enterprise = os.path.basename(path).replace('.docx','')
    print(path)
    do_shit(path, enterprise)