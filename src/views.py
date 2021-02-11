import pdb

from flask import jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
from google.auth.transport import requests
from google.oauth2 import id_token

from src.configs import db, GOOGLE_CLIENT_ID
from src.gateway import GooglePeopleGateway
from src.models import User, Contact, Organization


@login_required
def dashboard():
    gateway = GooglePeopleGateway()
    access_token = request.args.get('access_token')
    accounts = gateway.get_contacts(access_token)

    for account in accounts['connections']:
        if account.get('organizations') is not None:
            for organization in account['organizations']:
                m_organization = Organization.query.filter_by(name=organization['name']).first()
                if m_organization is None:
                    m_organization = Organization(name=organization['name'])
                if account.get('emailAddresses') is not None:
                    for email in account.get('emailAddresses'):
                        contact = Contact.query.filter_by(email=email['value']).first()
                        if contact is None:
                            contact = Contact(email=email['value'])
                        m_organization.contacts.append(contact)
                        db.session.add(contact)
                db.session.add(m_organization)

    db.session.add(current_user)
    db.session.commit()
    if current_user.is_authenticated:
        data = {'accounts': [{'organization': o.name, "emails": [e.email for e in o.contacts]} for o in Organization.query.all()]}
        return jsonify(data)
    else:
        return jsonify({"message": "faça login para acessar as funcionalidades."})


def login():
    try:
        # pdb.set_trace()
        idinfo = id_token.verify_oauth2_token(
            request.args.get("id_token"),
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        if idinfo['email_verified']:
            user = User.query.filter_by(email=idinfo['email']).first()
            if not user:
                user = User(
                    unique_id=idinfo['sub'],
                    name=idinfo['name'],
                    email=idinfo['email'],
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


def logout():
    logout_user()
    return jsonify({"message": "O usuário foi deslogado"})
