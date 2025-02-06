from flask import Flask, jsonify,request,render_template,url_for
from sqlalchemy.orm import sessionmaker
from models import Users,Job
from database import session
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    jobs=session.query(Job).all()
    return render_template('index.html',jobs=jobs)

@app.route('/account/')

def accountpage():
    return render_template('accountpage.html')

@app.route('/hirersignup/')

def hirersignup():
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
    session.add(obj)
    session.commit()

    # Return a response
    return jsonify({"message": "Job added successfully"}), 201


@app.route('/show-jobs')
def showjobs():
    jobs=session.query(Job).all()
    
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
