import schedule,os,platform
import time,datetime,csv
import tkinter.messagebox as msg



with open('details.csv', 'r') as file:
    csv_reader = csv.reader(file)
    flag=0

    for row in csv_reader:
        if flag==0:
                li = row
                flag=1
for proj in li[1:]:
    try:
        with open(str(proj)+".txt",'r+') as file:
            print("'" + str(proj) + ".txt'")
            mylist = []
            list_one=[]
            for line in file:
                mylist.append(line)
            mylist = mylist[0].split(',')
            print(len(mylist))
            for l in mylist:
                if not l =="":
                    t = l[2:10]
                    d = l[13:-2]
                    print(t,d)
                    schedule.every().day.at(t).do(lambda: f(d, t))


    except:
        pass



"""




with open('MED.txt','r+') as file:
    mylist = []
    list_one=[]
    for line in file:
        mylist.append(line)
    mylist = mylist[0].split(',')
    print(len(mylist))
    for l in mylist:
        if not l =="":
            t = l[2:10]
            d = l[13:-1]
            schedule.every().day.at("18:43").do(lambda: f(d, t))




with open('DUF.txt','r+') as file:
    mylist = []
    list_one=[]
    for line in file:
        mylist.append(line)
    print(mylist)
    mylist = mylist[0].split(',')
    #print(mylist)
    for l in mylist:
        if not l=="":
            t = l[2:10]
            d = l[13:-1]
            schedule.every().day.at(l[2:10]).do(lambda :f(d,t))


"""

def f(d,t):
    if platform.system() == 'Linux':
        os.system("notify-send '" + str(d) +" at " + str(t) +"'" )
    elif platform.system() == 'Windows':
        os.system('msg "%username%" you have a task '+ str(d) +" at " + str(t) +" ")
        pass



while True:
    schedule.run_pending()
    time.sleep(1)

