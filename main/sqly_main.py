from tkinter import *
import tkinter as tk
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import statistics
from scipy.stats import skew,kurtosis,norm

#REPORT BASE GENERATION    #0 will be component name
html_img_component = '''
        <section>
			<h2>{0}</h2>  
            <img src = "{1}",alt="ERROR IN DISPLAY">
			<p>{2}</p>-
		</section>'''

html_txt_component = '''
    <section>
			<h2>{0}</h2>  
			<p>{1}</p>
	</section>
'''
global html_base
html_base = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Technical Report Template</title>
	<link rel="stylesheet" href="style.css">
</head>
<body>
	<header>
		<h1>{0}</h1>
		<p>SQLY DATABASE REPORT</p>
	</header>
	<main>
		{1}
	</main>
	<footer>
		<p>© 2023 DBMS CAMP DATABASE PROJECT | SQLY GENERATED REPORT </p>
	</footer>
</body>
</html>
'''

global main_comp
header_comp = []

def generateReport(report_name):
    emp = ""
    write_base = html_base.format(report_name,emp.join(header_comp))
    print(write_base)
    report = open('bin/reports/{0}.html'.format(report_name),'w+')
    report.write(write_base)
    report.close()

# SQL DATABASE CONNECTIVITY ERROR
class sqlyError(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x200")
        self.title("Error")
        cross_logo = tk.PhotoImage(file="bin/cross_icon.png")
        self.iconphoto(False,cross_logo)
        self.resizable(False,False)
        lb_error_name = Label(self,text="Database Connectivity Error",font=("Times New Roman",12),fg='red')
        lb_error_name.place(x=10,y=0)


# SELECT DATABASE
class chooseDB(tk.Tk):
    def __init__(self):
        super().__init__()
        global clicked

        self.clicked = StringVar(self)
        self.rep = StringVar(self)

        self.clicked.set("database name")
        self.geometry("300x170")
        self.title("Database Selection")
        cross_logo = tk.PhotoImage(file="bin/sqly_logo.png")
        self.iconphoto(False,cross_logo)
        self.resizable(False,False)
        bg = PhotoImage(file="bin/sqly_logo.png")
        lb_bg = Label(self,image=bg)
        lb_bg.place(x=50,y=0)
        lb_bg.image = bg


        cursor = mydb.cursor()
        cursor.execute("SHOW DATABASES")
        avail_databases = cursor.fetchall()
        options = []
        for x in avail_databases:
            options.append(x)
        
        lbl = Label(self,text="Select a database:")
        lbl.place(x=5,y=90)
        drop = OptionMenu(self,self.clicked,*options)
        drop.place(x=100,y=85)

        rname = Label(self,text="Report name:")
        rname.place(x=5,y=120)
        entry_rname = Entry(self,textvariable=self.rep,width=30)
        entry_rname.place(x=85,y=120)



        choose_button = Button(self,text="Continue",command=self.start)
        choose_button.place(x=110,y=145)

       # mydb = mysql.connector.connect(host=conn_host,user=conn_user,password=conn_pswd,database='pokemon')

    def start(self):
        global repname
        global db
        db_raw = self.clicked.get()
        db = "".join(ch for ch in db_raw if ch.isalnum())

        print(db)
        repname =  self.rep.get()
        self.destroy()
        main = sqlyMain()
        main.mainloop()


# SQLY ANALYSIS TERMINAL
# select {table-name}
# xRy = how does x change with y = correlation
# sql execute {sql query}
# in future: hypothesis testing language -> compile and parse -> give ans (possibly use a language model)

class sqlyAnalysis(tk.Toplevel):
    def __init__(self,parent):

        super().__init__(parent)
        self.geometry("400x160")
        self.title('SQLY Analysis Commands')
        self.resizable(False,False) 
        self.configure(bg='black')
        logo = tk.PhotoImage(file="bin/sqly_logo.png")
        self.iconphoto(False,logo)

        info_lb_1 = Label(self,text="SQLY ANALYSIS TERMINAL",bg="black",fg="blue")
        info_lb_1.place(x=130,y=0)
        info_lb_2 = Label(self,text="Commands available for this version:",bg="black",fg="white")
        info_lb_2.place(x=0,y=20)
        info_lb_3 = Label(self,text="|select {table-name}|select a table| ",bg="black",fg="white")
        info_lb_4 = Label(self,text="|x R y|how x relates to y|",bg="black",fg="white")
        info_lb_3.place(x=0,y=40)
        info_lb_4.place(x=0,y=60)

        
        self.table = StringVar()
        self.x = StringVar()
        self.y = StringVar()
      

        dbselect_lb = Label(self,text="select",bg='black',fg='white')
        dbselect_lb.place(x=0,y=80)
        dbselect_entry = Entry(self,textvariable=self.table,width=20)
        dbselect_entry.place(x=40,y=80)
        dbselect_button = Button(self,text="Execute",command=self.table)
        dbselect_button.place(x=180,y=80)
        #cursor = conn.cursor()
        self.update()

        xyselect_lb = Label(self,text="X Y",bg="black",fg="white")
        xyselect_lb.place(x=0,y=110)
        xyselect_entry = Entry(self,textvariable=self.x,width=20)
        xyselect_entry.place(x=30,y=110)
        xy_button = Button(self,text = "Execute", command=self.setval)
        xy_button.place(x=180,y=110)
        
        
    def relation(self,xa,ya,table):
      conn = mysql.connector.connect(host=conn_host,user=conn_user,password=conn_pswd,database=db)
      query1 = "SELECT {0} FROM {1}".format(xa,table)
      query2 = "SELECT {0} FROM {1}".format(ya,table)
      cursor = conn.cursor()
      cursor.execute(query1)
      result = cursor.fetchall()

      x = []
      y = []

      for a in result:
          x.append(int(a[0]))
      cursor.execute(query2)
      result = cursor.fetchall()

      for b in result:
          y.append(int(b[0]))

      nx = np.array(x)
      ny = np.array(y)

      coeff_matrix = np.corrcoef(nx,ny)
      corr = coeff_matrix[1][0]
      print(coeff_matrix[1][0])

      plt.scatter(nx,ny)
      plt.savefig("bin/reports/cor_graph.png")
      new_comp = html_img_component
      p1 = "Correlation for table {0} for attributes {1} {2}".format(table,xa,ya)
      p2 = "cor_graph.png"
      if(abs(corr) > 0.90):
          p0 = "Very High"
      elif(abs(corr) < 0.90 and abs(corr) > 0.70):
          p0 = "High"
      elif(abs(corr) < 0.7 and abs(corr) > 0.5):
          p0 = "Moderate"
      else:
          p0 = "Low"

          
      if(corr > 0):
          p3 = "There is a {0} positive correlation b/w the attributes {1} and {2}, meaning they grow with each other".format(p0,xa,ya)
      else:
          p3 = "There is a {0} negative correlation b/w the attributes {1} and {2}, meaning they grow with each other".format(p0,xa,ya)

      new_comp = html_img_component.format(p1,p2,p3)
      print(new_comp)
      header_comp.append(new_comp)
      

      
    def setval(self):
        xyval = self.x.get()
        xylst = xyval.split()
        xval = xylst[0]
        yval = xylst[1]
        tab = self.table.get()
        self.relation(xa=xval,ya=yval,table=tab)

  

#SQL BASIC STATISTICS
class sqlyBstats(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("350x200")
        self.title('SQLY Statistics')
        self.resizable(False,False) 
        logo = tk.PhotoImage(file="bin/sqly_logo.png")
        self.iconphoto(False,logo)
        
        self.table = StringVar()
        self.mean = IntVar()
        self.median = IntVar()
        self.mode = IntVar()
        self.skew_kurt = IntVar()
        self.sd = IntVar()
        self.quartile = IntVar()

        lbl= Label(self,text="Provide the table and attribute [table;attribute]:")
        lbl.place(x=0,y=0)
        lbl_p = Entry(self,textvariable=self.table,width=200)
        lbl_p.place(x=0,y=20)

        c1 = Checkbutton(self,text="Mean",variable=self.mean,onvalue=1,offvalue=0)
        c1.place(x=10,y=40)
        c2 = Checkbutton(self,text="Median",variable=self.median,onvalue=1,offvalue=0)
        c2.place(x=70,y=40)
        c3 = Checkbutton(self,text="Mode",variable=self.mode,onvalue=1,offvalue=0)
        c3.place(x=10,y=60)
        c4 = Checkbutton(self,text="Skewness/Kurtosis",variable=self.skew_kurt,onvalue=1,offvalue=0)
        c4.place(x=70,y=60)
        c5 = Checkbutton(self,text="SD",variable=self.sd,onvalue=1,offvalue=0)
        c5.place(x=10,y=80)
        c6 = Checkbutton(self,text="Quartile Deviation",variable=self.quartile,onvalue=1,offvalue=0)
        c6.place(x=70,y=80)

        submit = Button(self,text="Submit",command=self.NewComp)
        submit.place(x=100,y=110)
    
    def NewComp(self):
        check = self.table.get()
        check_lst = check.split(";")
        table = check_lst[0]
        bool_tab = []
        attribute = check_lst[1]
        v1 = self.mean.get()
        bool_tab.append(v1)
        v2 = self.mean.get()
        bool_tab.append(v2)
        v3 = self.mean.get()
        bool_tab.append(v3)
        v4 = self.mean.get()
        bool_tab.append(v4)
        v5 = self.mean.get()
        bool_tab.append(v5)
        v6 = self.mean.get()
        bool_tab.append(v6)
       
        self.checkComp(table,attribute,bool_tab)

    def checkComp(self,tab,attr,btab):
        conn = mysql.connector.connect(host=conn_host,user=conn_user,password=conn_pswd,database=db)
        query1 = "SELECT {0} FROM {1}".format(attr,tab)
        cursor = conn.cursor()
        cursor.execute(query1)
        result = cursor.fetchall()
        x = []
        for a in result:
          x.append(int(a[0]))

      

        print(btab)
        if(btab[0]):
            #mean
            mean_x = statistics.mean(x)
            print("mean:",mean_x)
            p1 = "Mean of Attribute {0}".format(attr)
            comp = html_txt_component.format(p1,mean_x)
            header_comp.append(comp)
        if(btab[1]):
            #median
            median_x = statistics.median(x)
            p1 = "Median of Attribute {0}".format(attr)
            comp = html_txt_component.format(p1,median_x)
            print("median:", median_x)
            header_comp.append(comp)

        if(btab[2]):
            #mode
            modex = statistics.mode(x)
            print("mode:",modex)
            p1 = "Mode of Attribute {0}".format(attr)
            comp = html_txt_component.format(p1,median_x)
            print("median:", modex)
            header_comp.append(comp)

        if(btab[3]):
            #skewness/kurtosis
            skewn = skew(x,axis=0,bias=True)
            kurtos = kurtosis(x,axis=0,bias=True)
            print("skew:",skewn)
            print("kurt:",kurtos)
            p1 = "Skewness/Kurtosis for {0}".format(attr)
            plt.plot(x,norm.pdf(x,statistics.mean(x),statistics.stdev(x)))
            plt.savefig("bin/reports/sk_graph.png")
            p2 = "sk_graph.png"
            p3 = "LOREM IPSUM"
            comp = html_img_component.format(p1,p2,"skewness:{0},kurtosis:{1}".format(skewn,kurtos))
            header_comp.append(comp)

        if(btab[4]):
            #sd
            sd = statistics.stdev(x)
            print("sd:",sd)
            p1 = "Mode of Attribute {0}".format(attr)
            comp = html_txt_component.format(p1,sd)
            header_comp.append(comp)

        if(btab[5]):
            #quartile deviation
            q1 = np.quantile(x,0.25)
            q2 = np.quantile(x,0.50)
            q3 = np.quantile(x,0.75)
            qd = (q3 - q1)/2
            print("qd:",qd)
            p1 = "Quartile Deviation of Attribute {0}".format(attr)
            comp = html_txt_component.format(p1,qd)
            header_comp.append(comp)



#SQL VISUALIZATION TOOL
class sqlyVisual(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("300x150")
        self.title('SQLY Visualizer')
        self.resizable(False,False) 
        logo = tk.PhotoImage(file="bin/sqly_logo.png")
        self.iconphoto(False,logo)
        lbl = Label(self,text="")
        lbl.place(x=0,y=0)
       



# SQLY DASHBOARD
class sqlyMain(tk.Tk):
    def __init__(self):
        super().__init__()
      
        
        components = ""

        self.geometry("300x210")
        self.title('SQLY Dashboard')
        self.resizable(False,False)        

        logo = tk.PhotoImage(file="bin/sqly_logo.png")
        self.iconphoto(False,logo)
        
        bg = PhotoImage(file="bin/sqly_logo.png")
        lb_bg = Label(self,image=bg)
        lb_bg.place(x=50,y=0)
        lb_bg.image = bg
     
        info_lb = Label(self,text="Choose report elements:")
        info_lb.place(x=0,y=90)

        bstats = Button(self,text="BASIC STATISTICAL TOOLS",width=40,command=self.stats)
        bstats.place(x=5,y=110)
        analysis = Button(self,text="CORRELATION",width=40,command=self.infer)
        analysis.place(x=5,y=130)

        gen = Button(self,text = "Generate Report",command=self.generate,bg='green')
        gen.place(x=100,y=180)


    def generate(self):
        generateReport(repname)
    
    def stats(self):
        bstat = sqlyBstats(self)
        bstat.grab_set()

    def visual(self):
        viz = sqlyVisual(self)
        viz.grab_set()

    def infer(self):
        sa = sqlyAnalysis(self)
        sa.grab_set()



# SQLY INFORMATION
class sqlyInfo(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.geometry("300x150")
        self.title('SQLY Information')
        bg = PhotoImage(file="bin/sqly_logo.png")
        lb_bg = Label(self,image=bg)
        lb_bg.place(x=50,y=0)
        lb_bg.image = bg
        info_lb = Label(self,text="SQLY provides the program user a tool to visualize and\nstatistically analyze a user provided database")
        info_lb.place(x=0,y=90)

      


#SQL INITIAL LOGIN
class sqlyInit(tk.Tk):

    def __init__(self):
        super().__init__()
        self.host_string = StringVar()
        self.user_string = StringVar()
        self.pswd_string = StringVar()

        self.title("SQLY Data Analysis Tool")
        
        self.geometry("300x230")
        self.resizable(False,False)        
        
        logo = tk.PhotoImage(file="bin/sqly_logo.png")
        self.iconphoto(False,logo)
        
        bg = PhotoImage(file="bin/sqly_logo.png")
        lb_bg = Label(self,image=bg)
        lb_bg.place(x=50,y=0)
        lb_bg.image = bg

        lb_instr = Label(self,text="Provide the following database connection details:")
        lb_instr.place(x=0,y=90)

        # Entry fields
        lb_host = Label(self,text="Host:")
        entry_host = Entry(self,textvariable=self.host_string,width=40)
        entry_host.place(x=35,y=110)
        lb_host.place(x=0,y=110)
        lb_user = Label(self,text="User:")
        entry_user = Entry(self,textvariable=self.user_string,width=40)
        entry_user.place(x=35,y=135)
        lb_user.place(x=0,y=135)
        lb_password = Label(self,text="Pswd:")
        entry_password = Entry(self,textvariable=self.pswd_string,show="*",width=40)
        entry_password.place(x=35,y=160)
        lb_password.place(x=0,y=160)

        submit = Button(self,text="Information",command=self.showInfo)
        submit.place(x=20,y=190,width=70)
        info = Button(self,text="Enter",command=self.connectDB)
        info.place(x=120,y=190,width=70)
        quit = Button(self,text="Quit",command=self.destroy)
        quit.place(x=220,y=190,width=70)

    def showInfo(self):
        window = sqlyInfo(self)
        window.grab_set()

    def connectDB(self):
        global conn_host,conn_user,conn_pswd
        conn_host = self.host_string.get()
        conn_user = self.user_string.get()
        conn_pswd = self.pswd_string.get()

        startSession(self,conn_host,conn_user,conn_pswd)
     
        

def startSession(sqlyIni,hst,usr,pswd):
    sqlyIni.destroy()
    try:
        global mydb
        mydb = mysql.connector.connect(host=hst,user=usr,password=pswd)
        sqly = chooseDB()
        sqly.mainloop()
    except:
        error = sqlyError()
        error.mainloop()
        



#DRIVER CODE
if __name__ == "__main__":
    #generateReport('ayush')
    sqlyEntry = sqlyInit()
    sqlyEntry.mainloop()

 







