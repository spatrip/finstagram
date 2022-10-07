"""User page."""
import flask
import insta485


@insta485.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):
    """Show user page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()

    cur1 = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username1 = ? "
        "AND username2 = ?",
        (logname, user_url_slug, )
    )
    log = cur1.fetchone()

    logname_follows_user = log['COUNT(*)'] == 1

    cur2 = connection.execute(
        "SELECT fullname, filename "
        "FROM users "
        "WHERE username = ?",
        (user_url_slug, )
    )
    user_info = cur2.fetchone()

    cur3 = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username1 = ?",
        (user_url_slug, )
    )
    following = cur3.fetchone()

    cur4 = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username2 = ?",
        (user_url_slug, )
    )
    followers = cur4.fetchone()

    cur5 = connection.execute(
        "SELECT COUNT(*) "
        "FROM posts "
        "WHERE owner = ?",
        (user_url_slug, )
    )
    numposts = cur5.fetchone()

    cur6 = connection.execute(
        "SELECT postid, filename AS 'img_url' "
        "FROM posts "
        "WHERE owner = ?",
        (user_url_slug, )
    )

    posts = cur6.fetchall()
    for post in posts:
        post['img_url'] = '/uploads/' + post['img_url']
    # print(posts)

    context = {"logname": logname,
               "username": user_url_slug,
               "logname_follows_username": logname_follows_user,
               "fullname": user_info['fullname'],
               "user_img_url": '/uploads/' + user_info['filename'],
               "following": following["COUNT(*)"],
               "followers": followers["COUNT(*)"],
               "total_posts": numposts["COUNT(*)"],
               "posts": posts}
    return flask.render_template('user.html', **context)


@insta485.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """Logout."""
    if 'username' in flask.session:
        del flask.session['username']

    return flask.redirect(flask.url_for('show_login'))
