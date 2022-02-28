from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
file_dir = os.path.dirname(os.path.abspath(__file__))
goal_route = os.path.join(file_dir, "app.db")
app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///" + goal_route

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime)

db.create_all()


@app.route("/")
def index():
    now = datetime.datetime.now()
    titles = []
    dates = []
    task_id = 1
    tasks = Task.query.filter(Task.id == task_id).first()
    while tasks:
        titles.append(tasks.title)
        dates.append(tasks.date)
        task_id += 1
        tasks = Task.query.filter(Task.id == task_id).first()
    ids = len(titles)
    return render_template("index.html", now=now.strftime("%x"), titles=titles, dates=dates, ids=int(ids))

@app.route("/add", methods=['POST'])
def add():
    title = request.form.get("title")
    date = datetime.datetime.now()
    new_task = Task(title=title, date=date)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route("/reset")
def reset():
    db.drop_all()
    db.create_all()
    return redirect("/")