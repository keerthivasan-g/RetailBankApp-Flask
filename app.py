#Importing packages
from flask import Flask,render_template,request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
import os
import sqlite3


app = Flask(__name__)  #instance init
app.secret_key = '#12345678'


#DatabaseConfig
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'database.db')


db=SQLAlchemy(app)


#loginpage
@app.route('/', methods=['GET','POST'])
def Login_Page():
    if request.method=='POST':
        UserDetails=request.form
        username=UserDetails['username']
        password=UserDetails['password']
        session['username']=request.form['username']
        testuser=Auths.query.filter_by(username=username, password=password).first()
    return render_template('login.html')


#check_user
@app.route('/checkuser', methods=['GET','POST'])
def check_user():
    if request.method=='POST':
        UserDetails=request.form
        username=UserDetails['username']
        password=UserDetails['password']
        testuser=Auths.query.filter_by(username=username, password=password).first()
        if testuser:
            designation = int(testuser.usertype)
            loginat=datetime.now().strftime("%Y-%b-%d %I-%M%p") #June 17, 2020 03:55PM (%B %d, %Y %I:%M%p)
            login_user = Log(username=username,
                             password=password,
                             loginat=loginat)
            db.session.add(login_user)
            db.session.commit()
            if designation==0:
                return redirect(url_for('createCustomer'))
            else:
                return redirect(url_for('detailsSearchAccount'))


#createCustomer
ccustid=100000000
@app.route('/create-customer',methods=['GET','POST'])
def createCustomer():
    msg=''
    if request.method=='POST':
        #CustDetails=request.form
        ws_ssn=request.form['ws_ssn']
        ws_name=request.form['ws_name']
        ws_age=request.form['ws_age']
        ws_adrs=request.form['ws_adrs_1']
        testssn=CustDetails.query.filter_by(ws_ssn=ws_ssn).first()
        if testssn:
            msg='exists'
            return render_template('create-customer.html',msg=msg),409
        else:
            global ccustid
            ccustid = ccustid+1
            ws_cust_id=ccustid
            create_cus = CustDetails(ws_ssn=ws_ssn,
                                     ws_name=ws_name,
                                     ws_age=ws_age,
                                     ws_adrs=ws_adrs,
                                     ws_cust_id=ws_cust_id)
            db.session.add(create_cus)
            db.session.commit()
            msg='success'
            return render_template('create-customer.html',msg=msg),201
    return render_template('create-customer.html')


#updatesearchCustomer
@app.route('/update-search-customer',methods=['GET','POST'])
def uSearchCustomer():
    msg=''
    if request.method=='POST':
        updateCustomer=request.form
        ws_ssn=updateCustomer['ws_ssn']
        ws_cust_id=updateCustomer['ws_cust_id']
        testexists=CustDetails.query.filter_by(ws_ssn=ws_ssn, ws_cust_id=ws_cust_id).first()
        if testexists:
            ws_ssn = testexists.ws_ssn
            ws_cust_id = testexists.ws_cust_id
            ws_name = testexists.ws_name
            ws_adrs = testexists.ws_adrs
            ws_age = testexists.ws_age
            return render_template('update-customer.html',ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,ws_name=ws_name,ws_adrs=ws_adrs,ws_age=ws_age)
        else:
            return render_template('transfer-search-account.html',msg=msg)
    return render_template('transfer-search-account.html'),202


#deletesearchCustomer
@app.route('/delete-search-customer', methods=['GET','POST'])
def dSearchCustomer():
    msg=''
    if request.method=='POST':
        ws_ssn=request.form['ws_ssn']
        ws_cust_id=request.form['ws_cust_id']
        if (type(ws_ssn)==str):
            testexists=CustDetails.query.filter_by(ws_ssn=ws_ssn).first()
            ws_ssn=testexists.ws_ssn
            ws_cust_id=testexists.ws_cust_id
            ws_name=testexists.ws_name
            ws_adrs = testexists.ws_adrs
            ws_age = testexists.ws_age
            return render_template('delete-customer.html',ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,ws_name=ws_name,ws_adrs=ws_adrs,ws_age=ws_age)
        elif (type(ws_cust_id)==str) :
            testexists=CustDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_ssn=testexists.ws_ssn
            ws_cust_id=testexists.ws_cust_id
            ws_name=testexists.ws_name
            ws_adrs = testexists.ws_adrs
            ws_age = testexists.ws_age
            return render_template('delete-customer.html',ws_ssn=ws_ssn,ws_cust_id=ws_cust_id,ws_name=ws_name,ws_adrs=ws_adrs,ws_age=ws_age)
        else:
            msg='error'
            return render_template('delete-search-customer.html',msg=msg)
    return render_template('delete-search-customer.html')


#updateCustomer
@app.route('/update-customer', methods=['GET','POST'])
def updateCustomer():
    if request.method=='POST' and 'new_ws_name' in request.form():
        new_ws_name=request.form['new_ws_name']
        new_ws_adrs=request.form['new_ws_adrs']
        new_ws_age=request.form['new_ws_age']
        update_cus=CustDetails(ws_name=new_ws_name,
                               ws_adrs=new_ws_adrs,
                               ws_age=new_ws_age)
        db.session.add(update_cus)
        db.session.commit()
        msg='success'
        return render_template('update-customer.html',msg=msg),200
    return render_template('update-customer.html')


#deleteCustomer
@app.route('/delete-customer',methods=['GET','POST'])
def deleteCustomer():
    if request.method=='POST':
        ws_ssn=request.form['ws_ssn']
        delcus=CustDetails.query.filter_by(ws_ssn=ws_ssn).first()
        if delcus:
            db.session.delete(delcus)
            db.session.commit()
            msg='success'
            return render_template('delete-customer.html',msg=msg),200
    return render_template('delete-customer.html')


#create-acccount
@app.route('/create-account',methods=['GET','POST'])
def createAccount():
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_type=request.form['ws_acct_type']
        ws_amt=request.form['ws_amt']
        checacc=CustDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
        checacc2=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
        if checacc2:
            msg='exists'
            return render_template('create-account.html',msg=msg)
        if checacc:
            ws_acct_id=123456789
            ws_acc_crdate=datetime.now().strftime("%Y-%b-%d %I-%M%p")
            ws_acct_balance=ws_amt
            creacc=AcctDetails(ws_cust_id=ws_cust_id,
                                ws_acct_type=ws_acct_type,
                                ws_acct_balance=ws_acct_balance,
                                ws_acct_id=ws_acct_id,
                                ws_acc_crdate=ws_acc_crdate)
            db.session.add(creacc)
            db.session.commit()
            msg='success'
            return render_template('create-account.html',msg=msg)
        else:
            msg='no cust exist'
            return render_template('create-account.html',msg=msg)
    return render_template('create-account.html'),200


#searchaccount
@app.route('/search-account',methods=['GET','POST'])
def searchAccount():
    msg=''
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_id=request.form['ws_acct_id']
        if  ws_acct_id:
            testacct=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            return render_template('delete-account.html',ws_acct_id=ws_acct_id,ws_acct_type=ws_acct_type)
        if  ws_cust_id:
            testacct=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            return render_template('delete-account.html',ws_acct_id=ws_acct_id,ws_acct_type=ws_acct_type)
        else:
            msg='error'
            return render_template('search-account.html',msg=msg)
    return render_template('search-account.html')


#deleteaccount
@app.route('/delete-account',methods=['GET','POST'])
def deleteAccount():
    if request.method=='POST':
        ws_acct_id=request.form['ws_acct_id']
        delact=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
        if delact:
            db.session.delete(delact)
            db.session.commit()
            msg='success'
            return render_template('delete-customer.html',msg=msg)
    return render_template('delete-customer.html')


#detailsSearchAccount
@app.route('/details-search-account',methods=['GET','POST'])
def detailsSearchAccount():
    msg=''
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_id=request.form['ws_acct_id']
        #ws_acct_type=request.form['ws_acct_type']
        if  ws_acct_id:
            testacct=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('details-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        elif  ws_cust_id:
            testacct=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('details-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        else:
            msg='error'
            return render_template('details-search-account.html',msg=msg)
    return render_template('details-search-account.html')


#withdrawSearchAccount
@app.route('/withdraw-search-account',methods=['GET','POST'])
def withdrawSearchAccount():
    msg=''
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_id=request.form['ws_acct_id']
        #ws_acct_type=request.form['ws_acct_type']
        if  ws_acct_id:
            testacct=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('withdraw-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        if  ws_cust_id:
            testacct=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('withdraw-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        else:
            msg='error'
            return render_template('withdraw-search-account.html',msg=msg)
    return render_template('withdraw-search-account.html')


#depositSearchAccount
@app.route('/deposit-search-account',methods=['GET','POST'])
def depositSearchAccount():
    msg=''
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_id=request.form['ws_acct_id']
        #ws_acct_type=request.form['ws_acct_type']
        if  ws_acct_id:
            testacct=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('deposit-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        elif  ws_cust_id:
            testacct=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('deposit-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        else:
            msg='error'
            return render_template('deposit-search-account.html',msg=msg)
    return render_template('deposit-search-account.html')


#transferSearchAccount
@app.route('/transfer-search-account',methods=['GET','POST'])
def transferSearchAccount():
    msg=''
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_id=request.form['ws_acct_id']
        #ws_acct_type=request.form['ws_acct_type']
        if  ws_acct_id:
            testacct=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('transfer-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        if  ws_cust_id:
            testacct=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            return render_template('transfer-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance)
        else:
            msg='error'
            return render_template('transfer-search-account.html',msg=msg)
    return render_template('transfer-search-account.html')


#statementSearchAccount
@app.route('/statement-search-account',methods=['GET','POST'])
def statementSearchAccount():
    msg=''
    if request.method=='POST':
        ws_cust_id=request.form['ws_cust_id']
        ws_acct_id=request.form['ws_acct_id']
        #ws_acct_type=request.form['ws_acct_type']
        if  ws_acct_id:
            testacct=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            con = sqlite3.connect('database.db')
            con.row_factory = sqlite3.Row
            cur=con.cursor()
            cur.execute('SELECT * from trxnlogdetails')
            rows=cur.fetchall();
            cur.close
            return render_template('statement-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance,rows=rows)
        if  ws_cust_id:
            testacct=AcctDetails.query.filter_by(ws_cust_id=ws_cust_id).first()
            ws_acct_id=testacct.ws_acct_id
            ws_acct_type=testacct.ws_acct_type
            ws_cust_id=testacct.ws_cust_id
            ws_acct_balance=testacct.ws_acct_balance
            con = sqlite3.connect('database.db')
            cur=con.cursor()
            cur.execute('SELECT * from trxnlogdetails')
            rows=cur.fetchall();
            cur.close
            return render_template('statement-account.html',ws_acct_id=ws_acct_id,ws_cust_id=ws_cust_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance,rows=rows)
        else:
            return render_template('statement-search-account.html',msg=msg)
    return render_template('statement-search-account.html')


#withdrawAccount
@app.route('/withdraw-account',methods=['GET','POST'])
def withdrawAccount():
    if request.method=='POST':
        ws_desc='withdraw'
        ws_time=datetime.now().strftime("%Y-%b-%d %I-%M%p")
        ws_acct_id=request.form['ws_acct_id']
        ws_amt=request.form['ws_amt']
        #ws_acct_type=request.form['ws_acct_type']
        getdetails=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
        ws_acct_balance= int(getdetails.ws_acct_balance) - int(ws_amt)
        updateaccount=AcctDetails(ws_acct_balance=ws_acct_balance)
        getdetails.ws_acct_balance=ws_acct_balance
        ws_cust_id=getdetails.ws_cust_id
        ws_trxn_id=100000202
        savelog=TrxnLogDetails(ws_acct_id=ws_acct_id,
                               ws_amt=ws_amt,
                               ws_desc=ws_desc,
                               ws_time=ws_time,
                               ws_cust_id=ws_cust_id,
                               ws_trxn_id=ws_trxn_id)
        db.session.add(savelog)
        db.session.commit()
        msg='success'
        return render_template('withdraw-account.html',ws_cust_id=ws_cust_id,ws_acct_id=ws_acct_id,ws_acct_balance=ws_acct_balance,msg=msg)
    return render_template('withdraw-account.html')


#depositAccount
@app.route('/deposit-account',methods=['GET','POST'])
def depositAccount():
    if request.method=='POST':
        ws_desc='deposit'
        ws_time=datetime.now().strftime("%Y-%b-%d %I-%M%p")
        ws_trxn_id=100000202
        ws_acct_id=request.form['ws_acct_id']
        ws_amt=request.form['ws_amt']
        getdetails=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
        ws_acct_balance= int(getdetails.ws_acct_balance) + int(ws_amt)
        updateaccount=AcctDetails(ws_acct_balance=ws_acct_balance)
        getdetails.ws_acct_balance=ws_acct_balance
        ws_cust_id=getdetails.ws_cust_id
        savelog=TrxnLogDetails(ws_acct_id=ws_acct_id,
                               ws_amt=ws_amt,
                               ws_desc=ws_desc,
                               ws_time=ws_time,
                               ws_cust_id=ws_cust_id,
                               ws_trxn_id=ws_trxn_id)
        db.session.add(savelog)
        db.session.commit()
        msg='success'
        return render_template('deposit-account.html',ws_cust_id=ws_cust_id,ws_acct_id=ws_acct_id,ws_acct_balance=ws_acct_balance,msg=msg)
    return render_template('deposit-account.html')


#transferAccount
@app.route('/transfer-account',methods=['GET','POST'])
def transferAccount():
    if request.method=='POST':
        ws_src_id=request.form['ws_src_id']
        ws_acct_id=request.form['ws_tgt_id']
        ws_amt=request.form['ws_amt']
        checkexist=AcctDetails.query.filter_by(ws_acct_id=ws_acct_id).first()
        sourceexist=AcctDetails.query.filter_by(ws_acct_id=ws_src_id).first()
        if checkexist:
            ws_trxn_id=100000202
            ws_desc='transfer'
            ws_time=datetime.now().strftime("%Y-%b-%d %I-%M%p")
            newbal = int(checkexist.ws_acct_balance) + int(ws_amt)
            checkexist.ws_acct_balance=newbal
            newbal = int(sourceexist.ws_acct_balance) - int(ws_amt)
            sourceexist.ws_acct_balance=newbal
            ws_cust_id=sourceexist.ws_cust_id
            ws_acct_balance=newbal
            savelog=TrxnLogDetails(ws_trxn_id=ws_trxn_id,
                                   ws_acct_id=ws_acct_id,
                                   ws_amt=ws_amt,
                                   ws_desc=ws_desc,
                                   ws_time=ws_time,
                                   ws_cust_id=ws_cust_id)
            db.session.add(savelog)
            db.session.commit()
            msg='success'
            return render_template('transfer-account.html',ws_cust_id=ws_cust_id,ws_acct_id=ws_acct_id,ws_acct_balance=ws_acct_balance,msg=msg)
        else:
            msg='notexist'
            return render_template('transfer-account.html',msg=msg)
    return render_template('transfer-account.html')


#customerStatus
@app.route('/customer-status',methods=['GET','POST'])
def customerStatus():
    #cur = con.cursor() ws_cust_id,ws_ssn,ws_acct_status,ws_msg,ws_last_update
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur=con.cursor()
    cur.execute('SELECT * from custdetails')
    rows=cur.fetchall()
    cur.close
    return render_template('customer-status.html', rows=rows)


#accountStatus
@app.route('/account-status',methods=['GET','POST'])
def AccountStatus():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur=con.cursor()
    cur.execute('SELECT * from acctdetails')
    rows=cur.fetchall()
    cur.close
    return render_template('account-status.html', rows=rows)


#database models
class Auths(db.Model):
    __tablename__='auths'
    username=Column(String, primary_key=True, unique=True)
    password=Column(String)
    usertype=Column(Integer)


class Log(db.Model):
    __tablename__='log'
    username=Column(String, primary_key=True, unique=True)
    password=Column(String)
    loginat=Column(String)


class CustDetails(db.Model):
    __tablename__='custdetails'
    ws_ssn=Column(String, primary_key=True)
    ws_name=Column(String)
    ws_age=Column(String)
    ws_adrs=Column(String)
    ws_cust_id=Column(Integer)


class AcctDetails(db.Model):
    __tablename__='acctdetails'
    ws_cust_id=Column(Integer, primary_key=True)
    ws_acct_id=Column(Integer)
    ws_acct_type=Column(String)
    ws_acct_balance=Column(Integer)
    ws_acc_crdate=Column(String)
    ws_acct_lasttrdate=Column(String)
    ws_msg=Column(String)
    ws_acct_status=Column(String)
    ws_last_updated=Column(String)
    ws_ssn=Column(String)


class TrxnDetails(db.Model):
    __tablename__='trxndetails'
    ws_cust_id=Column(Integer, primary_key=True)
    ws_accnt_type=Column(String)
    ws_amt=Column(Integer)
    ws_trxn_date=Column(String)
    ws_src_typ=Column(String)
    ws_tgt_typ=Column(String)
    wc_src_id=Column(Integer)
    ws_tgt_id=Column(Integer)


class TrxnLogDetails(db.Model):
    __tablename__='trxnlogdetails'
    ws_trxn_id=Column(Integer, primary_key=True)
    ws_acct_id=Column(Integer)
    ws_amt=Column(Integer)
    ws_desc=Column(String)
    ws_time=Column(String)
    ws_cust_id=Column(Integer)


@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('logout.html')


app.run(debug=True)
