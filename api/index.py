from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session security
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///chatbot.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    email = db.Column(db.String(20), nullable = False, unique= True)
    password = db.Column(db.String(20), nullable = False)
    def __repr__(self) -> str:
        return f"{self.id}-{self.email}-{self.password}"  
# Function to create tables within the application context
def create_tables():
    with app.app_context():
        # db.drop_all()             
        db.create_all()
# Call the function to create tables
create_tables()
@app.route('/')
def chat_bot():
    # Check if user is authenticated by checking for email cookie
    email = request.cookies.get('email')
    if email:
        # User is authenticated, you can retrieve user information using email
        user = User.query.get(email)
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
@app.route('/product')
def products():
    return 'This is product page'
@app.get('/login')
def login_page():
    return render_template('login.html')
@app.get('/register')
def register_page():
    return render_template('register.html')
@app.post('/register')
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    # password = request.form.get('password')
    new_user = User(email = email, password = password)
    if new_user:
        error = 'Email already exist. Please use different Email.'
        return render_template('register.html', error=error)
    else:
          # Add the object to the session
        db.session.add(new_user) 
            # Commit the session to persist the changes
        db.session.commit()
        return redirect(url_for('login_page'))
@app.post('/login')
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Query the database for the user with the provided username
        user = User.query.filter_by(email=email).first()
        # Check if the user exists and the password matches
        if user and user.password == password:
            response = make_response(redirect(url_for('chat_bot')))
            response.set_cookie('email', user.email)
            return response
        else:
            # Authentication failed, show an error message
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
                  
if __name__ == "__main__":

    app.run(debug=True)