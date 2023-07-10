# import neccessary librarys
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

# create a Flask app
app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# Create the SQLAlchemy instance
db = SQLAlchemy(app)

# create a model for the database
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  desc = db.Column(db.String(500), nullable=False)
  status = db.Column(db.Boolean, default=False)


# Create the database tables
app.app_context().push()
db.create_all()

# create routes for the app
@app.route('/')
def home():
  # Retrieve all todos with status=False from the database
  alltodo = Todo.query.filter_by(status=False).all()
  return render_template('index.html', alltodo=alltodo)


@app.route('/api/todo/add', methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
    # Retrieve the title and description from the form
    title = request.form['title']
    desc = request.form['desc']
    
    # Create a new Todo object with the retrieved data
    todo = Todo(title=title, desc=desc)
    
    # Add the new todo to the database
    db.session.add(todo)
    db.session.commit()
    
    # Redirect the user to the home page after adding the todo
    return redirect(url_for('home'))
  
  # Render the add.html template for GET requests
  return render_template('add.html')


@app.route('/api/todo/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  if request.method == 'POST':
    # Retrieve the updated title and description from the form
    title = request.form['title']
    desc = request.form['desc']
    
    # Retrieve the todo with the given id from the database
    todo = Todo.query.filter_by(id=id).first()
    
    # Update the title and description of the retrieved todo
    todo.title = title
    todo.desc = desc
    
    # Add the updated todo to the database
    db.session.add(todo)
    db.session.commit()

    if todo.status == True:
      # Redirect the user to the completed page if the todo is marked as completed
      return redirect(url_for('completed'))
    else:
      # Redirect the user to the home page after updating the todo
      return redirect(url_for('home'))
    
  # Retrieve the todo with the given id from the database for rendering the update page
  todo = Todo.query.filter_by(id=id).first()
  
  # Render the update.html template and pass the retrieved todo as a parameter
  return render_template('update.html', todo=todo)


@app.route('/api/todo/complete/<int:id>')
def complete(id):
  # Retrieve the todo with the given id from the database
  todo = Todo.query.filter_by(id=id).first()
  
  # Update the status of the retrieved todo to True (completed)
  todo.status = True
  
  # Add the updated todo to the database
  db.session.add(todo)
  db.session.commit()
  
  # Redirect the user to the home page after marking the todo as completed
  return redirect(url_for('home'))


@app.route('/api/todo/complete')
def completed():
  # Retrieve all todos with status=True (completed) from the database
  alltodo = Todo.query.filter_by(status=True).all()
  
  # Render the complete.html template and pass the retrieved todos as a parameter
  return render_template('complete.html', alltodo=alltodo)


@app.route('/api/todo/delete/<int:id>')
def delete(id):
  # Retrieve the todo with the given id from the database
  todo = Todo.query.filter_by(id=id).first()
  
  # Delete the retrieved todo from the database
  db.session.delete(todo)
  db.session.commit()
  
  if todo.status == True:
    # Redirect the user to the completed page if the deleted todo was marked as completed
    return redirect(url_for('completed'))
  else:
    # Redirect the user to the home page after deleting the todo
    return redirect(url_for('home'))


# Main driver function
if __name__ == '__main__':
  # Run the Flask application in debug mode off
  app.run(debug=False)


# End of code
