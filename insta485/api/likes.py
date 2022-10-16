"""REST API for likes."""
import hashlib
import flask
import insta485


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def create_like():
    """Create a like for the given postid."""
    # AUTHENTICATION BEGIN

    if flask.request.authorization:
        user = flask.request.authorization['username']
        print("http auth user: ", user)
        password = flask.request.authorization['password']

        # Password salting and hashing
        # algorithm = 'sha512'
        salt = 'a45ffdcc71884853a2cba9e6bc55e812'
        # uuid.uuid4().hex
        hash_obj = hashlib.new('sha512')
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join(['sha512', salt, password_hash])

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

    postid = flask.request.args.get('postid')

    connection = insta485.model.get_db()

    cur1 = connection.execute(
        "SELECT COUNT(*), likeid "
        "FROM likes "
        "WHERE owner = ?"
        "AND postid = ?",
        (user, postid, )
    )
    res1 = cur1.fetchone()

    if res1['COUNT(*)'] == 1:
        context = {"likeid": res1['likeid'],
                   "url": "/api/v1/likes/" + str(res1['likeid']) + "/"
                   }
        return flask.jsonify(**context), 200
    # else:
    # Changed from cur2
    cur1 = connection.execute(
        "INSERT INTO likes (owner, postid) VALUES ( ? , ? ) "
        "RETURNING likeid",
        (user, postid, )
    )
    # Changed from cur2
    res2 = cur1.fetchone()
    context = {"likeid": res2['likeid'],
               "url": "/api/v1/likes/" + str(res2['likeid']) + "/"
               }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Delete a like with the given likeid."""
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
        "SELECT COUNT(*), likeid, owner "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid, )
    )

    res1 = cur1.fetchone()
    # no such likeid
    if res1['COUNT(*)'] == 0:
        flask.abort(404)
    # logged in user doesn't own like
    if res1['owner'] != user:
        flask.abort(403)

    connection.execute(
        "DELETE FROM likes WHERE owner = ? AND likeid = ?",
        (user, likeid, )
    )

    return "", 204
