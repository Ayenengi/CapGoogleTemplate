from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Sleep
from app.classes.forms import SleepForm
from flask_login import login_required
import datetime as dt
#import matplotlib.pyplot as plt
#import numpy as np

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/sleep/new', methods=['GET', 'POST'])
@login_required
def sleepNew():
    form = SleepForm()
    if form.validate_on_submit():
        # startDT = dt.datetime.combine(form.sleep_date.data, form.starttime.data)
        # endDT = dt.datetime.combine(form.sleep_date.data, form.endtime.data)
        # hours = startDT - endDT
        # flash(hours.min)
        newSleep = Sleep(
            sleeper = current_user,
            rating = form.rating.data,
            sleep_date = form.sleep_date.data,
            start = str(form.starttime.data),
            end = str(form.endtime.data),
            feel = form.feel.data,
            minstosleep = form.minstosleep.data,
        )
        newSleep.save()
        return redirect(url_for("sleep",sleepId=newSleep.id))
    
    if form.submit.data:
        if form.rating.data == 'None':
            form.rating.errors = ['Required']
        if form.feel.data == 'None':
            form.feel.errors = ['Required']
        
    return render_template("sleepform.html",form=form)

@app.route('/sleep/edit/<sleepId>', methods=['GET', 'POST'])
@login_required

def sleepEdit(sleepId):
    form = SleepForm()
    editSleep = Sleep.objects.get(id=sleepId)

    if editSleep.sleeper != current_user:
        flash("You can't edit a sleep you don't own.")
        return redirect(url_for('sleeps'))
    
    if form.validate_on_submit():
        editSleep.update(
            rating = form.rating.data,
            hours = form.hours.data,
            sleep_date = form.sleep_date.data
        )
        editSleep.save()
        return redirect(url_for("sleep",sleepId=editSleep.id))
    
    form.hours.data = editSleep.hours
    form.rating.process_data(editSleep.rating)
    form.sleep_date.data = editSleep.sleep_date
    return render_template("sleepform.html",form=form)

@app.route('/sleep/<sleepId>')
@login_required

def sleep(sleepId):
    thisSleep = Sleep.objects.get(id=sleepId)
    return render_template("sleep.html",sleep=thisSleep)

@app.route('/sleeps')
@login_required

def sleeps():
    sleeps = Sleep.objects()
    return render_template("sleeps.html",sleeps=sleeps)

@app.route('/sleep/delete/<sleepId>')
@login_required

def sleepDelete(sleepId):
    delSleep = Sleep.objects.get(id=sleepId)
    sleepDate = delSleep.sleep_date
    delSleep.delete()
    flash(f"sleep with date {sleepDate} has been deleted.")
    return redirect(url_for('sleeps'))

@app.route('/sleepgraph')
@login_required

def sleepgraph():
    sleeps = Sleep.objects()


    hours = []
    dates = []
    colors = []
    for sleep in sleeps:
        hours.append(sleep.hours)
        dates.append(sleep.sleep_date)   
        if sleep.rating >=4:
            colors.append('green')
        elif sleep.rating == 3:
            colors.append('yellow')
        else:
            colors.append('red')
    
    fig, ax = plt.subplots()

    ax.scatter(dates, hours, marker='o', c=colors)


    #ax.legend()
    plt.yticks(hours)
    plt.xticks(dates, rotation=45)
    #plt.gcf().set_size_inches(10, 5)
    fig.savefig("app/static/graphs/sleep.png", bbox_inches="tight")
    #fig.show()
    return render_template('sleepgraph.html',images=['sleep.png'])