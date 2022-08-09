# import modules
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
#from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_bcrypt import Bcrypt
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

# launch Flask App
app = Flask(__name__)
# configure PostgreSQL db and secret key
WTF_CSRF_CHECK_DEFAULT = False
# On our PostgreSQL server, 'default_pw' will be the password we use to access the CLI after typing the command below:
# psql -h localhost -p 5436 -U postgres -d users
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:default_pw@users_db:5432/users'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SESSION_COOKIE_SECURE'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# create user class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.LargeBinary(), nullable=False, unique=False)

# create registration form class
class RegisterForm(FlaskForm):
    username = StringField(label=('Enter your username: '), validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(label=('Enter your password: '), validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

# this function checks if the username already exists in the database of registered users
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username is already taken, please choose another one.")

# create login form class
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


# create home endpoint
@app.route('/')
def home():
    return render_template('home.html')

# create login endpoint and validate user credentials, 
# redirecting to dashboard upon success
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# create dashboard route to confirm successful user login
@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# create route for new user registration
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    # this function will validate the creation of the new user
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# this endpoint will log the user out and redirect to the login page
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# initialize the app and PostgreSQL db
if __name__ == '__main__':
    db.create_all()
    print(db.engine.url)
    for table in db.metadata.tables.items():
        print(table)
    app.run(debug=True, port=4000, host='0.0.0.0')
