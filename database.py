import psycopg2
con = psycopg2.connect(database='rainu')    
cur=con.cursor() 
cur.execute("DROP TABLE IF EXISTS post")  
cur.execute("CREATE TABLE post(id serial primary key,title TEXT,text TEXT,comment TEXT,time TEXT)")
con.commit()
con.close()

