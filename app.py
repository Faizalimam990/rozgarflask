from flask import Flask, jsonify,request,render_template,url_for,flash,redirect,session
from sqlalchemy.orm import sessionmaker
from models import Users,Job,Hirer
from database import session as db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import json
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'R0ZGAR_BUZZ_F4RALL' 
@app.route('/')
def index():
    # Get username and role from the session
    username = session.get('firstname', 'Guest')  # Default to 'Guest' if not in session
    role = session.get('role', 'guest')           # Default to 'guest' if not in session
    
    # Query the database for jobs
    jobs = db_session.query(Job).all()
    
    # Pass data to the template
    return render_template('index.html', jobs=jobs, username=username, role=role)
@app.route('/account/')

def accountpage():
    return render_template('accountpage.html')
@app.route('/hirersignup/', methods=['GET', 'POST'])
def hirersignup():
    if request.method == 'POST':
        # Form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        country = request.form.get('country')
        state = request.form.get('state')
        city = request.form.get('city')
        
        # Password validation
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('hirersignup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method= 'pbkdf2:sha256')

        # Create Hirer instance
        new_hirer = Hirer(
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
            email=email,
            password=hashed_password,
            city=city,
            state=state,
            country=country,
            verified="NO"  # Default verified status
        )

        # Commit to the database
        try:
            db_session.add(new_hirer)  # Add the new hirer to the session
            db_session.commit()  # Commit the transaction
            session['user_id'] = new_hirer.id  # Store the hirer's ID
            session['firstname'] = new_hirer.firstname  # Store the hirer's username (could also use email)
            session['role'] = 'Hirer'  # Set    the role as 'hirer'
            print(f"Session set: {session['firstname']}, {session['role']}")
            
            flash("Signup successful! Please verify your email.", "success")
            return redirect(url_for('index'))  # Or redirect to the login page
        except Exception as e:
            db_session.rollback()  # Rollback in case of error
            flash("An error occurred. Please try again.", "danger")
            print(f"Error: {e}")  # Log the error for debugging
            return redirect(url_for('hirersignup'))  # Optionally redirect back

    return render_template('hirersignup.html')


@app.route('/post-job/', methods=['GET', 'POST'])
def postjob():
    if request.method == 'POST':
        # Get the form data
        title = request.form.get('title')
        description = request.form.get('description')
        pincode = request.form.get('pincode')
        location_link = request.form.get('location_link')
        
        # Get the hirer (employer) information from the session
        hirer_id = session.get('user_id')  # Get the current user's ID from session

        if not hirer_id:
            flash("You need to be logged in to post a job.", "danger")
            return redirect(url_for('index'))  # Redirect to the index or login page

        # Create the new job object
        new_job = Job(
            title=title,
            description=description,
            pincode=pincode,
            location_link=location_link,
            hirer_id=hirer_id  # Associate job with the current hirer (user)
        )

        # Commit the new job to the database
        try:
            db_session.add(new_job)
            db_session.commit()
            flash("Job posted successfully!", "success")
            return redirect(url_for('index'))  # Redirect to the home page or job listing
        except Exception as e:
            db_session.rollback()
            flash("An error occurred. Please try again.", "danger")
            print(f"Error: {e}")
            return redirect(url_for('postjob'))  # Optionally redirect back

    return render_template('postjob.html')

@app.route('/api/v2/add-job/', methods=['POST'])
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
