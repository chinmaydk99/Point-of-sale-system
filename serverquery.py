import pymysql
import pymysql
db = pymysql.connect("localhost", "root", "narutosasuke", "testitems" )
transcursor = db.cursor()

print("-------- Information Centre -------")
while(1):
  print("Enter 0 for exit anytime\nEnter any other number to continue")
  c = int(input())
  if c == 0:
    print("Closing....")
    db.close
    sys.exit()
  else:    
    print("Enter the type of transaction information:")
    print("1. Daily Earnings")
    print("2. Items sold")
    print("3. Customers")
    b = int(input())
    if(b==1):
        sql = "select Date, sum(Price) from store group by date;"
        transcursor.execute(sql)
        lis = transcursor.fetchall()
        for i in lis:
            for j in i:
                print(j, end = "--")
               
            print("\n")
            
    elif(b==2):
        sql = "select store.Code, items.Description , count(store.Code), sum(store.Price) from items, store where store.Code = items.Code group by(Code);"
        transcursor.execute(sql)
        lis = transcursor.fetchall()
        for i in lis:
            for j in i:
                print(j, end = " -- ")
            print("\n")

    elif(b==3):
        sql = " select store.Cust_name, store.Cust_phone, sum(store.price) from store  group by Cust_name, Cust_phone;"
        transcursor.execute(sql)
        lis = transcursor.fetchall()
        for i in lis:
            for j in i:
                print(j, end = " -- ")
            print("\n")

    elif(b==0):
        db.close()
        sys.exit()
    else:
        print("Invalid option")

