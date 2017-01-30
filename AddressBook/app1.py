from flask import Flask, render_template, request, json
app = Flask(__name__)
from flask.ext.mysql import MySQL

mysql = MySQL()

 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'secondguest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secondGuestPW'
app.config['MYSQL_DATABASE_DB'] = 'james_odonnell_addressbook'
app.config['MYSQL_DATABASE_HOST'] = 'mysql.james-odonnell.com'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/showAddContact')
def showAddContact():
   return render_template('addContact.html')


@app.route('/addContact',methods=['POST'])
def addContact():

    _name = request.form['inputName']
    _details = request.form['inputDetails']
    _org = request.form['inputOrganisation']

    if _name and _details and _org:

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""insert into Contacts(name, details, org) values(%s,%s,%s)""",(_name, _details, _org))
        connection.commit()
        connection.close ()

        return json.dumps({'html':'<span>All fields good !!</span>'})#These could be made more descriptive
    else:
        return json.dumps({'html':'<span>Bad</span>'})


@app.route('/addOrganisation',methods=['POST'])
def addOrganisation():

    _orgname = request.form['inputOrgName']
    _orgdetails = request.form['inputOrgDetails']

    if _orgname and _orgdetails:

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""insert into Organisations(name, details) values(%s,%s)""",(_orgname, _orgdetails))
        connection.commit()
        connection.close ()

        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Bad</span>'})  


@app.route('/editContact')
def edit():
    return render_template('editContact.html')


@app.route('/runEditContact',methods=['POST'])
def editContact():
    _name1 = request.form['inputname1'] 
    _details1 = request.form['inputdetails1']
    _org1 = request.form['inputorg1']
    _name2 = request.form['inputname2']
    _details2 = request.form['inputdetails2']
    _org2 = request.form['inputorg2']


    if _name1 and _details1 and _org1:

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""update Contacts set name=%s, details=%s, org=%s where name=%s and details=%s and org=%s""",(_name2, _details2, _org2, _name1, _details1, _org1))
        connection.commit()
        connection.close ()
        print_contacts()

        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Bad</span>'})  


@app.route('/editOrg')
def editorg():
    return render_template('editOrg.html')


@app.route('/runEditOrg',methods=['POST'])
def editOrganisation():
    _name1 = request.form['inputname1'] 
    _details1 = request.form['inputdetails1']
    _name2 = request.form['inputname2']
    _details2 = request.form['inputdetails2']

    if _name1 and _details1:

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""update Organisations set name=%s, details=%s where name=%s and details=%s""",(_name2, _details2, _name1, _details1))
        connection.commit()
        connection.close ()

        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Bad</span>'})   


@app.route('/delContact')
def delContact():
    _name1 = request.args.get('name')
    _details1 = request.args.get('details')
    _org1 = request.args.get('organisation')

    if _name1 and _details1 and _org1:

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""delete from Contacts where name=%s and details=%s and org=%s""",(_name1, _details1, _org1))
        connection.commit()
        connection.close ()
        #return render_template('index.html')

        #terrible, tried to return print_contacts() instead
        connection = mysql.connect()
        cursor = connection.cursor()
        temp = cursor.execute("""select name, details, org, id from Contacts""")
        contactsList = cursor.fetchall()
        connection.commit()
        contacts = [dict(name=row[0], details=row[1], org=row[2]) for row in contactsList]
        temp = cursor.execute("""select name, details from Organisations""")
        orgs = cursor.fetchall()
        connection.commit()
        organisations = [dict(name=row[0], details=row[1]) for row in orgs]
        connection.close ()
        return render_template('viewBook.html', contacts=contacts, organisations=organisations)
    else:
        return json.dumps({'html':'<span>Failed to delete</span>'})  


@app.route('/delOrg')
def delOrg():
    _name1 = request.args.get('name')
    _details1 = request.args.get('details')

    if _name1 and _details1:

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""delete from Organisations where name=%s and details=%s""",(_name1, _details1))
        connection.commit()
        connection.close ()
        #return render_template('index.html')

        #terrible, tried to return print_contacts() instead
        connection = mysql.connect()
        cursor = connection.cursor()
        temp = cursor.execute("""select name, details, org, id from Contacts""")
        contactsList = cursor.fetchall()
        connection.commit()
        contacts = [dict(name=row[0], details=row[1], org=row[2]) for row in contactsList]
        temp = cursor.execute("""select name, details from Organisations""")
        orgs = cursor.fetchall()
        connection.commit()
        organisations = [dict(name=row[0], details=row[1]) for row in orgs]
        connection.close ()
        return render_template('viewBook.html', contacts=contacts, organisations=organisations)
    else:
        return json.dumps({'html':'<span>Failed to delete</span>'})          


@app.route('/viewBook')
def print_contacts():
    connection = mysql.connect()
    cursor = connection.cursor()

    temp = cursor.execute("""select name, details, org, id from Contacts""")
    contactsList = cursor.fetchall()
    connection.commit()
    contacts = [dict(name=row[0], details=row[1], org=row[2]) for row in contactsList]


    temp = cursor.execute("""select name, details from Organisations""")
    orgs = cursor.fetchall()
    connection.commit()
    organisations = [dict(name=row[0], details=row[1]) for row in orgs]

    connection.close ()

    return render_template('viewBook.html', contacts=contacts, organisations=organisations)


if __name__ == "__main__":
    app.run()
