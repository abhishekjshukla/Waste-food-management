from flask import Flask,render_template,request,flash,session,g,redirect,url_for
import pymysql
from functools import wraps
from wtforms import Form,validators,PasswordField,StringField

app=Flask(__name__)
def login_required(f):
    @wraps(f)
    def login_fun(*args, **kwargs):
        if 'logged_in' in session:
        	return f(*args, **kwargs)
        else:
        	flash("You need to be logged in first")
        	return render_template('/login-page.html')
    return login_fun
class registration(Form):
	first_name = StringField(u'fname', validators=[validators.Length(min=4,max=14)])
	last_name  = StringField('lame', validators=[validators.optional()])
	city  = StringField(u'city', validators=[validators.DataRequired(message="Plese Enter City")])
	email=StringField('email',validators=[validators.Email()])
	password=PasswordField('password',validators=[validators.DataRequired(message="Plese Enter Password"),validators.EqualTo('confirm'),validators.Length(min=8,max=20)])
	confirm=PasswordField('cpassword',validators=[validators.DataRequired()])
@app.route('/logout/')
def logout():
	session.clear()
	flash("You have been logged out")
	return redirect(url_for('home'))
@app.route('/')
def home():
	return render_template('/landing-page.html')
class details():   # details of user money and credits
	def fun(credits=0,email=""):
		credit=credits
		email=email
		return [email,credit,name]
@app.route('/signup',methods=['GET','POST'])
def signup():
	form=registration(request.form)
	if(request.method=="POST" and form.validate()):
		con=pymysql.connect(host='localhost',user='root',password='asbasti007',db='foodapp')
		cursor=con.cursor()
		# fname=request.form['fname']
		# lname=request.form['lname']
		# city=request.form['city']
		# email=request.form['email']
		# password=request.form['password']
		# cpassword=request.form['cpassword']
		fname=form.first_name.data
		lname=form.last_name.data
		city=form.city.data
		email=form.email.data
		dupli=cursor.execute('SELECT * from user where email="%s"'%(email))
		dta=cursor.fetchall()
		print("duplicate is",dta)
		if(dupli>0):
			flash("Email Already present")
			return render_template('/signup-page.html',form=form)
		password=form.password.data
		cpassword=form.confirm.data
		a="""INSERT into user values(
		"%s","%s","%s","%s","%s","%s",0)
		"""%(fname,lname,city,email,password,cpassword)
		print("cmd = ",a)
		cursor.execute(a)
		con.commit()
		flash("Thanks for registering")
	return render_template('/signup-page.html',form=form)
@app.route('/login',methods=['POST','GET'])
def login():
	if(request.method=='POST'):
		email=request.form['email']
		password=request.form['password']
		con=pymysql.connect(host='localhost',user='root',password='asbasti007',db='foodapp')
		cursor=con.cursor()
		cursor.execute('SELECT * from user where email="%s"'%(email))
		dta=cursor.fetchall()
		print("dtaa is ",dta)
		if(dta==()):
			flash("Email Not found")
			return render_template('/login-page.html')
		if(dta[0][4]==password):
			session['logged_in']=True
			session['email']=email
			money=dta[0][6]*(.3) # credit X .3
			session['messages'] = email
			return redirect(url_for("profile"))
		else:
			flash("Invalid Password")
			return render_template('/login-page.html')
	return render_template('/login-page.html')
@app.route('/profile')
@login_required
def profile():
	con=pymysql.connect(host='localhost',user='root',password='asbasti007',db='foodapp')
	cursor=con.cursor()
	email=session['messages']
	cursor.execute('SELECT * from user where email="%s"'%(email))
	dta=cursor.fetchall()
	credit=dta[0][6]
	money=dta[0][6]*(.3)
	name=dta[0][0]
	return render_template('/dashboard.html',credit=credit,money=money,name=name)
@app.route('/donate',methods=['POST','GET'])
@login_required
def donate():
	if(request.method=="POST"):
		address=request.form['address']
		pin=request.form['pin']
		city=request.form['city']
		state=request.form['state']
		time=request.form['time']
		address=request.form['address']
		con=pymysql.connect(host='localhost',user='root',password='asbasti007',db='foodapp')
		with con.cursor() as cursor:
			name="abhishek"
			a="""INSERT into donate values(
			"%s","%s","%s","%s","%s","%s" )
			"""%(address,pin,state,city,time,name)
			print("cmd = ",a)
			cursor.execute(a)
			con.commit()

	return render_template('/donate-page.html')
@app.route('/user')
@login_required
def user():
	return render_template('/profile-page.html',)
if __name__ == '__main__':
	app.secret_key = 'my unobvious secret key'
	app.run(debug=True)