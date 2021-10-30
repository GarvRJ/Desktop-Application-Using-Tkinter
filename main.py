import datetime
import platform
from tkinter import *
from tkinter.ttk import Notebook

try:
    import winsound

    tpe = 'windows'


except:
    import os

    tpe = 'other'

window = Tk()
window.title("Clock")
window.geometry('500x350')
stopwatch_counter_num = 66600
stopwatch_running = False
timer_counter_num = 66600
timer_running = False


def clock():
    date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S/%p")
    date, time1 = date_time.split()
    time2, time3 = time1.split('/')
    hour, minute, second = time2.split(':')
    if 11 < int(hour) < 24:
        time = str(int(hour) - 12) + ':' + minute + ':' + second + ' ' + time3
    else:
        time = time2 + ' ' + time3
    time_label.config(text=time)
    date_label.config(text=date)
    time_label.after(1000, clock)


def alarm():
    main_time = datetime.datetime.now().strftime("%H:%M:%S")

    def apm(atime2):
        if atime2 == 'AM':
            return 0
        else:
            return 1

    set_alarm_time = f"{str(int(alarm_hour.get()) + apm(alarm_time2.get()) * 12)}:{alarm_minutes.get()}:{alarm_second.get()} "
    if main_time == set_alarm_time:
        alarm_status_label.config(text='Alarm Sounding....')
        for i in range(3):
            alarm_status_label.config(text='Time Is Up')
            if platform.system() == 'Windows':
                winsound.Beep(5000, 1000)
            elif platform.system() == 'Darwin':
                os.system('say Time is Up')
            elif platform.system() == 'Linux':
                os.system('beep -f 5000')
        set_alarm_Button.config(state='active')
    elif set_alarm_time >= main_time:
        alarm_status_label.config(text='Alarm Started')
        set_alarm_Button.config(state='disabled')
    else:
        alarm_status_label.config(text='Use above dropdown to set alarm')
        set_alarm_Button.config(state='active')
    alarm_status_label.after(100, alarm)


def stopwatch_counter(label):
    def count():
        if stopwatch_running:
            global stopwatch_counter_num
            if stopwatch_counter_num == 66600:
                disp = "Starting..."
            else:
                tt = datetime.datetime.fromtimestamp(stopwatch_counter_num)
                string = tt.strftime("%H:%M:%S")
                disp = string
            label.config(text=disp)
            label.after(1000, count)
            stopwatch_counter_num += 1

    count()


def stopwatch(work):
    if work == 'start':
        global stopwatch_running
        stopwatch_running = True
        stopwatch_start.config(state='disabled')
        stopwatch_stop.config(state='active')
        stopwatch_reset.config(state='active')
        stopwatch_counter(stopwatch_label)
    elif work == 'stop':
        stopwatch_running = False
        stopwatch_start.config(state='active')
        stopwatch_stop.config(state='disabled')
        stopwatch_reset.config(state='active')
    elif work == 'reset':
        global stopwatch_counter_num
        stopwatch_running = False
        stopwatch_counter_num = 66600
        stopwatch_label.config(text='Stopwatch')
        stopwatch_start.config(state='active')
        stopwatch_stop.config(state='disabled')
        stopwatch_reset.config(state='disabled')


def timer_counter(label):
    # noinspection PyGlobalUndefined
    def count():
        global timer_running, display
        if timer_running:
            global timer_counter_num
            if timer_counter_num == 66600:
                for i in range(3):
                    display = "Time Is Up"
                    if platform.system() == 'Windows':
                        winsound.Beep(5000, 1000)
                    elif platform.system() == 'Darwin':
                        os.system('say Time is Up')
                    elif platform.system() == 'Linux':
                        os.system('beep -f 5000')
                timer_running = False
                timer('reset')
            else:
                tt = datetime.datetime.fromtimestamp(timer_counter_num)
                string = tt.strftime("%H:%M:%S")
                display = string
                timer_counter_num -= 1
            label.config(text=display)
            label.after(1000, count)

    count()


def timer(work):
    if work == 'start':
        global timer_running, timer_counter_num
        timer_running = True
        if timer_counter_num == 66600:
            hour_t = int(timer_hour.get())
            minutes_t = int(timer_minutes.get()) + (int(hour_t) * 60)
            seconds_t = int(timer_second.get()) + (minutes_t * 60)
            timer_counter_num = timer_counter_num + seconds_t
        timer_counter(timer_label)
        timer_start.config(state='disabled')
        timer_stop.config(state='active')
        timer_reset.config(state='active')
    elif work == 'stop':
        timer_running = False
        timer_start.config(state='active')
        timer_stop.config(state='disabled')
        timer_reset.config(state='active')
    elif work == 'reset':
        timer_running = False
        timer_counter_num = 66600
        timer_start.config(state='active')
        timer_stop.config(state='disabled')
        timer_reset.config(state='disabled')
        timer_label.config(text='Timer')


tabs_control = Notebook(window)
clock_tab = Frame(tabs_control)
alarm_tab = Frame(tabs_control)
frame_a = Frame(alarm_tab)
frame_a.place(relx=.5, rely=.3, anchor='center')
stopwatch_tab = Frame(tabs_control)
timer_tab = Frame(tabs_control)
timer_tab.place(relx=.5, rely=.5, anchor='c')
frame_t = Frame(timer_tab)
frame_t.place(relx=0.5, rely=.1, anchor='c')
tabs_control.add(clock_tab, text="Clock")
tabs_control.add(alarm_tab, text="Alarm")
tabs_control.add(stopwatch_tab, text='Stopwatch')
tabs_control.add(timer_tab, text='Timer')
tabs_control.pack(expand=1, fill="both")
time_label = Label(clock_tab, font='calibri 40 bold', foreground='black')
time_label.place(relx=.5, rely=.3, anchor='center')
date_label = Label(clock_tab, font='calibri 40 bold', foreground='black')
date_label.place(relx=.5, rely=.7, anchor='center')
alarm_hour = StringVar(alarm_tab)
hours = ('00', '01', '02', '03', '04', '05', '06', '07',
         '08', '09', '10', '11', '12'
         )
alarm_hour.set(hours[0])
a_hrs = OptionMenu(frame_a, alarm_hour, *hours)
a_hrs.pack(side=LEFT)
alarm_minutes = StringVar(alarm_tab)
minutes = ('00', '01', '02', '03', '04', '05', '06', '07',
           '08', '09', '10', '11', '12', '13', '14', '15',
           '16', '17', '18', '19', '20', '21', '22', '23',
           '24', '25', '26', '27', '28', '29', '30', '31',
           '32', '33', '34', '35', '36', '37', '38', '39',
           '40', '41', '42', '43', '44', '45', '46', '47',
           '48', '49', '50', '51', '52', '53', '54', '55',
           '56', '57', '58', '59', '60')
alarm_minutes.set(minutes[0])
a_mins = OptionMenu(frame_a, alarm_minutes, *minutes)
a_mins.pack(side=LEFT)
alarm_second = StringVar(alarm_tab)
seconds = ('00', '01', '02', '03', '04', '05', '06', '07',
           '08', '09', '10', '11', '12', '13', '14', '15',
           '16', '17', '18', '19', '20', '21', '22', '23',
           '24', '25', '26', '27', '28', '29', '30', '31',
           '32', '33', '34', '35', '36', '37', '38', '39',
           '40', '41', '42', '43', '44', '45', '46', '47',
           '48', '49', '50', '51', '52', '53', '54', '55',
           '56', '57', '58', '59', '60')
alarm_second.set(seconds[0])
a_sec = OptionMenu(frame_a, alarm_second, *seconds)
a_sec.pack(side=LEFT)
alarm_time2 = StringVar(alarm_tab)
ap = ('AM', 'PM')
alarm_time2.set(ap[0])
aps = OptionMenu(frame_a, alarm_time2, *ap)
aps.pack(side=LEFT)
set_alarm_Button = Button(alarm_tab, text="Set Alarm", command=alarm)
set_alarm_Button.place(relx=.5, rely=.5, anchor='center')
alarm_status_label = Label(alarm_tab, font='calibri 15 bold')
alarm_status_label.place(relx=.5, rely=.7, anchor='center')
stopwatch_label = Label(stopwatch_tab, font='calibri 40 bold', text='Stopwatch')
stopwatch_label.place(relx=.5, rely=.1, anchor='center')
stopwatch_start = Button(stopwatch_tab, text='Start', command=lambda: stopwatch('start'))
stopwatch_start.place(relx=.5, rely=.3, anchor='center')
stopwatch_stop = Button(stopwatch_tab, text='Stop', state='disabled', command=lambda: stopwatch('stop'))
stopwatch_stop.place(relx=.5, rely=.6, anchor='center')
stopwatch_reset = Button(stopwatch_tab, text='Reset', state='disabled', command=lambda: stopwatch('reset'))
stopwatch_reset.place(relx=.5, rely=.9, anchor='center')
timer_hour = StringVar(frame_t)
timer_hour.set(hours[0])
t_hrs = OptionMenu(frame_t, timer_hour, *hours)
t_hrs.pack(side=LEFT)
timer_minutes = StringVar(frame_t)
timer_minutes.set(minutes[0])
t_mins = OptionMenu(frame_t, timer_minutes, *minutes)
t_mins.pack(side=LEFT)
timer_second = StringVar(frame_t)
timer_second.set(seconds[0])
t_sec = OptionMenu(frame_t, timer_second, *seconds)
t_sec.pack(side=LEFT)
timer_label = Label(timer_tab, font='calibri 40 bold', text='Timer')
timer_label.place(relx=.5, rely=.3, anchor='center')
timer_start = Button(timer_tab, text='Start', command=lambda: timer('start'))
timer_start.place(relx=.5, rely=.5, anchor='center')
timer_stop = Button(timer_tab, text='Stop', state='disabled', command=lambda: timer('stop'))
timer_stop.place(relx=.5, rely=.7, anchor='center')
timer_reset = Button(timer_tab, text='Reset', state='disabled', command=lambda: timer('reset'))
timer_reset.place(relx=.5, rely=.9, anchor='center')
clock()
window.mainloop()
