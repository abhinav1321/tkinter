import schedule
import time,json
import tkinter.messagebox as msg
import json,ast






with open('MED.txt','r+') as file:
    mylist = []
    list_one=[]
    for line in file:
        mylist.append(line)
    mylist = mylist[0].split(',')
    #print(mylist)
    for l in mylist:
        t = l[2:10]
        d = l[13:-1]
        print(t, d)
        schedule.every().day.at(t).do(lambda: msg.showinfo(d, t))




with open('DUF.txt','r+') as file:
    mylist = []
    list_one=[]
    for line in file:
        mylist.append(line)
    print(mylist)
    mylist = mylist[0].split(',')
    #print(mylist)
    for l in mylist:

        t = l[2:10]
        d = l[13:-1]
        print(t,d)
        schedule.every().day.at(t).do(lambda :msg.showinfo(d,t))

while True:
    schedule.run_pending()
    time.sleep(1)

