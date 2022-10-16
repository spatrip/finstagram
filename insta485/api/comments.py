"""REST API for comments."""
import hashlib
import flask
import insta485


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def create_comment():
    """Create a comment for the given postid and text."""
    # AUTHENTICATION BEGIN

    if flask.request.authorization:
        user = flask.request.authorization['username']
        print("http auth user: ", user)
        password = flask.request.authorization['password']

        # Password salting and hashing
        # algorithm = 'sha512'
        # salt = 'a45ffdcc71884853a2cba9e6bc55e812'
        # uuid.uuid4().hex
        hash_obj = hashlib.new('sha512')
        password_salted = 'a45ffdcc71884853a2cba9e6bc55e812' + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join(
            ['sha512', 'a45ffdcc71884853a2cba9e6bc55e812', password_hash])

        # Connect and query database
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ?",
            (user, )
        )

        # Check if correct password
        pwd = cur.fetchone()

        if pwd is None:
            print("no pwd found")
            flask.abort(403)
        elif pwd['password'] == password_db_string:
            # authenticated
            print("User Authenticated")
        else:
            print("incorrect pwd")
            flask.abort(403)

    else:
        if 'username' not in flask.session:
            return flask.abort(403)
        # else:
        user = flask.session['username']
        # mexi.authorization()
    # AUTHENTICATION OVER

    text = flask.request.json.get("text", None)

    if not text:
        return flask.jsonify({}), 400

    postid = flask.request.args.get('postid')
    connection = insta485.model.get_db()

    cur1 = connection.execute(
        "INSERT INTO comments (owner, postid, text) VALUES ( ? , ?, ? )"
        "RETURNING commentid, owner",
        (user, postid, text, )
    )

    res1 = cur1.fetchone()

    context = {"commentid": res1['commentid'],
               "lognameOwnsThis": user == res1['owner'],
               "owner": user,
               "ownerShowUrl": "/users/" + user + "/",
               "text": text,
               "url": "/api/v1/comments/" + str(res1['commentid']) + "/"
               }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Delete a comment with the given likeid."""
    # AUTHENTICATION BEGIN

    if flask.request.authorization:
        user = flask.request.authorization['username']
        print("http auth user: ", user)
        password = flask.request.authorization['password']

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
            (user, )
        )

        # Check if correct password
        pwd = cur.fetchone()

        if pwd is None:
            print("no pwd found")
            flask.abort(403)
        elif pwd['password'] == password_db_string:
            # authenticated
            print("User Authenticated")
        else:
            print("incorrect pwd")
            flask.abort(403)

    else:
        if 'username' not in flask.session:
            return flask.abort(403)
        # else:
        user = flask.session['username']

    # AUTHENTICATION OVER

    connection = insta485.model.get_db()
    cur1 = connection.execute(
        "SELECT COUNT(*), commentid, owner "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid, )
    )

    res1 = cur1.fetchone()
    # no such commentid
    if res1['COUNT(*)'] == 0:
        flask.abort(404)
    # logged in user doesn't own comment
    if res1['owner'] != user:
        flask.abort(403)

    connection.execute(
        "DELETE FROM comments WHERE owner = ? AND commentid = ?",
        (user, commentid, )
    )

    return "", 204
