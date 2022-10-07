"""Followers page."""
import flask
import insta485


@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """Show a user's followers page."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()

    cur1 = connection.execute(
        "SELECT username1 AS username "
        "FROM following "
        "WHERE username2 = ?",
        (user_url_slug, )
    )
    followers = cur1.fetchall()
    # print(followers)

    for follower in followers:
        cur2 = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, follower['username'], )
        )
        log = cur2.fetchone()

        logname_follows_user = log['COUNT(*)'] == 1

        # if log['COUNT(*)'] is 1:
        #     logname_follows_user = True
        # else:
        #     logname_follows_user = False

        follower['logname_follows_username'] = logname_follows_user

        cur3 = connection.execute(
            "SELECT filename as user_img_url "
            "FROM users "
            "WHERE username = ?",
            (follower['username'], )
        )
        img = cur3.fetchone()
        img['user_img_url'] = '/uploads/' + img['user_img_url']
        follower['user_img_url'] = img['user_img_url']

    # print(followers)
    context = {"logname": logname,
               "followers": followers
               }
    print(context)
    return flask.render_template('followers.html', **context)
