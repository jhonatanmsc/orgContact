from flask import jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from google.auth.transport import requests
from google.oauth2 import id_token

from src.configs import *
from src.models import User

login_manager = LoginManager()
login_manager.init_app(app)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return jsonify({
            "unique_id": current_user.unique_id,
            "name": current_user.name,
            "email": current_user.email,
            "picture": current_user.picture,
            "given_name": current_user.given_name,
            "family_name": current_user.family_name,
            "locale": current_user.locale
        })
    else:
        return jsonify({"message": "faça login para acessar as funcionalidades."})


@app.route('/login')
def google_login(request):
    try:
        idinfo = id_token.verify_oauth2_token(
            request.args.get("access_token"),
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        if idinfo['email_verified']:
            user = User.get(idinfo['email'])
            if not user:
                user = User(
                    unique_id=idinfo['sub'],
                    name=idinfo['name'],
                    picture=idinfo['picture'],
                    given_name=idinfo['given_name'],
                    family_name=idinfo['family_name'],
                    locale=idinfo['locale']
                )
                db.session.add(user)
                db.session.commit()

            login_user(user)
            return jsonify({"message": f"Usuário autenticado."})
        else:
            return jsonify({"message": f"O google não conseguiu verificar o email."}), 400
    except ValueError:
        return jsonify({"message": "O token é inválido."}), 400


@app.route('/logout')
def logout():
    logout_user()
    return jsonify({"message": "O usuário foi deslogado"})
