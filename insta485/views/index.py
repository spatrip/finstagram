"""Insta485 index (main) view."""
# import pathlib
import operator
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display index page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    # else:
    user = flask.session['username']

    # print("logged in user: ", user)
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
    if len(users) == 0:
        num_following = 0
    else:
        num_following = 1
    feed_post_owners_list = [user]

    for row in users:
        feed_post_owners_list.append(row['username2'])
    # print(feed_post_owners_list)
    posts = []
    postinfo = []
    for userid in feed_post_owners_list:
        cur = connection.execute(
            "SELECT postid, owner, filename, created "
            "FROM posts "
            "WHERE owner = ? "
            "ORDER BY postid DESC ",
            (userid, )
        )
        info = cur.fetchall()
        # print(info)

        for container in info:
            postinfo.append(container)
        # print(postinfo)

        sorted_posts = sorted(
            postinfo, key=operator.itemgetter('postid'), reverse=True)

    for post in sorted_posts:
        img_path = '/uploads/' + post['filename']
        pfps = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (post['owner'], )
        )
        pic = pfps.fetchone()

        likes = connection.execute(
            "SELECT COUNT(*) "
            "FROM likes "
            "WHERE postid = ?",
            (post['postid'], )
        )

        numlikes = likes.fetchone()

        comms = connection.execute(
            "SELECT owner, text "
            "FROM comments "
            "WHERE postid = ?",
            (post['postid'], )
        )

        comments = comms.fetchall()
        # print(comments)

        likew = connection.execute(
            "SELECT COUNT(*) "
            "FROM likes "
            "WHERE owner = ?"
            "AND postid = ?",
            (user, post['postid'], )
        )
        liked = False
        # print(liked)
        if likew.fetchone()['COUNT(*)'] == 1:
            liked = True

        posts.append(
            {"postid": post['postid'], "owner": post['owner'],
             "owner_img_url": '/uploads/' + pic['filename'],
             "img_url": img_path,
             "timestamp": arrow.get(post['created']).humanize(),
             "likes": numlikes['COUNT(*)'], "comments": comments,
             "is_liked": liked})
    # Add database info to context
    # print(posts)
    context = {"logname": user, "following": num_following, "posts": posts}
    # print(context)
    return flask.render_template("index.html", **context)


@insta485.app.route('/accounts/login/')
def show_login():
    """Display login page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    # else:
    return flask.render_template("login.html")


@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Get pictures."""
    return flask.send_from_directory(
        insta485.app.config['UPLOAD_FOLDER'], filename, as_attachment=True
    )

# @insta485.app.route('/static/images/logo.png')
# def serve_logo():
#     """Get logo"""
#     return flask.send_from_directory(
#         insta485.app.config['STATIC_IMAGES_FOLDER'],
#           'logo.png', as_attachment=True
#     )


# @insta485.app.route('/likes/', methods=['POST'])
# def handle_likes():
#     """ Handle likes """
