"""Login page."""
# import uuid
import os
import hashlib
import uuid
import pathlib
import flask
import insta485


@insta485.app.route('/accounts/', methods=['POST'])
def handle_login():
    """Handle the login form."""
    target = flask.request.args.get('target')

    # print("DEBUG Login:", flask.request.form['username'])
    operation = flask.request.form['operation']
    # Grabbing username and password values from form
    if operation == 'login':
        user_text = flask.request.form['username']
        password = flask.request.form['password']
        if (user_text is None or password is None):
            print("abort")
            flask.abort(400)

        # Password salting and hashing
        algorithm = 'sha512'
        salt = 'a45ffdcc71884853a2cba9e6bc55e812'
        # uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        # Connect and query database
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ?",
            (user_text, )
        )

        # Check if correct password
        pwd = cur.fetchone()
        # print("fetched password: ", pwd['password'])
        # print("entered password: ", password_db_string)

        if pwd is None:
            print("no pwd found")
            flask.abort(403)
        elif pwd['password'] == password_db_string:
            flask.session['username'] = flask.request.form['username']
            if target is None:
                # flask.abort(403)
                return flask.redirect(flask.url_for('show_index'))
                # return flask.redirect('/')
            return flask.redirect(flask.url_for('show_index'))
            # return flask.redirect(pathlib.Path(target))
        else:
            print("incorrect pwd")
            flask.abort(403)

    elif operation == 'edit_account':
        connection = insta485.model.get_db()
        logname = flask.session['username']
        profilepic = flask.request.files['file']

        # flask.send_from_directory(
        # insta485.app.config['UPLOAD_FOLDER'], profilepic, as_attachment=True
        # )
        filename = profilepic.filename
        fullname = flask.request.form['fullname']
        email = flask.request.form['email']

        # create function to handle get photo
        # use send from directory
        # source = url_for
        # Unpack flask object
        fileobj = flask.request.files["file"]
        if fileobj.filename != "":
            filename = fileobj.filename
            # Compute base name (filename without directory).
            # We use a UUID to avoid
            # clashes with existing files, and ensure that the name
            # is compatible with the
            # filesystem.
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix
            if suffix != ('.jpg' or '.png' or '.jpeg' or 'heic'):
                flask.abort(400, description="Invalid file format")
            uuid_basename = f"{stem}{suffix}"
            # Save to disk
            path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            connection.execute(
                "UPDATE users SET fullname = ? , "
                "email = ? , filename = ? WHERE username = ?",
                (fullname, email, uuid_basename, logname, )
            )
        else:
            connection.execute(
                "UPDATE users SET fullname = ? , email = ? WHERE username = ?",
                (fullname, email, logname, )
            )
        if target is None:
            return flask.redirect(flask.url_for('show_edit'))
        return flask.redirect(target)

    elif operation == "create":
        if 'username' in flask.session:
            return flask.redirect(flask.url_for('show_edit'))

        connection = insta485.model.get_db()

        fullname = flask.request.form['fullname']
        username = flask.request.form['username']
        email = flask.request.form['email']
        password = flask.request.form['password']

        # check if user is trying to create an account
        # having an already existing username
        cur = connection.execute(
            'SELECT COUNT(*) FROM users WHERE username = ?',
            (username, )
        )
        res = cur.fetchone()
        if res['COUNT(*)'] > 0:
            print("Conflict error: username already exists")
            flask.abort(409)

        algorithm = 'sha512'
        salt = 'a45ffdcc71884853a2cba9e6bc55e812'
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        if suffix != ('.jpg' or '.png' or '.jpeg' or '.heic'):
            flask.abort(400, description="Invalid file format")
        uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        if (fullname == '' or username == ''
                or email == '' or password == '' or filename == ''):
            print("Error: one or more fields are empty")
            flask.abort(400)

        connection.execute(
            "INSERT INTO users "
            "(username, fullname, email, password, filename) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, fullname, email, password_db_string, uuid_basename, )
        )

        # cur = connection.execute(
        #     "SELECT * "
        #     "FROM users "
        #     "WHERE username = ?",
        #     (username, )
        # )
        # res = cur.fetchall()
        # print("entered password: ",password)
        # print("hashed pwd: ", password_db_string)
        # print("databse pwd: ", res)
        # print(res)
        flask.session['username'] = flask.request.form['username']

        if target is None:
            return flask.redirect(flask.url_for('show_index'))
        return flask.redirect(target)

    elif operation == "delete":
        connection = insta485.model.get_db()
        logname = flask.session['username']
        cur = connection.execute(
            "SELECT filename "
            "FROM posts "
            "WHERE owner = ?",
            (logname, )
        )
        res = cur.fetchall()
        print(res)
        for file in res:
            path = insta485.app.config["UPLOAD_FOLDER"]/file['filename']
            print(path)
            os.remove(path)

        connection.execute(
            "DELETE from users WHERE username = ? ",
            (logname, )
        )
        # change to show_create
        del flask.session['username']

        if target is None:
            return flask.redirect(flask.url_for('show_create'))
        return flask.redirect(target)

    elif operation == 'update_password':
        connection = insta485.model.get_db()
        password = flask.request.form['password']
        newpassword1 = flask.request.form['new_password1']
        newpassword2 = flask.request.form['new_password2']

        if (password is None or newpassword1 is None or newpassword2 is None):
            print("one or more required fields are empty")
            flask.abort(400)

        # Password salting and hashing
        algorithm = 'sha512'
        salt = 'a45ffdcc71884853a2cba9e6bc55e812'
        # uuid.uuid4().hex
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        # Connect and query database
        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ?",
            (flask.session['username'], )
        )

        # Check if correct password
        pwd = cur.fetchone()
        print("fetched password: ", pwd['password'])
        print("entered password: ", password_db_string)

        if pwd is None:
            print("no pwd found")
            flask.abort(403)
        elif pwd['password'] == password_db_string:
            print("old password verified")

        if newpassword1 != newpassword2:
            print("new passwords do not match")
            flask.abort(401)
        else:
            print("new passwords match")

        new_hash_obj = hashlib.new(algorithm)
        new_password_salted = salt + newpassword1
        new_hash_obj.update(new_password_salted.encode('utf-8'))
        new_password_hash = new_hash_obj.hexdigest()
        new_password_db_string = "$".join([algorithm, salt, new_password_hash])

        connection.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password_db_string, flask.session['username'], )
        )

        if target is None:
            return flask.redirect(flask.url_for('show_edit'))
        return flask.redirect(target)
