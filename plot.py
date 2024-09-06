import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from config import *
import discord

def userPlot(user, server_id, lift):
    ref = db.reference(f"/")
    fig, ax = plt.subplots()
    servRef = ref.child(server_id)
    userRef = servRef.child(user)
    benchRef = userRef.child(lift)
    temp = benchRef.get()
    time = []
    weight = []
    for i in temp:
        if i != "latest":
            dateStr = datetime.strptime(i, '%Y-%m-%d %H-%M-%S-%f')
            time.append(dateStr)
            weight.append(int(temp[i]))
    ax.plot(time, weight)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
    fig.autofmt_xdate()
    title = lift + " progression"
    plt.title(title)
    ax.set_xlabel('Time (yr-m-d hr)')
    ax.set_ylabel('Weight (lb)')
    for i, point in enumerate(weight):
        ax.annotate(point, (time[i], weight[i]))
    plt.scatter(time, weight)
    plt.savefig("plot")
    plt.clf()
    plt.close()
            
def userPlotAll(user, server_id): 
    ref = db.reference(f"/")
    fig, ax = plt.subplots()
    servRef = ref.child(server_id)
    userRef = servRef.child(user)
    for lift in ["bench", "squat", "deadlift"]:
        benchRef = userRef.child(lift)
        temp = benchRef.get()
        time = []
        weight = []
        for i in temp:
            if i != "latest":
                dateStr = datetime.strptime(i, '%Y-%m-%d %H-%M-%S-%f')
                time.append(dateStr)
                weight.append(int(temp[i]))
        ax.plot(time, weight, label = lift)
        for i, point in enumerate(weight):
            ax.annotate(point, (time[i], weight[i]))
        plt.scatter(time, weight)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
    fig.autofmt_xdate()
    title = "overall progression"
    plt.title(title)
    ax.set_xlabel('Time (yr-m-d hr)')
    ax.set_ylabel('Weight (lb)')
    plt.legend()
    plt.savefig("plot")
    plt.clf()
    plt.close()

def serverPlotAll(server_id):
    ref = db.reference(f"/")
    fig, ax = plt.subplots()
    servRef = ref.child(server_id)
    servGet = servRef.get()
    for user in servGet:
        userRef = servRef.child(user)
        for lift in ["bench", "squat", "deadlift"]:
            benchRef = userRef.child(lift)
            temp = benchRef.get()
            time = []
            weight = []
            for i in temp:
                if i != "latest":
                    dateStr = datetime.strptime(i, '%Y-%m-%d %H-%M-%S-%f')
                    time.append(dateStr)
                    weight.append(int(temp[i]))
            ax.plot(time, weight, label = lift)
            for i, point in enumerate(weight):
                ax.annotate(point, (time[i], weight[i]))
            plt.scatter(time, weight)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
    fig.autofmt_xdate()
    title = "overall progression"
    plt.title(title)
    ax.set_xlabel('Time (yr-m-d hr)')
    ax.set_ylabel('Weight (lb)')
    plt.legend()
    plt.savefig("plot")
    plt.clf()
    plt.close()