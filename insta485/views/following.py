"""Followers page."""
import flask
import insta485


@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """Show a user's following page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()

    cur1 = connection.execute(
        "SELECT username2 AS username "
        "FROM following "
        "WHERE username1 = ?",
        (user_url_slug, )
    )
    followings = cur1.fetchall()
    # print(followers)

    for following in followings:
        cur2 = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, following['username'], )
        )
        log = cur2.fetchone()

        logname_follows_user = False
        if log['COUNT(*)'] == 1:
            logname_follows_user = True

        following['logname_follows_username'] = logname_follows_user

        cur3 = connection.execute(
            "SELECT filename as user_img_url "
            "FROM users "
            "WHERE username = ?",
            (following['username'], )
        )
        img = cur3.fetchone()
        img['user_img_url'] = '/uploads/' + img['user_img_url']
        following['user_img_url'] = img['user_img_url']

    # print(followers)
    context = {"logname": logname,
               "following": followings
               }
    print(context)
    return flask.render_template('following.html', **context)
