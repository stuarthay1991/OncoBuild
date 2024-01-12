import psycopg2
import traceback

def sync(SQL):
        try:
                conn = psycopg2.connect("dbname='oncocasen' user='haym4b' host='127.0.0.1' password=''")
                print("Connection win")
                #print(SQL)
                cur = conn.cursor()
                for i in SQL:
                        try:
                                print("Currently executing...", i)
                                cur.execute(i)
                                print("Execution complete")
                        except:
                                var = traceback.format_exc()
                                print(var)
                                print("connection rollback.")
                                conn.rollback()
                                #print("Error:", i)
                conn.commit()
                cur.close()
                conn.close()
                print("SQL win")
        except:
                print("Something failed")
                var = traceback.format_exc()
                print(var)

