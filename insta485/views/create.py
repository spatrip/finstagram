"""Create Account page."""
import flask
import insta485


@insta485.app.route('/accounts/create/')
def show_create():
    """Display create page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_edit'))
    return flask.render_template("create.html")
