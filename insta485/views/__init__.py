"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.index import show_login
from insta485.views.index import download_file
# from insta485.views.index import serve_logo
from insta485.views.login import handle_login
from insta485.views.user import show_user
from insta485.views.followers import show_followers
from insta485.views.following import show_following
from insta485.views.explore import show_explore
from insta485.views.user import show_logout
from insta485.views.post import show_post
from insta485.views.update import update_like
from insta485.views.edit import show_edit
from insta485.views.delete import show_delete
from insta485.views.create import show_create
from insta485.views.password import show_password
# from insta485.views.uploads import show_upload
