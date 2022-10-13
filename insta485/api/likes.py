"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/likes/')
def create_like():
    """Creates a like for the given postid."""

    if 'username' not in flask.session:
        return flask.abort(403)
    else:
        user = flask.session['username']

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
                   "url": "/api/v1/likes/{}/".format(res1['likeid']),
                   "was_liked": True}
        return flask.jsonify(**context), 201
    else:
        cur2 = connection.execute(
            "INSERT INTO likes (owner, postid) VALUES ( ? , ? ) "
            "RETURNING likeid",
            (user, postid, )
        )
        res2 = cur2.fetchone()
        context = {"likeid": res2['likeid'],
                   "url": "/api/v1/likes/{}/".format(res2['likeid']),
                   "was_liked": False}
        return flask.jsonify(**context), 200
