"""REST API for returning list of services."""
import flask
import insta485


@insta485.app.route('/api/v1/')
def show_services():
    """Return list of services."""

    # use commented code below for aborting when not authenticated in other api calls
    # if 'username' not in flask.session:
    #     return flask.abort(403)
    # else:
    #     user = flask.session['username']

    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)
