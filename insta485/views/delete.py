"""Delete page."""
import flask
import insta485


@insta485.app.route('/accounts/delete/')
def show_delete():
    """Display delete page."""
    if 'username' in flask.session:
        return flask.render_template("delete.html",
                                     **{'logname': flask.session['username']})
    return flask.redirect(flask.url_for('show_login'))
