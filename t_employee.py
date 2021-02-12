import uuid
import os
import psycopg2
if os.path.exists('out_shtat'):
    os.remove('out_shtat')
connection = psycopg2.connect(f"dbname= host= port=5432 user=postgres password=")
if connection:
    with connection.cursor() as cursor:
        persons = open('shtat.txt', 'r', encoding='utf-8')
        out = open('out_shtat', 'a', encoding='utf-8')
        for person in persons:
            person = person.split('\t')

            enterprise_id = person[0]
            
            jid = int(person[-1].replace('\n', ''))
            jobtitle_id = ''
            if jid == 1:
                jobtitle_id = '2f193324-6219-4f96-a892-8863f11b3ee5' # akim
            elif jid == 2:
                jobtitle_id = '9dd310d5-73f8-4e96-8689-4b045b3c986f' # zam akima
            elif jid == 3:
                jobtitle_id = 'a516ec88-3108-40b1-9c3c-251a12e5610d' # rukap
            elif jid == 4:
                jobtitle_id = '3946d056-f0ea-45d4-a051-8fbeb1d0dae0' # sovetnik
            elif jid == 5:
                jobtitle_id = '4c88dd48-d962-4795-933c-b651873c4e62' # bas inspector
            elif jid == 6:
                jobtitle_id = 'e654564c-faf7-4e19-9a8f-8637a687c689' # bas maman
            elif jid == 7:
                jobtitle_id = 'ae27b70e-bf35-4f90-af69-914afe6b2d64' # bolim basshy
            elif jid == 8:
                jobtitle_id = '88cfcab9-5ee4-4f63-bdd3-c1e15e958ca1' # sector mengeru
            elif jid == 9:
                jobtitle_id = '8ae8c310-d946-4048-a6a0-907a228dee78' # bolim basshy orynbasary
            elif jid == 10:
                jobtitle_id = 'cddae439-5342-46eb-9b6a-88315ab1452a' # архивист 
            elif jid == 11:
                jobtitle_id = '4e05ede8-d450-4ab1-96d4-0b656501d8a9' # есепш
            elif jid == 12:
                jobtitle_id = 'addeb2cd-f2a4-4917-9d72-48230a70e136' # басшы
            elif jid == 13:
                jobtitle_id = '1e3f43b3-8c89-422c-9d0e-5e2d56022e38' # басшы орынбасары

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
            # cursor.execute(f"SELECT id FROM t_xml_person WHERE first_name = '{first}' AND last_name = '{second}' ")
            # pers_result = cursor.fetchone()
            # print(pers_result)
            # if len(pers_result) > 0:
            #     person_id = pers_result[0]
            # else:
            person_id = uuid.uuid4()
            
            person_query = f"""INSERT INTO "public"."t_xml_person"("id", "parent_id", "owner_id", "code", "first_name", "last_name", "middle_name", "birth_date", "sex", "resident", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{person_id}', '00000000-0000-0000-0000-000000000000', NULL, 0, '{first}', '{second}', '{third}', NULL, 0, 'f', 'Avrora.Objects.Common.Person', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Common.Person><AddressId>0</AddressId></Avrora.Objects.Common.Person>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 11:00:00.123456', 0, 'f');\n"""
            out.write(person_query)
            workplace_query = f"""INSERT INTO "public"."t_xml_community"("id", "parent_id", "owner_id", "head", "name", "shortname", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{workplace_id}', '{enterprise_id}', '{enterprise_id}', '{employee_id}', '{{}}', '{{}}', 'Avrora.Objects.Modules.EMS.WorkPlace, Avrora.Objects.Common.Community', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Modules.EMS.WorkPlace><Enterprise>{enterprise_id}</Enterprise><Employee>{employee_id}</Employee><JobTitle>{jobtitle_id}</JobTitle><StaffRecord>True</StaffRecord><CommunityParent>{enterprise_id}</CommunityParent></Avrora.Objects.Modules.EMS.WorkPlace>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 11:49:13.29975', 0, 'f');\n"""
            employee_query = f"""INSERT INTO "public"."t_xml_employee"("id", "parent_id", "owner_id", "enterprise_id", "from_date", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{employee_id}', '{workplace_id}', '{person_id}', '{enterprise_id}', '2020-08-24 00:00:00', 'Avrora.Objects.Modules.EMS.Employee', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Modules.EMS.Employee><WorkPlace>{workplace_id}</WorkPlace><Person>{person_id}</Person><TabNumber>0</TabNumber><WorkKind>1</WorkKind><WorkView>1</WorkView></Avrora.Objects.Modules.EMS.Employee>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-08-24 12:02:42.26966', 0, 'f');\n"""
            out.write(workplace_query)
            out.write(employee_query)
out.close()

        