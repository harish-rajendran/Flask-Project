from flask import Flask, render_template,request,url_for
from flask_wtf import Form
from forms import RegistrationForm
from formss import ApplicationForm
from wtforms.fields import TextField ,TextAreaField, SubmitField, PasswordField 
from wtforms import validators , ValidationError
from wtforms.validators import Required
import datetime 
import MySQLdb
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = 'myverylongsecretkey'
db=MySQLdb.connect(user= 'user',
                   passwd= 'user',
                   db='sample',
                   host= 'localhost',
                   cursorclass=MySQLdb.cursors.DictCursor
				   )
@app.route('/')
def main():
    return render_template('index.html')
    
    
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate()== False:
            return ('ALL FIELDS ARE REQUIRED')
        else:
            name=form.name.data
            email= form.email.data
            password= form.password.data
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT email FROM example")
            result_set = cursor.fetchall()
            a=[]
            for row in result_set:
                a.append(row["email"])
            count=0
            for  x in a:
                if x==email:
                    count=count+1
            if count>1:
                return render_template('redirect.html')
            else:
                now = datetime.datetime.now()
                date=now.strftime('%Y-%m-%d %H:%M:%S')
                cursor = db.cursor() 
                cursor.execute("INSERT INTO example(Name,email,Password,Date)VALUES(%s,%s,%s,%s)",(name,email,password,date))
                db.commit()
                c= "hey , " + name + "..Have a good day!!!"
            return c
    else:
        return render_template('register.html', form=form)
        
@app.route('/signin',methods=['POST','GET'])
def signin():
    form=ApplicationForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            return ('ALL FIELDS ARE REQUIRED')
        else:
            email= form.email.data
            password= form.password.data
            now = datetime.datetime.now()
            date=now.strftime('%Y-%m-%d %H:%M:%S')
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT email FROM example")
            result_set = cursor.fetchall()
            d=[]
            for row in result_set:
                d.append(row["email"])
            count=0
            for  x in d:
                if x==email:
                    count=count+1
            if count<1:
                return 'You do not have an account.Please try signing in!!'
            else:
                cursor = db.cursor() 
                cursor.execute("INSERT INTO log(email,Password,Date)VALUES(%s,%s,%s)",(email,password,date))
                db.commit()
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT email FROM example")
                result_set = cursor.fetchall()
                a=[]
                for row in result_set:
                    a.append(row["email"])
                count=0
                for  x in a:
                    if x==email:
                        count=count+1
                cursor = db.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT email FROM log")
                result_set = cursor.fetchall()
                b=[]
                for row in result_set:
                    b.append(row["email"])
                count1=0
                for  x in b:
                    if x==email:
                        count1=count1+1
                flag=count+count1-1
                c= "hey , buddy" + "..You've logged in " + str(flag) +" time(s) before"
                return c 
    else:
        return render_template('signin.html', form=form)
            
        
if __name__ == "__main__":
    app.run(port=5002)