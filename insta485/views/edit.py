"""Edit page."""
import flask
import insta485


@insta485.app.route('/accounts/edit/', methods=['GET'])
def show_edit():
    """Edit account details."""
    connection = insta485.model.get_db()

    logname = flask.session['username']

    cur = connection.execute(
        "SELECT fullname, email, filename FROM users WHERE username = ?",
        (logname, )
    )
    res = cur.fetchone()

    # cur1 = connection.execute(
    #     "SELECT email FROM users WHERE username = ?",
    #     (logname, )
    # )
    # email = cur1.fetchone()

    context = {
            "logname": logname,
            "fullname": res['fullname'],
            "logname_photo": '/uploads/'+res['filename'],
            "email": res['email']
    }
    print("test")
    return flask.render_template("edit.html", **context)
