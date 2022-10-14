"""REST API for posts."""
import operator
import flask
import insta485


@insta485.app.route('/api/v1/posts/')
def get_ten_posts():
    """Returns 10 newest posts."""

    if 'username' not in flask.session:
        return flask.abort(403)
    else:
        user = flask.session['username']

    # Keep this for rememebering
    # postid_lte = 10
    # size = 10
    # page = -1
    # postid_lte = flask.request.args.get('postid_lte')
    # size = flask.request.args.get("size", default=<some number>, type=int
    # page = flask.request.args.get("page", default=<some number>, type=int
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
            {"postid": post['postid'], "url": "/api/v1/posts/{}/".format(post['postid'])})

    context = {
        "next": "",
        "results": results,
        "url": "/api/v1/posts/"
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/<int:postid>/')
def get_post(postid):
    """Returns post information"""

    if 'username' not in flask.session:
        return flask.abort(403)
    else:
        user = flask.session['username']

    connection = insta485.model.get_db()
    cur1 = connection.execute(
        "SELECT owner, filename, created "
        "FROM posts "
        "WHERE postid = ?",
        (postid, )
    )
    res1 = cur1.fetchone()
    # print(res1)

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
    listOfComments = []
    for entry in res4:
        listOfComments.append({"commentid": entry['commentid'],
                              "lognameOwnsThis": user == entry['owner'],
                               "owner": entry['owner'],
                               "ownerShowUrl": "/users/{}/".format(entry['owner']),
                               "text": entry['text'],
                               "url": "/api/v1/comments/{}/".format(entry['commentid'])
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
        likeurl = "/api/v1/likes/{}/".format(res5['likeid'])
    else:
        likeurl = None

    context = {"comments": listOfComments,
               "comments_url": "/api/v1/comments/?postid={}/".format(postid),
               "created": res1['created'],
               "imgUrl": '/uploads/' + res1['filename'],
               "likes": {"lognameLikesThis": res5['COUNT(*)'] == 1,
                         "numLikes": res3['COUNT(*)'],
                         "url": likeurl
                         },
               "owner": res1['owner'],
               "ownerImgUrl": '/uploads/' + res2['filename'],
               "ownerShowUrl": "/users/{}/".format(res1['owner']),
               "postShowUrl": "/posts/{}/".format(postid),
               "postid": postid,
               "url": "/api/v1/posts/{}/".format(postid)
               }
    return flask.jsonify(**context)
