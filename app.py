import pdb

from flask_login import LoginManager

from src.configs import *
from src.models import User
from src.views import dashboard, login, logout

login_manager = LoginManager(app)


@login_manager.request_loader
def load_user_from_request(request):
    return User.query.filter_by(unique_id=request.args.get('unique_id')).first()


app.add_url_rule('/', 'dashboard', dashboard)
app.add_url_rule('/login', 'login', login)
app.add_url_rule('/logout', 'logout', logout)
