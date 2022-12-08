import socket
import sys

#Connection to mysql database
import pymysql
db = pymysql.connect("localhost", "root", "narutosasuke", "testitems" )
cursor = db.cursor()

vals = []
cust_vals = []

#creating a socket
def create_socket():
    
        global host
        global port
        global s
        global addr
        host = ""
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #except socket.error as msg:
    #    print("Socket creation error" + str(msg))

#binding the socket
def bind_socket():
    
        global host
        global port
        global s

        print("Binding the port "+ str(port))
        addr = (host,port)

        s.bind((host,port))
        #s.listen(5)

    #except socket.error as msg:
     #   print("Socket binding error" + str(msg) + "\nRetrying....")
      #  bind_socket()

#receiving the data from client 
def recv_data():

    global cust_vals
    global s
    while True:
        t, addr = s.recvfrom(1024)
        
        client_data = t.decode("utf-8")
        print("Client data - ", client_data)
        
        
        #If client sends 'quit', save the items into database and close the connection
        if 'quit' in client_data:
            for x in vals:
                print("List of items - ", x)
                sql = "insert into store(Date, Code , Price, Cust_name, Cust_phone) values (CURDATE()," + x[0]+ "," + x[1]+ "," + "\'" + cust_vals[0] + "\'" + "," + "\'" + cust_vals[1] + "\'" + ");";
                cursor.execute(sql)
                db.commit()
            
            s.close()
            sys.exit()
            
        #Getting the customer information (name and phone no) 
        elif 'customer info' in client_data:
            d, addr = s.recvfrom(1024)
            data = d.decode("utf-8")
            cust = data.split(",")
            cust_vals.append(cust[0])
            cust_vals.append(cust[1])
            print("Name - " + cust[0])
            print("Phone - " + cust[1])
        
        #If data sent is itemas, append them into a list of items    
        else:
            lis = client_data.split(",")
            vals.append(lis)
            print(lis)
         
        
#Accepting the connection request from the client        
def socket_accept():
    
    recv_data()
    s.close()

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()
db.close()
