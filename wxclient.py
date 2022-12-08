import socket
import os
import subprocess
import wx
import wx.grid as gridlib
import webbrowser

#Open the file for writing the bill
bill = open("Bill.txt","w")

import pymysql
db = pymysql.connect("localhost", "root", "narutosasuke", "testitems" )
cursor = db.cursor()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host ='192.168.43.253'
port = 9999
#s.connect((host,port))
addr = (host,port)

sum1 =0.0
count = 0
name = ""
phone = ""

#Function to send list of items
def send_data(lis):
        
    data = lis[0] + "," + lis[1] 
    print("DATA" , data)
    s.sendto(data.encode("utf-8"), addr)
    print("Sent successfully")
            
            
#Creating textfields for getting customer info(name and phone no)            
class GetData(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Customer Info", size= (650,220))
        self.panel = wx.Panel(self,wx.ID_ANY)
        self.lblname = wx.StaticText(self.panel, label="Customer Name", pos=(20,20))
        self.name = wx.TextCtrl(self.panel, value="", pos=(110,20), size=(500,-1))
        self.lblsur = wx.StaticText(self.panel, label="Customer Phone", pos=(20,60))
        self.surname = wx.TextCtrl(self.panel, value="", pos=(110,60), size=(500,-1))
        self.saveButton =wx.Button(self.panel, label="Save", pos=(110,100))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Show()

    def OnQuit(self, event):
        self.result_name = None
        self.Destroy()

    def SaveConnString(self, event):
        global name
        global phone
        name = self.name.GetValue()
        phone = self.surname.GetValue()
        
        print("Name - ", name)
        print("Phone - ", phone)
        frame = MyForm().Show()
       
        self.Destroy()


#Creating grid to get list of items from the cashier
class MyGrid(gridlib.Grid):      

    def __init__(self, parent):
        """Constructor"""
        gridlib.Grid.__init__(self, parent)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        
        
    def OnCellChange(self, evt):
        print("OnCellChange: (%d,%d) \n" % (evt.GetRow(), evt.GetCol() ))

        row = evt.GetRow()
        col = evt.GetCol()
        val = self.GetCellValue(row, col)
        cursor.execute("select Code from items")
        lis = cursor.fetchall()
        if(col == 0):

         try:    
            cell_input = int(val)
            global count
            count = count + 1
                
                
            sql = "select Description, Price from items where Code = " + val;
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                
                    c = 1
                    for x in result[0]:
                        
                        self.SetCellValue(row,c,str(x))
                        c = c+1
                    global sum1
                    sum1 = sum1 + float(result[0][1])
                    
                       
                    
                        
            else:
                    wx.CallAfter(self.notfound)
                    
                
         except:               
            self.SetCellValue(row, col, '')
            wx.CallAfter(self.Later)
    
#Raise an error message if invalid input is entered
    def Later(self):
        wx.MessageBox('Invalid Input! Please Try Again', 'Error', wx.OK | wx.ICON_HAND | wx.CENTRE)
#Raise an exception if item code entered is not matched with existing list
    def notfound(self):
        wx.MessageBox('Item Code not recognized', 'Error', wx.OK | wx.ICON_HAND | wx.CENTRE)


class MyForm(wx.Frame):

    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Items")
        panel = wx.Panel(self)
        

        

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.btn = wx.Button(panel,-1,"Submit")
        
        
        sizer.Add(self.btn,0,  wx.SHAPED)
        self.btn.Bind(wx.EVT_BUTTON,self.OnClicked)
        myGrid = MyGrid(panel)
        myGrid.CreateGrid(12, 3)
        myGrid.SetCellValue(0,0,"Code")
        myGrid.SetCellValue(0,1,"Description")
        myGrid.SetCellValue(0,2,"Price")
       
        self.abc = myGrid
        sizer.Add(myGrid, 1, wx.SHAPED)
        panel.SetSizer(sizer)
        

    def OnClicked(self, event): 
        btn = event.GetEventObject().GetLabel()
        
        final = []
        for i in range(1,count+1):
            lis =[]
            lis.append(self.abc.GetCellValue(i,0))
            lis.append(self.abc.GetCellValue(i,2))
            
            send_data(lis)
            lis.append(self.abc.GetCellValue(i,1))
            final.append(lis)
        
        print("Items list sent")
        print("Sending customer info")
        st = "sending customer info"
        s.sendto(st.encode("utf-8"), addr)
        st = name + "," + phone
        s.sendto(st.encode("utf-8"), addr)
        
        print("Customer info sent")
        st = "quit"
       
        s.sendto(st.encode('utf-8'), addr)

        bill.write("******* BILL ********\n\n")
        bill.write("Customer Name - " + name + "\n")
        bill.write("Customer Phone - " + phone + "\n\n")
        x = bill.tell()
        bill.write("Code")
        bill.seek(x+15,0)
        bill.write("Description")
        bill.seek(x+30,0)
        bill.write("Price\n\n")

        for i in final:
            x = bill.tell()
            bill.write(i[0])
            bill.seek(x+15,0)
            bill.write(i[2])
            bill.seek(x+30,0)
            bill.write(i[1]+"\n\n")
        x = bill.tell()
        bill.write("Total Price - ")
        bill.seek(x+30,0)
        
        
        bill.write(str(sum1))
        
      
app = wx.App()
dlg = GetData(None)
dlg.Show()

app.MainLoop()
webbrowser.open("Bill.txt")
db.close()

bill.close()
