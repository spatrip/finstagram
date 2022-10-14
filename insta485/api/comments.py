"""REST API for comments."""
import flask
import insta485


@insta485.app.route('/api/v1/comments/')
def create_like():
    """Creates a like for the given postid."""

    if 'username' not in flask.session:
        return flask.abort(403)
    else:
        user = flask.session['username']