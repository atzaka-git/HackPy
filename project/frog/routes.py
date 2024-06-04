from frog import app, db
from flask import render_template, request, url_for, redirect, session, flash
from sqlalchemy import text

@app.route('/')
def home_page():
    cookie = session.get('tadpole')
    print("<>home_page()")
    return render_template('home.html')

# -------- LOGIN -----------
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    print("login was called")

    if request.method == 'POST':
        print("->login_page()")
        username = request.form.get('Username')
        password = request.form.get('Password')
        print("Here the Data!!!")
        print(username)
        print(password)

        if (username is None or isinstance(username, str) is False or len(username) < 3):
            print("not valid")
            #flash(f"Username is not valid", category='warning')
            return render_template('login.html', cookie=None)

        if (password is None or
                isinstance(password, str) is False or
                len(password) < 3):
            print("something with password")
            #flash(f"Password is not valid", category='warning')
            return render_template('login.html', cookie=None)

        query_stmt = f"select username from users where username = '{username}' and password = '{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))

        user = result.fetchall()
        #print("debug1")
        if not user:
            flash(f"Try again", category='warning')
            #print("debug2")
            return redirect(url_for("login_page"))
        #print("debug3")
        #flash(f"'{user}', you are logged in ", category='success')
        print("debug1")

        #resp = redirect('/facts')
        print("debug2")
        #resp.set_cookie('tadpole', username)
        session["tadpole"] = username
        print("<-login(), go to facts_page")
        
        return redirect(url_for("facts_page"))
        #return resp

    return render_template('login.html', cookie=None)

# -------- REGISTER -----------
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        print("->register_page()")

        username = request.form.get('Username')
        email = request.form.get('Email')
        password = request.form.get('Password')
        confirmPassword = request.form.get('ConfirmPassword')

        print(username)
        print(email)
        print(password)
        print(confirmPassword)

        if(username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            #flash("Username not valid", category='danger')
            print("<-register_page(), username invalid")
            return render_template('register.html', cookie=None)

        if(email is None or
                isinstance(email, str) is False or
                len(email) < 3):
            print("<-register_page(), email not valid")
            #flash("Email not valid", category='danger')
            return render_template('register.html', cookie=None)

        if(password is None or isinstance(password, str) is False or len(password) < 3 or password != confirmPassword):
            print("<-register_page(), password not valid")
            #flash("Password not valid", category='danger')
            return render_template('register.html', cookie=None)

        query_stmt = f"select * from users where username = '{username}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        item = result.fetchone()
        print(item)

        if item is not None:
            #flash("Username exists, try again")
            print("Username exists")
            return render_template('register.html', cookie=None)

        query_insert = f"insert into users (username, email_address, password) values ('{username}', '{email}', '{password}');"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        #flash("You are registered", category='success')
        #resp = redirect('/facts')
        #resp.set_cookie('name', username)
        print("<-register_page(), go to facts_page")
        #return resp
        session["tadpole"] = username
        return redirect(facts_page)

    return render_template('register.html')

# -------- FACTS -----------
@app.route('/facts', methods=['GET', 'POST'])
def facts_page():
    #cookie = request.cookies.get('tadpole')
    cookie = session.get("tadpole")
    print("->facts_page()", cookie)

    #if not request.cookies.get('tadpole'):
    if not session.get("tadpole"):
        print("<-facts_page(), no cookie")
        return redirect(url_for('login_page'))

    query_stmt = f"select * from frogfacts;"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()

    print(itemsquery)
    print("<-facts_page()=", cookie)
    return render_template('facts.html', items=itemsquery, cookie=cookie)


# -------- ALL -----------
@app.route('/fact_entry', methods=['GET', 'POST'])
def fact_entry():

    #cookie = request.cookies.get('tadpole')
    cookie = session.get("tadpole")
    print("->fact_entry()", cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login'))

    if request.method == 'POST':
        coolness = request.form.get('Coolness')
        username = request.form.get('Username')
        title = request.form.get('Title')
        description = request.form.get('Description')

        query_insert = f"insert into frogfacts (coolness, username, title, description) values ({coolness}, '{username}', '{title}', '{description}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        print("hey erfolgreich")
        #resp = redirect('/facts')
        #resp.set_cookie('tadpole', cookie)
        #return resp
        session["tadpole"] = username
        return redirect("/facts")

    return render_template('fact_entry.html', cookie=cookie)

@app.route('/fact_item/<item_id>', methods=['GET'])
def fact_item(item_id):
    print("->fact_item()")
    query_stmt = f"select * from frogfacts where id={item_id}"
    # UNION SELECT * FROM frogfacts;

    result = db.session.execute(text(query_stmt))
    item = result.fetchone()
    print(query_stmt)
    if not item:
        print("item not existing")
        # error handling ....

    #cookie = request.cookies.get('tadpole')
    cookie = session.get("tadpole")

    return render_template('fact_item.html', items=item, cookie=cookie)

@app.route('/logout')
def logout_page():
    resp = redirect ('/')
    #resp.set_cookie('tadpole', '', expires=0)
    #resp.set_cookie('name', None)
    session["tadpole"] = None
    #return resp
    return redirect("/#")


