import uuid
import os

if os.path.exists('out'):
    os.remove('out')
persons = open('persons.txt', 'r', encoding='utf-8')
out = open('out', 'a', encoding='utf-8')
for person in persons:
    guid = uuid.uuid4()
    
    person = person.split(' ')
    person[-1] = person[-1].replace('\n','')
    if len(person) > 2:
        first = person[0].upper()
        second = person[1].upper()
        third = person[2].upper()
    elif len(person) == 2:
        first = person[0].upper()
        second = person[1].upper()
    query = f"""INSERT INTO "public"."t_xml_person"("id", "parent_id", "owner_id", "code", "first_name", "last_name", "middle_name", "birth_date", "sex", "resident", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{guid}', '00000000-0000-0000-0000-000000000000', NULL, 0, '{first}', '{second}', '{third}', NULL, 0, 'f', 'Avrora.Objects.Common.Person', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Common.Person><AddressId>0</AddressId></Avrora.Objects.Common.Person>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 11:00:00.123456', 0, 'f');\n"""
    out.write(query)