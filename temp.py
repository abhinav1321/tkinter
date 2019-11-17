from tkinter import *

from tkinter import ttk

import tkinter.messagebox

import os

import schedule

import time

import csv, datetime, calendar

the_user = []

month_date = []

with open('details.csv', 'r+') as detail_file:
    csv_reader = csv.reader(detail_file)

    final = []

    line1 = True

    for index, row in enumerate(csv_reader):

        if line1:

            line1 = FALSE

            continue



        else:

            user = {

                'uid': row[0],

                'DUF': row[1],

                'FOX': row[2],

                'MED': row[3],

                'VFS': row[4],

                'XL': row[5],

                'XE': row[6],

                'SA': row[7]

            }

            final.append(user)

    for f in final:
        the_user.append(f['uid'])


def get_rota(date):
    formatted = datetime.datetime.strptime(date, '%d/%m/%Y')

    month, year = int(formatted.strftime('%m')), int(formatted.strftime('%Y'))

    num_days = calendar.monthrange(year, month)[1]

    # print(num_days)

    with open('rota.csv', 'r+') as rota:

        csv_reader1 = csv.reader(rota)

        final_data = []

        line1 = True

        for index, row in enumerate(csv_reader1):

            shift_list = []

            less_index = index - 1

            if line1:
                line1 = False

                continue

            for d in range(num_days - 1):
                shift_list.append(row[d + 1])

            # print(row[0])

            Sh = {'uid': row[0], 'rota': shift_list}

            final_data.append(Sh)

            # print(final_data)

    return (final_data)


def get_proj(user_id='584037'):
    for line in final:

        if line['uid'] == user_id:
            projects = [key for key, value in line.items() if value == '1']

            # print(projects)

            return projects


def get_task_list(project):
    try:

        # file name should be first 3 letters(capital) of project like "DUF-Task.csv"

        file_name = str(project) + '-Task.csv'

        # print(file_name)

        with open(file_name, 'r+') as pfile:

            csv_reader_project = csv.reader(pfile)

            ptaklist = []

            line1 = True

            for index, row in enumerate(csv_reader_project):

                if line1:
                    line1 = False

                    continue

                ptaklist.append(row)

            # print((ptaklist))

            # timelist will be iteration of every 15 mins in a day- i.e 24*15= 96 , thats why range(95) used in below code

            timelist = []

            a = datetime.time(0, 0)

            timelist.append(a)

            for i in range(95):
                b = datetime.timedelta(minutes=15)

                a = (datetime.datetime.combine(datetime.date(1, 1, 1), a) + b).time()

                timelist.append(a)

            actual_list = []

            # len(ptaklist is 7 as day of week)

            for i in range(len(ptaklist)):

                day_list = []

                for j in range(95):

                    if not ptaklist[i][j] == '':
                        task_dict = {

                            timelist[j]: ptaklist[i][j]

                        }

                        day_list.append(task_dict)

                actual_list.append(day_list)

            # print(actual_list)

            return (actual_list, project)





    except:

        # print('Info not Avl for ',project)

        return ('Info not Avl for ', project)

        # actual list is the whole task list for a week per day, datetime(0,0) has the name of the day

        # print(actual_list)


window = Tk()

window.geometry("900x600")

user_detail = []


def notif(last):
    timings = last[0]

    tasks = last[1]

    project = last[2]

    for i in range(len(project)):
        f = open(str(project[i]) + '.txt', 'w')

        f.write('')

        f.close()

    for i in range(len(timings)):

        if not timings[i] == 'No Data for the Project of ' and not tasks[i] == 'OFF':
            f = open(str(project[i]) + '.txt', 'a')

            to_enter = '{' + "'" + str(timings[i]) + "'" + ':'  + "'" + str(tasks[i]) + "'" + '}'

            f.write(to_enter + ',')

            f.close()

    Label(window, text="Info Sent to Task Scheduler").grid(row=15, column=5)

    os.system('python notif.py')


def action():
    for i in range(50):
        Label(window, text='                                                                   ').grid(row=10 + i,
                                                                                                       column=1)

        Label(window, text='                                                                   ').grid(row=10 + i,
                                                                                                       column=3)

        Label(window, text='                                                                    ').grid(row=10 + i,
                                                                                                        column=5)

    got_uid = user_id_selected.get()

    day = d_selected.get()

    month = m_selected.get()

    year = y_selected.get()

    date = day + '/' + month + '/' + year

    got_date = date

    # print(date)

    if got_date == '':

        Label(window, text="Please Enter Date").grid(row=10, columnspan=5)



    else:

        rota = get_rota(date)

        # if user has not entered id

        if got_uid == '':

            counter = 0

            for item in rota:
                Label(window).grid(row=13, )

                Label(window, text='EMPLOYEE').grid(row=14, column=1)

                Label(window, text='SHIFT').grid(row=14, column=3)

                # if no user is given gui will show user name : the shift at current date

                # item['rota'] => get_rota() returns a dict with keys uid and rota

                to_show = [(str(the_user[counter])) + ' : ' + item['rota'][int(day) - 1]]

                id_label = Label(window, text=(str(the_user[counter]))).grid(row=(counter + 15), column=1)

                shift_label = Label(window, text=item['rota'][int(day) - 1]).grid(row=(counter + 15), column=3)

                counter = counter + 1



        else:

            for item in rota:

                if item['uid'] == got_uid:

                    shift = item['rota'][int(day) - 1]

                    # print(shift)

                    weekly_task_list = []

                    ids = get_proj(got_uid)

                    for i in ids:
                        w = get_task_list(i)

                        weekly_task_list.append(w)

                    # print('the weekly task',weekly_task_list)

                    last = the_last(shift, weekly_task_list, date)

                    # print(last)

                    n = 0

                    fc = last[0]

                    sc = last[1]

                    pc = last[2]

                    for i in range(len(fc)):
                        Label(window, text=fc[i]).grid(row=i + 10, column=1)

                        Label(window, text=sc[i]).grid(row=i + 10, column=3)

                        Label(window, text=pc[i]).grid(row=i + 10, column=5)

                    Notification = Button(window, text="Set Notification for " + str(got_uid),
                                          command=lambda: notif(last)).grid(row=i + 15, column=3)


def the_last(shift, weelky_task_list, date):
    timings = []

    proj = []

    tasks = []

    the_task = ''

    week_day = datetime.datetime.strptime(date, '%d/%m/%Y')

    day_of_week = calendar.day_name[week_day.weekday()]

    task_list = weelky_task_list

    week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

    for v in task_list:

        # print('fhuisdgvrevbfuidovhfuidvh',v)

        if v[0] == 'Info not Avl for ':

            # print('yes')

            timings.append('No Data for the Project of '), tasks.append(v[1]), proj.append(v[1])

            continue





        else:

            vi = v[0]

            p = v[1]

            for i in range(7):

                if day_of_week == week[i]:
                    # print(day_of_week)

                    # print('kes see',v)

                    the_task = vi[i]

                    # print('the Task are ',the_task)

        if shift == 'WO' or shift == 'L':

            timings.append('NONE'), tasks.append('OFF'), proj.append(p)





        elif shift == 'M':

            for t in the_task:

                for k, v in t.items():

                    if not v is None:

                        if k < datetime.time(15, 45) and k > datetime.time(7, 0):
                            timings.append(k), tasks.append(v), proj.append(p)









        elif shift == 'A':

            for t in the_task:

                for k, v in t.items():

                    # print('As values',v)

                    if not v is None:

                        if k > datetime.time(15, 45) and k < datetime.time(22, 0):
                            timings.append(k), tasks.append(v), proj.append(p)

                            # print(tasks)







        elif shift == 'N':

            for t in the_task:

                for k, v in t.items():

                    if not v is None:

                        if k < datetime.time(23, 45) and k > datetime.time(22, 0):
                            timings.append(k), tasks.append(v), proj.append(p)

                        if k > datetime.time(0, 0) and k < datetime.time(7, 0):
                            timings.append(k), tasks.append(v), proj.append(p)

    if len(timings) > 0:
        # z=zip(timings,tasks)

        # print("jyfuy",tasks)

        return timings, tasks, proj


user_id_selected = StringVar()

days = str(list(range(32)[1:])).replace(',', '').replace('[', '').replace(']', '')

month = str(list(range(13)[1:])).replace(',', '').replace('[', '').replace(']', '')

year = str(list(range(2019, 2021))).replace(',', '').replace('[', '').replace(']', '')

Label(window, text="Select User").grid(row=1, column=1)

Label(window, text="Select date of current month").grid(row=2, column=1)

Label(window, text=' Turn on Notification').grid(row=3, column=1)

user_id = ttk.Combobox(window, width=8, textvariable=user_id_selected, value=the_user, state='readonly')

d_selected = StringVar()

m_selected = StringVar()

y_selected = StringVar()

d = ttk.Combobox(window, width=4, textvariable=d_selected, value=days, state='readonly')

m = ttk.Combobox(window, width=4, textvariable=m_selected, value=month, state='readonly')

y = ttk.Combobox(window, width=6, textvariable=y_selected, value=year, state='readonly')

d.grid(row=2, column=2)

m.grid(row=2, column=3)

y.grid(row=2, column=4)

user_id.grid(row=1, column=2)

submit = Button(window, text="Submit", command=action).grid(row=6, column=2)

window.mainloop()

# tkinter messagebox code--------------------------------------------------------


'''

import Tkinter

import tkMessageBox

top = Tkinter.Tk()

def hello():

   tkMessageBox.showinfo("Say Hello", "Hello World")

B1 = Tkinter.Button(top, text = "Say Hello", command = hello)

B1.pack()

top.mainloop()

# tkinter running a job code

'''