"""Explore page."""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Show a user's explore page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()

    cur1 = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username != ? "
        "EXCEPT "
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname, logname, )
    )
    not_followings = cur1.fetchall()

    for not_following in not_followings:
        cur2 = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, not_following['username'], )
        )
        log = cur2.fetchone()

        logname_follows_user = log['COUNT(*)'] == 1

        not_following['logname_follows_username'] = logname_follows_user

        cur3 = connection.execute(
            "SELECT filename as user_img_url "
            "FROM users "
            "WHERE username = ?",
            (not_following['username'], )
        )
        img = cur3.fetchone()
        img['user_img_url'] = '/uploads/' + img['user_img_url']
        not_following['user_img_url'] = img['user_img_url']

    # print(followers)
    context = {"logname": logname,
               "not_following": not_followings
               }
    # print(context)
    return flask.render_template('explore.html', **context)
