import sqlite3

def create_db():
      with sqlite3.connect('database.db') as db:
            pass

def create_table(db_name):
      with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name=?",("Keywords",))
            result = cursor.fetchall()
            if len(result) == 1:
                  #print(" Tables already available no need to create ")
                  return
            tab1 = """ create table Keywords(
                        Id integer,
                        KeyName text,
                        Average real,
                        primary key(Id))"""
            tab2 = """ create table Tweets(
                        TId integer,
                        Id integer,            
                        Tweet text,
                        Polarity real,
                        DTStamp date,
                        foreign key(Id) references Keywords(Id),
                        primary key(TId))"""
            cursor.execute(tab1)
            cursor.execute(tab2)
            db.commit()

def insert(values):
      # values = (KeyName,Tweet,Polarity,DTStamp)
      create_db()
      create_table("database.db")
      with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            sql = "select KeyName from Keywords where KeyName=?"
            key = values[0]
            cursor.execute(sql,(key,))
            result = cursor.fetchall()
            if len(result) >= 1:
                  newtweets(values)
                  return
            sql1 = """ insert into Keywords(KeyName) values (?) """
            # default average will be 0.0 updation will be done at the end
            cursor.execute(sql1,(values[0],))
            # getting Id from table Keywords
            cursor.execute(" select Id from Keywords where KeyName = ?",(values[0],))
            getId = list(cursor.fetchone())
            getId = int(getId[0])
            #print(getId)
            sql2 = """ insert into Tweets(Tweet,Polarity,DTStamp,Id)
                        values (?,?,?,?)"""
            cursor.execute(sql2,(values[1],values[2],values[3],getId))
            db.commit()

def newtweets(values):
      with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute(" select Id from Keywords where KeyName = ?",(values[0],))
            getId = list(cursor.fetchone())
            getId = int(getId[0])
            #print(getId)
            sql2 = """ insert into Tweets(Tweet,Polarity,DTStamp,Id)
                        values (?,?,?,?)"""
            cursor.execute(sql2,(values[1],values[2],values[3],getId))
            db.commit()

