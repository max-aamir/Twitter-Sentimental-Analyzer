import sqlite3
def result(key,db_name):
      with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            getId = """ select Id from Keywords
                        where KeyName = ?"""
            cursor.execute(getId,(key,))
            Id = cursor.fetchone()
            Id = int(Id[0])
            
            sql = """ select Polarity from Tweets
                        where Id = ?"""
            cursor.execute(sql,(Id,))
            polar = cursor.fetchall()
            s=0
            for i in range(len(polar)):
                  s+=float(polar[i][0])
            avg=s/len(polar)
            print("\n\n\n\n")
            print("The average polarity was found to be ",avg)
            print(" Positivity for the word %s is about %.2f"%(key,avg*100),"%")
            print("\n\n\n\n")
"""
if __name__ == "__main__":
      result("Sunday","database.db")
    
"""
