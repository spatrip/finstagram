"""Change password."""
import flask
import insta485


@insta485.app.route('/accounts/password/')
def show_password():
    """Change password."""
    if 'username' not in flask.session:
        flask.redirect(flask.url_for('show_index'))

    return flask.render_template('password.html',
                                 **{'logname': flask.session['username']})
