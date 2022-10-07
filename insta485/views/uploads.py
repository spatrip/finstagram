"""Manages upload viewing permissions."""
# import flask
# import os
# import flask
# import insta485


# @insta485.app.route('/uploads/<filename>/')
# def show_upload(filename):
#     """Manages upload viewing permissions."""
#     if 'username' not in flask.session:
#         print("Permission denied: log in to view")
#         flask.abort(403)

#     target = f'/uploads/{filename}/'

#     if not os.path.exists(target):
#         print("Error: user tried to access a file that doesn't exist")
#         flask.abort(404)

#     return flask.redirect(target)
