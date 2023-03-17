from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Sleep
from app.classes.forms import SleepForm
from flask_login import login_required
import datetime as dt

@app.route('/sleep/new', methods=['GET', 'POST'])
def sleepNew():
    form = SleepForm()
    if form.validate_on_submit():
        newSleep = Sleep(
            sleeper = current_user,
            rating = form.rating.data,
            hours = form.hours.data,
            sleep_date = form.sleep_date.data
        )
        newSleep.save()
        return redirect(url_for("sleep",sleepId=newSleep.id))
    return render_template("sleepform.html",form=form)

@app.route('/sleep/edit/<sleepId>', methods=['GET', 'POST'])
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
def sleep(sleepId):
    thisSleep = Sleep.objects.get(id=sleepId)
    return render_template("sleep.html",sleep=thisSleep)

@app.route('/sleeps')
def sleeps():
    sleeps = Sleep.objects()
    return render_template("sleeps.html",sleeps=sleeps)

@app.route('/sleep/delete/<sleepId>')
def sleepDelete(sleepId):
    delSleep = Sleep.objects.get(id=sleepId)
    sleepDate = delSleep.sleep_date
    delSleep.delete()
    flash(f"sleep with date {sleepDate} has been deleted.")
    return redirect(url_for('sleeps'))
