import psycopg2
import os

"""
Перебор по схемам с обновлением срока окончания номенклатуры дел 
"""

NAME = 'stat.txt'
if os.path.exists(NAME):
    os.remove(NAME)

def get_stat(dbname):
    counter = 0
    connection = psycopg2.connect(database=dbname, user="postgres", password="", host="", port="5432")
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT table_schema FROM information_schema.tables WHERE table_name = 't_docflow_businessobjects' AND table_schema != 'public'""")
            schemas = cursor.fetchall()
            
            for scheme in schemas:
                cursor.execute(f"""SELECT * FROM "{scheme[0]}".t_docflow_businessobjects WHERE business_object_type = '500' """)
                nomens = cursor.fetchall()
                
                for nomenclature in nomens:
                    n_id = nomenclature[0]
                    data = nomenclature[9]

                    # data['EndDate'] = '31.12.2025'
                    # print(data['EndDate'])
                    cursor.execute(f"""UPDATE "{scheme[0]}".t_docflow_businessobjects SET json_data = jsonb_set(json_data, '{{EndDate}}', '"31.12.2025"') WHERE id = '{n_id}';""")
                print(scheme[0], 'is Done', len(nomens))
                connection.commit()


        
if __name__ == "__main__":
    get_stat("Avrora.C4")

                