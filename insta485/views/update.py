"""Update likes,comments, etc."""
import uuid
import pathlib
import os
import flask
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def update_like():
    """Update like count."""
    operation = flask.request.form['operation']
    postid = flask.request.form['postid']
    logname = flask.session['username']
    target = flask.request.args.get('target')

    # print(operation)

    connection = insta485.model.get_db()

    if operation == 'like':
        # print("like clicked")
        # likes = connection.execute(
        #     "SELECT COUNT(*) "
        #     "FROM likes "
        #     "WHERE postid = ?",
        #     (postid, )
        # )
        # liked = likes.fetchone()['COUNT(*)']
        # if liked > 0:
        #     flask.abort(409)
        connection.execute(
            "INSERT INTO likes (owner, postid) VALUES ( ? , ? )",
            (logname, postid, )
        )

    elif operation == 'unlike':
        # print("unlike clicked")
        # likes = connection.execute(
        #     "SELECT COUNT(*) "
        #     "FROM likes "
        #     "WHERE postid = ?",
        #     (postid, )
        # )
        # liked = likes.fetchone()['COUNT(*)']
        # if liked == 0:
        #     flask.abort(409)
        connection.execute(
            "DELETE FROM likes WHERE owner = ? AND postid = ?",
            (logname, postid, )
        )

    # cur = connection.execute(
    #     "SELECT * "
    #     "FROM likes "
    # )
    # if target specified
    # res = cur.fetchall()
    # print(res)
    if target is None:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


@insta485.app.route('/comments/', methods=['POST'])
def update_comment():
    """Add/delete comment."""
    connection = insta485.model.get_db()
    target = flask.request.args.get('target')

    logname = flask.session['username']
    # text = flask.request.form['text']
    operation = flask.request.form['operation']

    if operation == 'create':
        text = flask.request.form['text']
        postid = flask.request.form['postid']
        connection.execute(
            "INSERT INTO comments (owner, postid, text) VALUES ( ? , ?, ? )",
            (logname, postid, text, )
        )
    # only called from post page
    elif operation == 'delete':
        print('entered')
        commentid = flask.request.form['commentid']
        print(commentid)
        print("commentid: ", commentid)

        cur = connection.execute(
            "SELECT owner FROM comments WHERE commentid = ?",
            (commentid, )
        )
        res = cur.fetchone()

        if res['owner'] != flask.session['username']:
            # print("Permission denied")
            flask.abort(403, description="Permission denied")

        connection.execute(
            "DELETE FROM comments WHERE commentid = ?",
            (commentid, )
        )
        # leave this here
        # cur = connection.execute(
        #     "SELECT * "
        #     "FROM comments"
        # )
        # res = cur.fetchall()
        # print(res)

    if target is None:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


@insta485.app.route('/posts/', methods=['POST'])
def delete_post():
    """Delete a post."""
    postid = flask.request.form['postid']
    # logname = flask.session['username']
    target = flask.request.args.get('target')
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename, owner "
        "FROM posts "
        "WHERE postid = ?",
        (postid,)
    )

    res = cur.fetchone()

    if res['owner'] != flask.session['username']:
        print("Permission denied")
        flask.abort(403)

    connection.execute(
        "DELETE FROM posts WHERE postid = ?",
        (postid, )
    )

    path = insta485.app.config["UPLOAD_FOLDER"]/res['filename']
    os.remove(path)
    # print('yoohoo', target)
    if target is None:
        return flask.redirect(flask.url_for('show_user',
                                            user_url_slug=res['owner']))
    # else:
    return flask.redirect(target)


@insta485.app.route('/following/', methods=['POST'])
def update_following():
    """Change following status."""
    username = flask.request.form['username']
    connection = insta485.model.get_db()
    logname = flask.session['username']
    operation = flask.request.form['operation']
    target = flask.request.args.get('target')

    if operation == 'follow':
        connection.execute(
            "INSERT INTO following (username1, username2) VALUES ( ? , ? )",
            (logname, username, )
        )

    elif operation == 'unfollow':
        connection.execute(
            "DELETE FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username, )
        )

    if target is None:
        return flask.redirect(flask.url_for('show_index'))
    # else:
    return flask.redirect(target)


@insta485.app.route('/users/', methods=['POST'])
def create_post():
    """Create a new post."""
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    if filename == '':
        flask.abort(400, description="Empty file")
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    print(suffix)
    if suffix != ('.jpg' or '.png' or '.jpeg' or '.heic'):
        flask.abort(400, description="Invalid file format")
    uuid_basename = f"{stem}{suffix}"
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    logname = flask.session['username']
    target = flask.request.args.get('target')
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO posts (filename, owner) VALUES ( ? , ? )",
        (uuid_basename, logname, )
    )
    if target is None:
        return flask.redirect(flask.url_for('show_index'))
    # else:
    return flask.redirect(target)
