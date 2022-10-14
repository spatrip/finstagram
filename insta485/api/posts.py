"""REST API for posts."""
import hashlib
import operator
import flask
import insta485


@insta485.app.route('/api/v1/posts/')
def get_ten_posts():
    """Return 10 newest posts."""
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

    # Keep this for rememebering
    # postid_lte = 10
    # size = 10
    # page = -1
    # postid_lte = flask.request.args.get('postid_lte')
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=1, type=int)
    # size or page can't be negative (test case)
    if size < 0 or page < 0:
        flask.abort(400)
    # here we can do if not size size eq 10
    # postid_lte is largest post in the page that were working on
    # size
    # if not postid_lte:
    #     postid_lte =

    # Connect to database
    connection = insta485.model.get_db()
    # Query database
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (user, )
    )
    users = cur.fetchall()

    feed_post_owners_list = [user]

    for row in users:
        feed_post_owners_list.append(row['username2'])

    postinfo = []
    for userid in feed_post_owners_list:
        cur = -1
        # keep this
        # if size:
        #     cur = connection.execute(
        #     "SELECT postid, owner, filename, created "
        #     "FROM posts "
        #     "WHERE owner = ? ",
        #     "LIMIT = ? "
        #     # "ORDER BY postid DESC ",
        #     (userid, size, )
        # )
        # else:
        cur = connection.execute(
            "SELECT postid, owner, filename, created "
            "FROM posts "
            "WHERE owner = ? ",
            # "ORDER BY postid DESC ",
            (userid, )
        )

        info = cur.fetchall()
        # print("info: ", info)

        for container in info:
            postinfo.append(container)
    # print("posts: ", postinfo)
    sorted_posts = sorted(
        postinfo, key=operator.itemgetter('postid'), reverse=True)
    # print("sorted posts: ", sorted_posts)
    top_ten = sorted_posts[:10]
    # print(top_ten)
    results = []
    for post in top_ten:
        results.append(
            {"postid": post['postid'],
             "url": "/api/v1/posts/" + str(post['postid']) + "/"
             }
        )

    context = {
        "next": "",
        "results": results,
        "url": "/api/v1/posts/"
    }
    return flask.jsonify(**context)


@ insta485.app.route('/api/v1/posts/<int:postid>/')
def get_post(postid):
    """Return post information."""
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
        "SELECT owner, filename, created "
        "FROM posts "
        "WHERE postid = ?",
        (postid, )
    )
    res1 = cur1.fetchone()

    # postid does not exist
    if res1 is None:
        flask.abort(404)

    var = res1['owner']
    cur2 = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?",
        (var, )
    )
    res2 = cur2.fetchone()

    cur3 = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE postid = ?",
        (postid, )
    )
    res3 = cur3.fetchone()

    cur4 = connection.execute(
        "SELECT owner, text, commentid "
        "FROM comments "
        "WHERE postid = ?",
        (postid, )
    )
    res4 = cur4.fetchall()
    list_of_comments = []
    for entry in res4:
        list_of_comments.append({"commentid": entry['commentid'],
                                 "lognameOwnsThis": user == entry['owner'],
                                 "owner": entry['owner'],
                                 "ownerShowUrl": "/users/" +
                                 entry['owner'] +
                                 "/",
                                 "text": entry['text'],
                                 "url": "/api/v1/comments/" +
                                 str(entry['commentid']) +
                                 "/"
                                 })

    cur5 = connection.execute(
        "SELECT COUNT(*), likeid "
        "FROM likes "
        "WHERE owner = ?"
        "AND postid = ?",
        (user, postid, )
    )
    res5 = cur5.fetchone()

    if res5['COUNT(*)'] == 1:
        likeurl = "/api/v1/likes/" + str(res5['likeid']) + "/"
    else:
        likeurl = None

    context = {"comments": list_of_comments,
               "comments_url": "/api/v1/comments/?postid=" + str(postid),
               "created": res1['created'],
               "imgUrl": '/uploads/' + res1['filename'],
               "likes": {"lognameLikesThis": res5['COUNT(*)'] == 1,
                         "numLikes": res3['COUNT(*)'],
                         "url": likeurl
                         },
               "owner": res1['owner'],
               "ownerImgUrl": '/uploads/' + res2['filename'],
               "ownerShowUrl": "/users/" + res1['owner'] + "/",
               "postShowUrl": "/posts/" + str(postid) + "/",
               "postid": postid,
               "url": "/api/v1/posts/" + str(postid) + "/"
               }
    return flask.jsonify(**context)
