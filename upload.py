import psycopg2
import traceback

def sync(SQL):
        try:
                conn = psycopg2.connect("dbname='oncocasen' user='python' host='127.0.0.1' password='magicmondomania'")
                print("Connection win")
                #print(SQL)
                cur = conn.cursor()
                for i in SQL:
                        try:
                                cur.execute(i)
                        except:
                                var = traceback.format_exc()
                                print(var)
                                #print("Error:", i)
                conn.commit()
                cur.close()
                conn.close()
                print("SQL win")
        except:
                print("Something failed")
                var = traceback.format_exc()
                print(var)

