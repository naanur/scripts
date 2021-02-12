import psycopg2
import uuid
import os
connection = psycopg2.connect(f"dbname= host= port=5432 user=postgres password=")

if os.path.exists('outputfile.sql'):
    os.remove('outputfile.sql')
if connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT owner_id, enterprise_id, id FROM t_xml_employee WHERE del_rec = False")
        employees = cursor.fetchall()
        c = 0
        e = 0
        outputfile = open('outputfile.sql', 'a', encoding='utf-8')
        for employee in employees:
            
            print(employee)
            owner_id = employee[0]
            enterprise = employee[1]
            employee_id = employee[2]
            cursor.execute("SELECT first_name FROM t_xml_person WHERE id = '%s'" % (owner_id))
            try:
                login = cursor.fetchone()[0].capitalize()
                new_user_id = uuid.uuid4()
                cursor.execute("SELECT xpath('//Employee/text()', xml_data) FROM t_xml_user WHERE del_rec = False")
                login_check = cursor.fetchall()
                r = []
                for exist_employee_id in login_check:
                    exist = exist_employee_id[0].replace('{','').replace('}', '')
                    
                    if exist == employee_id:
                        r.append(exist)
                if len(r) == 0:
                    c += 1
                    insert_user_query = f"""INSERT INTO "public"."t_xml_user"("id", "parent_id", "owner_id", "type", "xml_data", "user_id", "rec_date", "status", "del_rec") VALUES ('{new_user_id}', '{enterprise}', NULL, 'Avrora.Objects.Security.SecurityUser', '<?xml version="1.0" standalone="yes"?><Avrora.Objects.Security.SecurityUser><Enterprise>{enterprise}</Enterprise><Employee>{employee_id}</Employee><Login>{login}</Login><Password>8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92</Password><Description></Description><Locked>False</Locked><PermissionList></PermissionList><Internal>False</Internal></Avrora.Objects.Security.SecurityUser>', '288b2765-6ff8-4a88-81fc-92a25f7e18fb', '2020-07-19 16:00:00.123456', 0, 'f');"""
                    outputfile.write(insert_user_query + '\n')
            except TypeError:
                print('error at', owner_id)
            
            
        print(c, r)

        outputfile.close()