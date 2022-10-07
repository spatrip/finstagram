"""Post page."""
import flask
import arrow
import insta485


@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    """Show post."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['username']

    connection = insta485.model.get_db()
    cur1 = connection.execute(
        "SELECT owner, filename, created "
        "FROM posts "
        "WHERE postid = ?",
        (postid_url_slug, )
    )
    res1 = cur1.fetchone()
    print(res1)

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
        (postid_url_slug, )
    )
    res3 = cur3.fetchone()

    cur4 = connection.execute(
        "SELECT owner, text, commentid "
        "FROM comments "
        "WHERE postid = ?",
        (postid_url_slug, )
    )
    res4 = cur4.fetchall()

    cur5 = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE owner = ?"
        "AND postid = ?",
        (logname, postid_url_slug, )
    )
    res5 = cur5.fetchone()['COUNT(*)'] == 1

    context = {"logname": logname, "postid": postid_url_slug,
               "owner": res1['owner'],
               "is_liked": res5,
               "img_url": '/uploads/' + res1['filename'],
               "timestamp": arrow.get(res1['created']).humanize(),
               "owner_img_url": '/uploads/' + res2['filename'],
               "likes": res3['COUNT(*)'], "comments": res4}

    return flask.render_template("post.html", **context)
