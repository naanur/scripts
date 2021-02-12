import psycopg2
import os

outputfilename = 'output.txt'
if os.path.exists(outputfilename):
    os.remove(outputfilename)

conn = psycopg2.connect(database="ReportingMeeting", user="postgres", password="", host="")
c = 0
conn2 = psycopg2.connect(database="Atlas", user="postgres", password="", host="")
with open(outputfilename, 'a', encoding="utf-8") as f:
    with conn2.cursor() as cur:
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT * FROM t_report_form WHERE creation > '2021-01-01 00:00:01' AND controldate < '2021-01-26 23:59:00'""")
                forms = cursor.fetchall()
                for form in forms:
                    fid = form[0]
                    enterprise = form[8]
                    cursor.execute(f"""SELECT * FROM t_fill_report WHERE tplid = '{fid}' AND filldate < '2021-01-26 21:00:00'""")
                    fills = cursor.fetchall()
                    for fill in fills:
                        propertyid = fill[1]
                        cursor.execute(f"""SELECT count(*) FROM t_meeting_question WHERE ownerid = '{propertyid}'""")
                        count = cursor.fetchone()
                        # if int(count[0]) == 1:
                        c += 1
                        name = form[1].split('<kk-KZ>')[0].replace('<?xml version="1.0" encoding="utf-8" standalone="yes"?><Integro.Objects.DataTypes.UniString><ru-RU>', '')
                        name = name.replace('</ru-RU>','').replace('\n','').replace('\r','')
                        cur.execute(f"""SELECT name FROM contractors WHERE id = '{enterprise}'""")
                        orgName = cur.fetchone()[0]
                        date = form[7].strftime("%Y.%m.%d")
                        stringToWrite = str(c) + '\t' + orgName + '\t' + name +'\t' + date + '\t' + str(count[0]) + "\n"
                        
                        print(stringToWrite)
                        f.write(stringToWrite)

