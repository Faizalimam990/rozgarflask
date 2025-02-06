from flask import Flask, jsonify,request,render_template,url_for,flash,redirect
from sqlalchemy.orm import sessionmaker
from models import Users,Job,Hirer
from database import session as db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'R0ZGAR_BUZZ_F4RALL' 

@app.route('/')
def index():
    jobs=db_session.query(Job).all()
    return render_template('index.html',jobs=jobs)

@app.route('/account/')

def accountpage():
    return render_template('accountpage.html')

@app.route('/hirersignup/', methods=['GET', 'POST'])
def hirersignup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        
        # Check if the passwords match
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('hirersignup'))

        # Hash the password before saving
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new Hirer instance
        new_hirer = Hirer(
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
            email=email,
            password=hashed_password,
            location=f"{city}, {state}, {country}"
        )
        
        # Add to database and commit the transaction
        try:
            db_session.add(new_hirer)
            db_session.commit()
            flash("Signup successful! Please verify your email.", "success")
            return redirect(url_for('hirersignup'))  # Or redirect to login page
        except Exception as e:
            db_session.rollback()
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for('hirersignup'))

    return render_template('hirersignup.html')



@app.route('/add-job', methods=['POST'])
def addjob():
    # Get the data from the POST request
    data = request.get_json()

    # Extracting the fields from the received JSON data
           # 'get' method prevents KeyError if key is missing
    title = data.get('title')
    description = data.get('description')
    pincode = data.get('pincode')

    # Check if all necessary fields are provided
    if not all([title, description, pincode]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new Job object
    obj = Job( title=title, description=description, pincode=pincode)

    # Add the object to the database session and commit
    db_session.add(obj)
    db_session.commit()

    # Return a response
    return jsonify({"message": "Job added successfully"}), 201


@app.route('/show-jobs')
def showjobs():
    jobs=db_session.query(Job).all()
    
    job_list=[]
    for job in jobs:
        job_list.append(
            {
                'id':job.id,
                'title':job.title,
                'description':job.description,
                'pincode':job.pincode

        })
    response = json.dumps(job_list, indent=4)
    
    return app.response_class(response, content_type='application/json')






if __name__ == '__main__':
    app.run(debug=True)
