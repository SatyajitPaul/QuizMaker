from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizemaker.sqlite"
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(10), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.question


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

db.create_all()

@app.route("/")
def home():
    return render_template('list-question.html')

@app.route("/add-question" , methods=['POST', 'GET'])
def addQuestion():
    if request.method == 'POST':
        question = request.form.get('question')
        opt1 = request.form.get('opt-0')
        opt2 = request.form.get('opt-1')
        opt3 = request.form.get('opt-2')
        opt4 = request.form.get('opt-3')
        answer = request.form.get('rightAnswer')
        catagory = request.form.get('category')
        optList = [opt1, opt2, opt3, opt4]
        optList = json.dumps(optList)
        # cat = Category(name = catagory)
        cat = Category.query.filter_by(name=catagory).first()
        q = Question(question = question, option = optList, answer = answer, category=cat)
        db.session.add(q)
        db.session.commit()
        return redirect("/all-question")
        
    else:
        cat = Category.query.all()
        return render_template('add-question.html', cat=cat)

@app.route("/catagory", methods=['POST', 'GET'])
def catagory():
    if request.method == 'POST':
        catagory = request.form.get('catagory')
        print(catagory)
        cat = Category(name=catagory)
        db.session.add(cat)
        db.session.commit()
        return redirect('/catagory')
    else:
        cat = Category.query.all()
        return render_template('add-catagory.html', cat=cat)

@app.route("/all-question")
def allQuestion():
    questions = Question.query.all()
    return render_template('list-question.html', questions = questions)
    
if __name__ == "__main__":
    app.run(debug=True)