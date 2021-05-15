from flask import Flask
from flask import render_template, request
import json

app = Flask(__name__)

checkLogin = False
name= None

data = json.load(open('application\static\course.json'))



@app.route('/')
@app.route('/home')
def home():
    rc = json.load(open('application/static/userCourses.json'))
    registeredCourses = rc.get(name)
    print("registeredcourses home", registeredCourses)
    return render_template("home.html",check=checkLogin, name = name,courses = registeredCourses)


@app.route('/courses')
def contact():
    # print("courses are ", data, checkLogin)
    return render_template("courses.html", name = name, checkLogin= checkLogin, data = data)


@app.route('/login')
def login():
    users = json.load(open('application/static/users.json'))
    details = users.get(name)
    return render_template('login.html', checkLogin= checkLogin, name = name, details= details)


@app.route('/register')
def register():
    return render_template('register.html', checkLogin= checkLogin, name = name)

@app.route('/checkLogin', methods=["GET"])
def checklogin():
    global checkLogin, name
    name = request.args.get('username')
    pwd = request.args.get('password')
    checkLogin = True
    users = json.load(open('application/static/users.json'))
    for user in users:
        if user["name"] == name and user["password"] == pwd:
            return render_template("home.html", check=True, name=name)
    return render_template("login.html", tag="login Failed")
        



@app.route('/registerUser', methods=['POST'])
def registerUser():
    uname = request.form.get("name")
    password = request.form.get("password")
    phonenumber = request.form.get("phonenumber")
    users = json.load(open('application/static/users.json'))
    new_user = {}
    new_user["name"] = uname
    new_user["password"] = password
    new_user["phone"]= phonenumber
    users.append(new_user)
    print("after adding", users)

    json.dump(users, open('application/static/users.json', 'w') )

    return render_template("login.html")


@app.route('/registerCourse', methods=["post"])
def registerCourse():
    userCourses = json.load(open('application/static/userCourses.json'))
    user =  request.form.get("username")
    print("data is ", userCourses)
    course ={}
    course['name'] = request.form.get('course')
    course['price'] = request.form.get('price')
    course['description'] = request.form.get('description')
    course['id'] = request.form.get('id')

    if userCourses.get(user) == None:      
        userCourses[user] = [course]       
    else:
        rc = userCourses.get(user)
        rc.append(course)
        userCourses[user] = rc
    json.dump(userCourses, open('application/static/userCourses.json', 'w'))

    return render_template("courses.html", name = name, checkLogin= checkLogin, data = data, tag = "registered successfully course")


    





