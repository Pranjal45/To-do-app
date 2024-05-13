from flask import Flask, request,render_template, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app)

class Todo(db.Model):
   sno = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(200), nullable=False)
   desc = db.Column(db.String(500), nullable=False)
   date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

   def __repr__(self) -> str:
       return f"{self.sno} - {self.title}"
   

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        title= request.form.get('title')
        desc=request.form.get('desc')
        todo= Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title= request.form.get('title')
        desc=request.form.get('desc')
        todo= Todo(title=title, desc=desc)
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
 app.run(debug = True)