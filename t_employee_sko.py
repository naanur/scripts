import uuid
import os
import psycopg2
if os.path.exists('out_shtatsko'):
    os.remove('out_shtatsko')
connection = psycopg2.connect(f"dbname= host=localhost port=5432 user=postgres password=")
if connection:
    with connection.cursor() as cursor:
        persons = open('shtatskogm.txt', 'r', encoding='utf-8')
        out = open('out_shtatsko', 'a', encoding='utf-8')
        for person in persons:
            person = person.split('\t')

            enterprise_id = person[0]
            
            jid = int(person[-1].replace('\n', ''))
            jobtitle_id = ''
            if jid == 1:
                jobtitle_id = '2ed3d809-6719-422b-b77f-c1cee64ca527' # akim
            elif jid == 2:
                jobtitle_id = 'b365559c-d5ad-4e90-be8d-026255039529' # zam akima
            elif jid == 3:
                jobtitle_id = 'c847379c-d5ad-4e90-be8d-026273039529' # главный спец
            elif jid == 4:
                jobtitle_id = '85f82a90-005a-48f7-8e92-272159fa5428' # ведущий спец
            
            

            
            workplace_id = uuid.uuid4()
            employee_id = uuid.uuid4()
            # print(person)
            fio = person[1].split()
            if len(fio) > 2:
                first = fio[0].upper().strip()
                second = fio[1].upper().strip()
                third = fio[2].upper().strip()
            elif len(fio) == 2:
                first = fio[0].upper().strip()
                second = fio[1].upper().strip()
                third = ''
            elif len(fio) == 1:
                print('ERROR at ', fio)
            cursor.execute(f"SELECT id FROM t_xml_person WHERE first_name = '{first}' AND last_name = '{second}' ")
            pers_result = cursor.fetchall()
            # print(pers_result)
            if len(pers_result) > 0:
                person_id = pers_result[0]
            else:
                person_id = uuid.uuid4()
                
                person_query = f"""INSERT INTO "public"."t_xml_person"("id", "parent_id", "owner_id", "code", "first_name", "last_name", "middle_name", "birth_date", "sex", "resident", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{person_id}', '00000000-0000-0000-0000-000000000000', NULL, 0, '{first}', '{second}', '{third}', NULL, 0, 'f', 'Avrora.Objects.Common.Person', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Common.Person><AddressId>0</AddressId></Avrora.Objects.Common.Person>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 11:00:00.123456', 0, 'f');\n"""
                out.write(person_query)
                workplace_query = f"""INSERT INTO "public"."t_xml_community"("id", "parent_id", "owner_id", "head", "name", "shortname", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{workplace_id}', '{enterprise_id}', '{enterprise_id}', '{employee_id}', '{{}}', '{{}}', 'Avrora.Objects.Modules.EMS.WorkPlace, Avrora.Objects.Common.Community', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Modules.EMS.WorkPlace><Enterprise>{enterprise_id}</Enterprise><Employee>{employee_id}</Employee><JobTitle>{jobtitle_id}</JobTitle><StaffRecord>True</StaffRecord><CommunityParent>{enterprise_id}</CommunityParent></Avrora.Objects.Modules.EMS.WorkPlace>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 11:49:13.29975', 0, 'f');\n"""
                employee_query = f"""INSERT INTO "public"."t_xml_employee"("id", "parent_id", "owner_id", "enterprise_id", "from_date", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{employee_id}', '{workplace_id}', '{person_id}', '{enterprise_id}', '2020-08-24 00:00:00', 'Avrora.Objects.Modules.EMS.Employee', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Modules.EMS.Employee><WorkPlace>{workplace_id}</WorkPlace><Person>{person_id}</Person><TabNumber>0</TabNumber><WorkKind>1</WorkKind><WorkView>1</WorkView></Avrora.Objects.Modules.EMS.Employee>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 12:02:42.26966', 0, 'f');\n"""
                out.write(workplace_query)
                out.write(employee_query)
out.close()

        