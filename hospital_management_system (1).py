#hospital management system

#importing modules
import mysql.connector as sqltor
from datetime import date,timedelta
import random
import stdiomask as s
import os
from tabulate import tabulate
db=sqltor.connect(user='root',passwd='nx310')
cur=db.cursor()

# creating database
cur.execute('create database if not exists hospital;')
cur.execute('use hospital;')

# creating tables
cur.execute('create table if not exists patient(pid char(5) primary key,name varchar(100),age varchar(3),gender char(1),email varchar(100),phno char(10),password char(8) unique,chronic varchar(500));')
cur.execute('create table if not exists employee (empid char(5) primary key,name varchar(100),age varchar(3),gender char(1),email varchar(100),phno char(10),password char(8) unique,dept varchar(50),job varchar(50),wdi varchar(100),salary int,cpa varchar(5));')
cur.execute('create table if not exists history (empid char(5) ,pid char(5),date date,time time,disease varchar(50),tablets_prescribed varchar(500),tests_prescribed varchar(500),height varchar(4),weight varchar(4),cdcount varchar(100));')
cur.execute('create table if not exists lab(pid char(5),empid char(5),test varchar(500),date date,time time,status varchar(50),cost int);')
cur.execute('create table if not exists appointment(pid char(5),empid char(5),date date,time time,token int);')
cur.execute('create table if not exists med_shop(mid char(3),med_name varchar(50),stock int check(stock>1),price int);')
cur.execute('create table if not exists lab_test(test_name varchar(50),price int);')

#functions
def bkap(pid):
    cur.execute('select distinct dept from employee where dept!="staff";')
    x=cur.fetchall()
    print('Select Department:')
    for i in range(len(x)):
        print(str(i+1)+'.'+x[i][0])
    ch=int(input('\nEnter your choice :'))
    cur.execute('select name,empid from employee where dept=(%s) and job="doc";',(x[ch-1][0],))
    y=cur.fetchall()
    print('\nSelect Consultant:')
    for i in range(len(y)):
        print(str(i+1)+'.'+y[i][0])
    ch2=int(input('\nEnter your choice :'))
    eid=y[ch2-1][1]
    cur.execute('select wdi from employee where empid=%s;',(eid,))
    z=cur.fetchall()
    da=date.today()+timedelta(days=1)
    cur.execute('select date,token from appointment where empid=%s;',(eid,))
    d=cur.fetchall()
    l=[]
    for i in range(3):
        while len(l)!=3:
            if str(date.weekday(da)) in z[0][0]:
                if (da,20) not in d:
                    l.append(str(da))
            da+=timedelta(days=1)
    print('\nSelect a date:')
    for i in range(3):
        print(str(i+1)+'.'+l[i])
    ch3=int(input('\nEnter your choice :'))
    cur.execute('select token from appointment where date=%s;',(l[ch3-1],))
    fe=cur.fetchall()
    if fe==[]:
        cur.execute('insert into appointment values(%s,%s,%s,"10:00:00",1);',(pid,eid,l[ch3-1]))
        db.commit()
        print('Appointment successfully booked!')
        print('Appointment date:',l[ch3-1])
        print('Appointment time: 10.00 pm')
        print('Token number:1')
    elif fe[0][0]<=10:
        cur.execute('insert into appointment values(%s,%s,%s,"10:00:00",%s);',(pid,eid,l[ch3-1],fe[0][0]+1))
        db.commit()
        print('Appointment successfully booked!')
        print('Appointment date:',l[ch3-1])
        print('Appointment time: 10.00 am')
        print('Token number:',fe[0][0]+1)
    else:
        cur.execute('insert into appointment values(%s,%s,%s,"18:00:00",%s);',(pid,eid,l[ch3-1],fe[0][0]+1))
        db.commit()
        print('Appointment successfully booked!')
        print('Appointment date:',l[ch3-1])
        print('Appointment time: 6.00 pm')
        print('Token number:',fe[0][0]+1)


def app(eid):
     cur.execute('select pid,date,time,token from appointment where empid=%s;',(eid,))
     x=cur.fetchall()
     if x!=[]:
         print('Your future appointments:')
         h=['Pid','Date','Time','Token']
         v=[i for i in x]
         print(tabulate(v,h,tablefmt='grid'))
     else:
         print('You do not have any appointments!')


def status(pid):
    cur.execute('select test,status from lab where pid=%s;',(pid,))
    x=cur.fetchall()
    if x!=[]:
        print('Your lab results:')
        h=['test','status']
        v=[i for i in x]
        print(tabulate(v,h,tablefmt='grid'))
    else:
        print('You do not have any results pending')

def addpatient():
    print('Fill the below details to register as a patient:')
    name=input('Enter your name :')
    age=input('Enter age :')
    gen=input('Enter gender(m/f) :')
    email=input('Enter your email address :')
    phno=input('Enter your contact number :')
    pid='p'+str(random.randint(1000,9999))
    cur.execute('select pid from patient;')
    x=cur.fetchall()
    while (pid,) in x:
        pid='p'+str(random.randint(1000,9999))
    password=s.getpass('\nEnter your password:')
    cur.execute('select password from patient;')
    x=cur.fetchall()
    while (password,) in x:
        print('\nSorry you can\'t use this password!')
        password=s.getpass('Enter another password:')        
    cur.execute('insert into patient(pid,name,age,gender,email,phno,password) values(%s,%s,%s,%s,%s,%s,%s);',(pid,name,age,gen,email,phno,password))
    db.commit()
    print('\nYou have successfully registered with DHANVANTRI hospitals\nThank you for joining with us!\n\nYour user id is',pid,'\n please use this id to avail our services.')

#__main__

cur.execute('select med_name,price from med_shop;')
x=cur.fetchall()
med_cost={}
for i in x:
    med_cost[i[0]]=i[1]


cur.execute('select test_name,price from lab_test;')
x=cur.fetchall()
test_cost={}
for i in x:
    test_cost[i[0]]=i[1]

#admins
admin={'gvr':'vivek','ts':'ananda'}

cur.execute('update lab set status="On process" where date=curdate() and time<=curtime();')
db.commit()
cur.execute('update lab set status="Results ready" where curdate()=date_add(date,interval 3 day);')
db.commit()
cur.execute('delete from appointment where date<curdate();')
db.commit()

while True:
    print('''                   DHANVANTRI HOSPITAL
------Main Menu------
1.Register as patient
2.Login as Patient
3.Login as Doctor
4.Login as Admin
5.Facilities offered
6.View department wise doctors
7.Exit''')
    ch=int(input('\nEnter your choice:'))
    os.system('cls')
    if ch==2:
        pa=s.getpass('\nPlease enter your password:')
        cur.execute('select password from patient;')
        if (pa,) in cur.fetchall():
            print('successfully logged in!')
            cur.execute('select pid from patient where password=%s;',(pa,))
            pid=cur.fetchone()[0]
            while True:
                print('''\n-------Patient Menu-------
1.Book appointment
2.View your medical history
3.Your future appointments
4.View lab results
5.Exit''')
                ch1=int(input('\nEnter your choice:'))
                os.system('cls')
                if ch1==1:
                    bkap(pid)
                elif ch1==2:
                    cur.execute('select name,chronic from patient where pid=%s;',(pid,))
                    w=cur.fetchall()
                    name,cro=w[0][0],w[0][1]
                    cur.execute('select date,name,disease,tablets_prescribed,tests_prescribed,cdcount from history,employee where pid=%s and history.empid=employee.empid;',(pid,))
                    x=cur.fetchall()
                    print('Patient id:',pid)
                    print('Patient Name:',name)
                    print('Chronic diseases patient has:',cro)
                    print('Your medical history:')
                    if x!=[]:
                        h=['Date','Doc_name','disease','tablets_prescribed','tests_prescribed','cdcount']
                        v=[i for i in x]
                        print(tabulate(v,h,tablefmt='grid'))                       
                    else:
                        print('you have no history with this hospital')
                elif ch1==3:
                    cur.execute('select name as doc_name,date,time,token from appointment,employee where pid=%s and appointment.empid=employee.empid ;',(pid,))
                    x=cur.fetchall()
                    if x!=[]:
                        print('Your future appointments:')
                        h=['Doctor_name','Date','Time','Token']
                        v=[i for i in x]
                        print(tabulate(v,h,tablefmt='grid'))                        
                    else:
                        print('You do not have any future appointments!') 
                elif ch1==4:
                    status(pid)
                elif ch1==5:
                    break
                else:
                    print('Invalid choice!')
        else:
            print('Error! Please check your login credentials.')


    elif ch==3:
        pa=s.getpass('\nPlease enter your password:')
        cur.execute('select password from employee where dept!="staff";')
        if (pa,) in cur.fetchall():
            print('successfully logged in!')
            cur.execute('select empid,cpa from employee where password=%s;',(pa,))
            x=cur.fetchone()
            eid,cpa=x[0],x[1]
            while True:
                print('''\n-------Doctor Menu-------
1.See your appointments
2.Attend Patient
3.Exit''')
                ch2=int(input('\nEnter your choice :'))
                os.system('cls')
                if ch2==1:
                    app(eid)
                elif ch2==2:
                    x=input('Enter patient id :')
                    cur.execute('select pid,empid from appointment where date=curdate();')
                    if (x,eid) in cur.fetchall():
                        file=open("C:\\Users\\vivek\\AppData\\Local\\Programs\\Python\\Python36-32\\hospital\\bills\\"+x+'_'+str(date.today())+'.txt','w')
                        cur.execute('select name from patient where pid=%s;',(x,))
                        file.write( '''              DHANVANTRI HOSPITAL
No.8, Anna Salai Chennai-600002 Contact no: 044-8542 5824
Name of patient: '''+cur.fetchall()[0][0]+'''
Patient_id: '''+x+'''
Date: '''+str(date.today())+'''
-------------------------------------------------------------------------
    Item description/Activity                      Cost
         Checkup Charges                          Rs.'''+str(cpa))
                        tot=cpa
                        cur.execute('select chronic from patient where pid=%s;',(x,))
                        y=cur.fetchall()[0][0]
                        if y==None:
                            y=input('\nNew patient!!\nEnter chronic diseases patient has (comma seperated):')
                            cur.execute('update patient set chronic=%s where pid=%s;',(str(y),x))
                            db.commit()
                            print('chronic diseases has been successfully updated!')
                        print('\nChronic disease patient have ',y.split(','))
                        print('Enter the below details:')
                        w=input('Enter weight  :')
                        h=input('Enter height :')
                        d=input('Enter Diseases diagnosed with(space seperated):').split()
                        t=input('Enter medicines prescribed (space seperated):').lower().split()
                        nos=input('Enter no. of medicines space seperated respectively  :').lower().split()
                        while len(t)!=len(nos):
                            nos.append(1)
                        lis=[]
                        for i in t:
                            if i not in med_cost.keys():
                                nos.remove(nos[t.index(i)])
                                t.remove(i)
                                lis.append(i)
                        cd=[input('Enter '+i+' count:') for i in y.split(',')]
                        tab_cost=[med_cost[i] for i in t ]
                        total=sum([tab_cost[i]*int(nos[i]) for i in range(len(nos))])
                        tot+=total
                        for i in range(len(nos)):
                            cur.execute('update med_shop set stock=stock-%s where med_name=%s;',(nos[i],t[i]))
                            db.commit()
                        
                        file.write('\n         Pharmacy charges                         Rs. '+str(total))
                        ch3=input('\nDo you want to book lab test for patient?(y/n)')
                        if ch3=='y':
                            test=input('\nEnter tests space seperated:').lower().split()
                            try:
                                lab_cost=sum([test_cost[i] for i in test])
                                date=input('Enter date for test(yyyy-mm-dd) :')
                                time=input('Enter time(hh:mm):')+':00'
                                tot+=lab_cost
                                cur.execute('insert into lab values(%s,%s,%s,%s,%s,"booked",%s);',(x,eid,str(test),date,time,lab_cost))
                                db.commit()
                                file.write('\n         Laboratory charges                       Rs. '+str(lab_cost))
                                print('Tests successfully booked!')
                            except:
                                    print('These tests not available in our lab!!')
                                    print('Please refer external lab for these tests')
                                    print('Tests:',test)
                                    print('Sorry for inconvenience!!')
                                                                                           
                            cur.execute('insert into history values(%s,%s,curdate(),curtime(),%s,%s,%s,%s,%s,%s);',(eid,x,str(d),str(t+lis),str(test),h,w,str(cd)))
                            db.commit()
                        else:
                            cur.execute('insert into history values(%s,%s,curdate(),curtime(),%s,%s,"none",%s,%s,%s);',(eid,x,str(d),str(t+lis),h,w,str(cd)))
                            db.commit()
                        file.write('\n         TOTAL:                                   Rs. '+str(tot))
                        file.close()
                        cur.execute('delete from appointment where pid=%s and date=curdate() and empid=%s;',(x,eid))
                        db.commit()
                    else:
                        print('You do not have an appointment with this patient today.')
                elif ch2==3:
                    break
                else:
                    print('Wrong input!')
        else:
            print('Error! Please check your login credentials.')


    elif ch==1:
        addpatient()
    elif ch==5:
        file=open('dhanvantri_hospital.txt')
        print(file.read())
    elif ch==6:
        cur.execute('select distinct dept from employee where dept!="staff" and job="doc";')
        x=cur.fetchall()
        print('\nChoose Department:')
        for i in range(len(x)):
            print(str(i+1)+'.'+x[i][0])
        ch4=int(input('Enter your choice :'))
        h=['Doctors']        
        cur.execute('select name from employee where dept=%s;',(x[ch4-1][0],))
        x=cur.fetchall()
        v=[i for i in x]
        print(tabulate(v,h,tablefmt='grid'))        
    elif ch==7:
        break


    elif ch==4:
        i=input('Enter Admin id  :')
        p=s.getpass('Enter password :')
        if (i,p) in admin.items():
            print('Sucessfully logged in..')
            while True:
                print('''\n-------Admin Menu-------
1.Generate bill
2.Manage patients
3.Manage employees
4.Medical Shop
5.Lab
6.Exit''')
                ch5=int(input('Enter your choice:'))
                os.system('cls')
                if ch5==1:
                    pid=input('Enter patient id :')
                    cur.execute('select pid from patient;')
                    x=cur.fetchall()
                    if (pid,) in x:
                        try:
                            file=open("C:\\Users\\vivek\\AppData\\Local\\Programs\\Python\\Python36-32\\hospital\\bills\\"+pid+'_'+str(date.today())+'.txt')
                            print('\nBill successfully generated!\nIt is named as '+pid+'_'+str(date.today())+'.txt in bills folder!')
                            file.close()
                        except:
                            print('\nNo bill remaining for patient id '+pid)
                    else:
                        print('Invalid patient Id!')
                elif ch5==2:
                    print('''\n-------Patient management-------
  Select an option:
1.Book appointment for patient
2.Remove patient
3.Exit''')
                    ch6=int(input('Enter your choice:'))
                    os.system('cls')
                    if ch6==1:
                        pid=input('Enter patient id :')
                        bkap(pid)
                    elif ch6==2:
                        pid=input('Enter patient id :')
                        cur.execute('delete from patient where pid=%s;',(pid,))
                        db.commit()
                        print('Patient Successfully removed!')
                    else:
                        pass
                elif ch5==3:
                    print('''\n-------Employee management-------
  Select an option:
1.View appointments of doctor
2.Add employee
3.Remove employee
4.Exit''')
                    ch7=int(input('Enter your choice:'))
                    os.system('cls')
                    if ch7==1:
                        eid=input('Enter employee id:')
                        app(eid)
                    elif ch7==2:
                        
                        name=input('Enter  name :')
                        age=input('Enter age :')
                        gen=input('Enter gender(m/f) :')
                        email=input('Enter  email address:')
                        phno=input('Enter  contact number :')
                        dep=input('Enter department :')
                        jo=input('Enter job(eg:doc,cle etc.,) :')
                        wd=input('Enter Working day index space seperated(mon-0,tue-1......sun-6):')
                        sal=int(input('Enter salary :'))
                        eid='e'+str(random.randint(1000,9999))
                        cur.execute('select empid from employee;')
                        x=cur.fetchall()
                        while (eid,) in x:
                            eid='e'+str(random.randint(1000,9999))
                        password=s.getpass('Enter your password :')
                        cur.execute('select password from employee;')
                        x=cur.fetchall()
                        while (password,) in x:
                            print('Sorry you can\'t use this password')
                            password=s.getpass('Enter another password :')
                        if jo=='doc':
                            cpa=input('Enter Doctor fee per appointment :')  
                            cur.execute('insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',(eid,name,age,gen,email,phno,password,dep,jo,wd,sal,cpa))
                            db.commit()
                        else:
                            cur.execute('insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0);',(eid,name,age,gen,email,phno,password,dep,jo,wd,sal))
                            db.commit()
                        print('Employee successfully added!\nEmployee id is: '+eid)
                                                
                    elif ch7==3:
                        eid=input('Enter employee id:')
                        x=input('Are you sure in removing employee??(y/n):')
                        if x=='y':
                            cur.execute('delete from employee where empid=%s;',(eid,))
                            db.commit()
                            print('Employee successfully removed!')
                        else:
                            print('Employee not removed!!')
                    else:
                        pass
                elif ch5==4:
                    print(('''\n-------Medical shop Menu-------
  Select an option:
1.Add new medicines
2.Update stock
3.Update price of a medicine
4.Exit'''))
                    ch8=int(input('Enter your choice :'))
                    os.system('cls')
                    if ch8==1:
                        mid=input('Enter medicine id :')
                        mname=input('Enter medicine name :').lower()
                        st=int(input('Enter nos :'))
                        price=int(input('Enter price of 1 nos medicine  :'))
                        cur.execute('insert into med_shop values(%s,%s,%s,%s);',(mid,mname,st,price))
                        db.commit()
                        print('Medicine Successfully added!')
                        med_cost[mname]=price
                    elif ch8==2:
                        mid=input('Enter medicine id :')
                        cur.execute('select mid from med_shop;')
                        x=cur.fetchall()
                        if (mid,) in x:
                            st=int(input('Enter nos added :'))
                            cur.execute('update med_shop set stock=stock+%s where mid=%s;',(st,mid))
                            db.commit()
                            print('\nStock updated!')
                        else:
                            print('\nInvalid medicine id')
                    elif ch8==3:
                        mid=input('Enter medicine id :')                        
                        cur.execute('select mid from med_shop;')
                        x=cur.fetchall()
                        if (mid,) in x:
                            st=int(input('Enter new price  :'))
                            cur.execute('update med_shop set price=%s where mid=%s;',(st,mid))
                            db.commit()
                            print('\nprice updated!')
                            cur.execute('select med_name from med_shop where mid=%s;',(mid,))
                            mname=cur.fetchall()[0][0]
                            med_cost[mname]=st
                        else:
                            print('\nInvalid medicine id!')
                    else:
                        pass
                elif ch5==5:
                    print('''\n-------Laboratory menu-------
  Select an option:
1.Check results
2.Update price for a test
3.Add test
4.Exit''')
                    ch9=int(input('Enter your choice:'))
                    os.system('cls')
                    if ch9==1:
                        pid=input('Enter patient id :')
                        status(pid)
                    elif ch9==2:
                        n=input('Enter test name :').lower()
                        if n in test_cost:
                            p=int(input('Enter new price :'))
                            test_cost[n]=p
                            cur.execute('update lab_test set price=%s where test_name=%s;',(p,n))
                            db.commit()
                            print('\nprice updated successfully')
                        else:
                            print('\nInvalid Test name!')
                    elif ch9==3:
                        n=input('Enter test name  :').lower()
                        p=int(input('Enter new price  :'))
                        test_cost[n]=p
                        cur.execute('insert into lab_test values(%s,%s);',(n,p))
                        db.commit()
                        print('\nTest added successfully!')
                    else:
                        pass
                elif ch5==6:
                    break
                else:
                    print('invalid input!')
        else:
            print('Please check your login credentials!')
    else:
        print('Wrong input!')                 
db.close()                                
                        
                    
                    
                        
                        
                        
                    
                        
                    
                        
                        


                                  
        


