import pdb

from flask_login import LoginManager

from src.configs import *
from src.models import User
from src.views import login, logout, refresh_contacts, contacts, index

login_manager = LoginManager(app)


@login_manager.request_loader
def load_user_from_request(request):
    return User.query.filter_by(unique_id=request.args.get('unique_id')).first()


app.add_url_rule('/', 'index', index)
app.add_url_rule('/contacts', 'contacts', contacts)
app.add_url_rule('/login', 'login', login)
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/refresh-contacts', 'refresh_contacts', refresh_contacts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
