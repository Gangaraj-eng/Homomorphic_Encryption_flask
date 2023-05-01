from flask import Flask, jsonify,render_template
import requests
from ConnectToDB import get_user_collection
from flask import request,Response,redirect
from flask import session
from  Encryptions.Encryption import EncryptText
from  Encryptions.Encryption import EncryptNumber
from  Encryptions.Decryption import DecryptText
from  Encryptions.Decryption import DecryptNmber
import sys
import webbrowser
import os
from dotenv import load_dotenv
import json
import numpy as np
from flask import send_file

import jwt # for jwt authentication
app=Flask(__name__) # creating flask app

# get users collection 
user_collection=get_user_collection()
load_dotenv()

SECRET_KEY=os.environ.get('SECRET_KEY_JWT')
CLOUD_FUNCTION_URL_1=os.environ.get('CLOUD_FUNCTION_URL_1')
CLOUD_FUNCTION_URL_2=os.environ.get('CLOUD_FUNCTION_URL_2')

app.secret_key=SECRET_KEY

# home page
@app.route("/")
def home():
    if 'email' not in session:
        return redirect('/login')
    return render_template("index.html")


@app.route('/login',methods=['Get'])
def login_page():
    return render_template("Login.html")


@app.route('/signup',methods=['Get'])
def signup_page():
    return render_template("signup.html")


@app.route('/signup',methods=['Post'])
def signup():
    form_data=request.json
    firstName=form_data['firstName']
    lastName=form_data['lastName']
    email=form_data['email']
    password=form_data['Password']
    form_data['Password']=json.dumps(EncryptText(password))
    existing_users=user_collection.find_one({'email':email})

    if existing_users!=None:
        response={
            'message':'Email ID already exists'
        }
        return jsonify(response)
    
    # else create account
    new_user=user_collection.insert_one(form_data)
    session['email']=email
    response={
            'success':'true ',
            'message':'Account created succesfully'
        }
    return jsonify(response)


@app.route('/login',methods=['Post'])
def login():
    form_data=request.json
    email=form_data['email']
    password=form_data['Password']

    curr_user=user_collection.find_one({'email':email})

    if curr_user==None:
        response={
            'message':'Email doesn\'t exists'
        }
        return jsonify(response)
    
    curr_password=json.loads(curr_user['Password'])
    decrypted=DecryptText(curr_password)

    if decrypted!=password:
         response={
                    'message':'Wrong password'
                }
         return jsonify(response)

    # else return sucess
    session['email']=email
    response={
        'success':'true',
        'messsage':'Logged in successfully'
    }

    return jsonify(response)
    


@app.route('/perFormCalculations',methods=['Post'])
def calculate():
    marks=request.json['json_data_excel']
    print(marks)
#     temp_res={
#     "chemistry_total": 3524,
#     "maths_total": 3836,
#     "physics_total": 3670,
#     "student_wise_total": "[262, 191, 208, 165, 177, 192, 287, 171, 206, 210, 257, 235, 202, 241, 237, 259, 251, 245, 94, 243, 197, 233, 273, 280, 253, 239, 263, 256, 164, 166, 253, 210, 247, 212, 259, 226, 218, 212, 171, 186, 198, 256, 173, 164, 195, 240, 256, 245, 197, 255]"
# }
#     return jsonify(temp_res)
    
    # extract data 
    student_wise_marks=[]
    physics_marks=[]
    chemistry_marks=[]
    maths_marks=[]
    total_students=len(marks)
    marks.pop(0)
    for mr in marks:
        p=int(mr[1])
        c=int(mr[2])
        m=int(mr[3])
        # encrypting 
        p=EncryptNumber(p).tolist()
        c=EncryptNumber(c).tolist()
        m=EncryptNumber(m).tolist()

        physics_marks.append(p)
        chemistry_marks.append(c)
        maths_marks.append(m)
        student_wise_marks.append([p,c,m])
    

    # requesting the cloud function url
    response=requests.post(CLOUD_FUNCTION_URL_1,json={'num_array':physics_marks})
    data=response.json()
    physics_total=int(DecryptNmber(np.array(data)))
    response=requests.post(CLOUD_FUNCTION_URL_1,json={'num_array':maths_marks})
    data=response.json()
    maths_total=int(DecryptNmber(np.array(data)))
    response=requests.post(CLOUD_FUNCTION_URL_1,json={'num_array':chemistry_marks})
    data=response.json()
    chemistry_total=int(DecryptNmber(np.array(data)))

    response=requests.post(CLOUD_FUNCTION_URL_2,json={'num_array':student_wise_marks})

    data=response.json()
    
    student_wise_total=[]
    for x in data:
        student_wise_total.append(int(DecryptNmber(np.array(x))))

    response={
        'physics_total':physics_total,'chemistry_total':chemistry_total,'maths_total':maths_total
                    ,'student_wise_total':json.dumps(student_wise_total)
    }
    print(response)
    return jsonify(response)


@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/sample_ss')
def sampless():
    return send_file("sample_output.png")


@app.route("/sample_sheet_1")
def samplesheet1():
    filepath= "sample_sheet_1.xlsx"
    return send_file(filepath,as_attachment=True)

@app.route("/sample_sheet_2")
def samplesheet2():
    filepath= "sample_sheet_2.xlsx"
    return send_file(filepath,as_attachment=True)

# running the app in debug mode 
# so that app restarts on changes
app.run(debug=True) 