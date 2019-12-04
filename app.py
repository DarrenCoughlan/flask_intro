from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# __name__ referencing this file
app = Flask(__name__)
# telling sql_alchemy where our DB is (3 forward slashes is relative path,
# 4 is absolute path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# class for to-do db setup extending db.Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# index route so when we browse to url we dont immediately just 404
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # Task content is the value which is entered in the textbox
        # and taken in through the form in index.html input
        task_content = request.form['content']

        # Create a new content db model
        new_task = Todo(content=task_content)

        # Push to database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        # All current tasks in the table queried from database
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# New route for deleting a task from the list
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

# New route for updating a task in the list
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # set the task content as the 'content' in the forms input box in update
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating the task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
