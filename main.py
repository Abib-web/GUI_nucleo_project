import datetime as dt
from time import sleep

import pandas as pd
import serial
import matplotlib.pyplot as plot
import csv
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ser = serial.Serial()
seconds = []
ys = []
xs = []
zs = []
temp = []
hum = []


def init_com():
    serial.Serial('COM12', 115200, timeout=10000)
    ser.flush()
    ser.close()


def open_port():
    ser.open()


def close_port():
    ser.close()


def receiveData():
    if ser.isOpen():
        try:
            if ser.in_waiting > 0:
                donnes.configure(text="data.get()")
                line = ser.readline().decode('utf-8')
                data.set(line)
                if line[0] == "T":
                    data.set(" ")
                    donnes.configure(text=data.get())
                    data.set(line)
                else:
                    donnes.configure(text=data.get())
                    write_in_cvs(line)
                    curve()
        except ValueError:
            print(ValueError.with_traceback())
            click_fun()
    else:
        pass
    root.after(1000, receiveData)


def choice():
    pop.destroy()


def click_fun():
    global pop
    pop = Toplevel(root)
    pop.title("Erreur")
    pop.geometry("300x150")
    pop.config(bg="white")
    # Create a Label Text
    label = Label(pop, text="Veuillez ouvrir le port svp?",
                  font=('Aerial', 12))
    label.pack(pady=20)
    # Add a Frame
    frame = Frame(pop, bg="gray71")
    frame.pack(pady=10)
    # Add Button for making selection
    button1 = Button(frame, text="Ok", command=lambda: choice, bg="blue", fg="white")
    button1.grid(row=0, column=1)


fieldnames = ['Axis X', 'Axis Y', 'Axis Z', 'Temperature', 'Humidite']


def write_in_cvs(line):
    line = line.replace('|', ',')
    line = line.replace('\r', '')
    line = line.replace('\n', '')
    line = line.split(',')
    with open('data.csv', 'a', newline='') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvfile.seek(0, 2)
        if csvfile.tell() == 0:
            spamwriter.writeheader()
        spamwriter.writerow(
            {'Axis X': line[0], 'Axis Y': line[1], 'Axis Z': line[2], 'Temperature': line[3], 'Humidite': line[4]})


figure = plot.Figure(figsize=(6, 6), dpi=50)
figure2 = plot.Figure(figsize=(6, 6), dpi=50)
ax = figure.add_subplot(111)
ax2 = figure2.add_subplot(111)
ax.legend(['Les axes du gyroscope'])
ax.set_xlabel('Temps')
ax.set_title('Les axes du gyroscope')
ax2.legend(['HTU21D'])
ax2.set_xlabel('Temps')
ax2.set_title("La temperature et l'humidité")


def curve():
    update_cvs('Axis X', xs)
    update_cvs('Axis Y', ys)
    update_cvs('Axis Z', zs)
    update_cvs('Temperature', temp)
    update_cvs('Humidite', hum)
    seconds.append(int(dt.datetime.utcnow().timestamp()))
    ax.plot(seconds, xs, color='blue')
    ax.plot(seconds, ys, color='green')
    ax.plot(seconds, zs, color='yellow')
    ax2.plot(seconds, temp, color='black')
    ax2.plot(seconds, hum, color='red')
    chart_type.draw()
    chart_type2.draw()


def update_cvs(char, arr):
    reader = pd.read_csv("data.csv", usecols=fieldnames)
    listes = reader[char].tolist()
    listes = listes[-1]
    arr.append(listes)


def delete_cvs():
    filename = "data.csv"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()


def Togglebtn_Open():
    open_port()
    btnOpen_close["state"] = "disabled"
    btnClose_open["state"] = "normal"


def Togglebtn_Close():
    close_port()
    btnClose_open["state"] = "disabled"
    btnOpen_close["state"] = "normal"


def display_csv():
    col_names = ('Axis X', 'Axis Y', 'Axis Z', 'Temperature', 'Humidite')
    for i, col_name in enumerate(col_names, start=0):
        Label(frame_csv, text=col_name, bg='#ACA8A7').grid(row=3, column=i, padx=10)
    with open("data.csv", "r", newline="") as passfile:
        reader = csv.reader(passfile)
        data = list(reader)
        data = data[-10:]
    entrieslist = []
    for i, row in enumerate(data, start=4):
        entrieslist.append(row[0])
        for col in range(0, 5):
            Label(frame_csv, text=row[col], fg='black', bg='#ACA8A7').grid(row=i, column=col)


root = Tk()
root.geometry('1200x500')
root.title('Projet')
data = StringVar()
frame = Frame(root, borderwidth=1, relief="raised", highlightthickness=1)
frame.grid(row=2, column=2)
donnes = Label(frame, text=data.get(), font=('times', 12, 'bold'))
donnes.grid(row=1, column=0)
frame_csv = Frame(root, borderwidth=1, relief="ridge", width=400, height=400, bg='#ACA8A7')
frame_csv.grid(row=0, column=2, padx=5)
title_csv = Label(frame_csv, text="Les 10 derniers csv enregistres", bg='#000', fg='#ff0', padx=10, pady=5)
title_csv.grid(row=0, column=2, pady=10, sticky=NW)
frame_btn = Frame(root)
frame_btn.grid(row=2, column=0)
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().grid(row=0, column=0, padx=5, pady=10)
chart_type2 = FigureCanvasTkAgg(figure2, root)
chart_type2.get_tk_widget().grid(row=0, column=1, padx=5, pady=10)
message = Label(frame, text="Axis X| Axis Y| Axis Z| Temperature|Humidite: ", font=('times', 12, 'bold'))
message.grid(row=0, column=0)

btn1 = Button(frame_btn, text='Quit !',
              command=root.destroy, bg="red")
btn1.grid(row=1, column=5, padx=5)
btn2 = Button(frame_btn, text='Lancer  !', command=receiveData, bg="green")
btn2.grid(row=1, column=3, padx=5)
btnOpen_close = Button(frame_btn, text='Open port', command=Togglebtn_Open, bg="green")
btnOpen_close.grid(row=1, column=1, padx=5)
btnClose_open = Button(frame_btn, text='Close port', command=Togglebtn_Close, bg="orange")
btnClose_open.grid(row=1, column=2, padx=5)
btn_delete = Button(frame_btn, text='Supprimer ', command=delete_cvs, bg="red")
btn_delete.grid(row=1, column=4, padx=5)
display_csv()
root.mainloop()
