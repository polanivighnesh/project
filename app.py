from flask import Flask,render_template,redirect,url_for,request,flash,session
import mysql.connector
app=Flask(__name__)
app.config['SECRET_KEY']="my super secret key that no one is supported to know"
mydb=mysql.connector.connect(host='localhost',user='root',password='system',db='project')
with mysql.connector.connect(host='localhost',password='system',user='root',db='project'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(50) primary key,firstname varchar(20),lastname varchar(100),locality varchar(50),password varchar(20))")
    cursor.execute("create table if not exists login(username varchar(35),password varchar(20))")
   
@app.route('/login',methods=['post','get'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('view_posts'))
        else:
            return 'Invalid username and password' 
      
    return render_template('login.html')
@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method=='POST':
        username=request.form.get('username')
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        locality=request.form.get('locality')
        password=request.form.get('password')
        print(username)
        print(firstname)
        print(lastname)
        print(locality)
        print(password)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into registration values(%s,%s,%s,%s,%s)',[username,firstname,lastname,locality,password])
        mydb.commit()
        cursor.close()
    return render_template('registration.html')
@app.route('/forgot',methods=['GET','POST'])
def fp():
    if request.method=='post':
        newpassword=request.form.get('newpassword')
        confirmpassword=request.form.get('confirmpassword')
    return render_template('forgot.html')
@app.route('/')
def homepage():
     return render_template('homepage.html')
@app.route('/addpost',methods=['post','get'])
def addpost():
    if request.method=='POST':
        family=request.form['family']
        file=request.form['file']
        name=request.form['name']
        members=request.form['members']
        content=request.form['content']
        AC=request.form['AC']
        print(family)
        print(file)
        print(name)
        print(members)
        print(content)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts(family,file,name,members,content,AC) values(%s,%s,%s,%s,%s,%s)',[family,file,name,members,content,AC])
        mydb.commit()
        cursor.close()
    return render_template('addpost.html')
@app.route('/viewposts',methods=['post','get'])
def view_posts():
    cursor=mydb.cursor(buffered=True)
    cursor.execute("select*from posts")
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewposts.html',posts=posts)
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
app.run(debug=True,use_reloader=True)