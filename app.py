from flask import Flask ,  render_template , request , redirect , url_for ,flash
from sqlalchemy.orm import sessionmaker
from database import session as db_session
from models import UsersLD
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config['SECRET_KEY'] = 'R0ZGAR_BUZZ_F4RALL' 


@app.route('/')
def signup():
     return render_template('signup.html')

@app.route('/save_users_login_data/' , methods = ["POST"])
def saving():
     if request.method == "POST":
          full_name = request.form.get("fname")
          last_name = request.form.get("lname")
          phone = request.form.get("phone")
          email = request.form.get("email")
          password = request.form.get("password")
          re_pass = request.form.get("re_pass")
          
          
          if password != re_pass:
            flash("Passwords do not match", "danger")
            return redirect(url_for('signup'))
       
          hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
          
          data = UsersLD(Firstname = full_name ,Lastname= last_name, Phone = phone,Email = email,Password =hashed_password)
          
          try:
               db_session.add(data)
               db_session.commit()
               flash("Signup successful! Please verify your email.", "success")
               return redirect(url_for('signup'))  
          except Exception as e:
               db_session.rollback()
               flash("An error occurred. Please try again.", "danger")
               return render_template('signup.html')

     return render_template('signup.html')
          




if __name__ == '__main__':
     app.run(debug=True)