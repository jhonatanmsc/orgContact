import pdb
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.configs import *


class GooglePeopleGateway:
    SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']
    SERVICE_ACCOUNT_FILE = f'{BASE_DIR}/credentials.json'

    def get_contacts(self, access_token):
        """Shows basic usage of the People API.
            Prints the name of the first 10 connections.
            """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=3000)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        people_service = build('people', 'v1', credentials=creds)

        connections = people_service.people().connections().list(
            resourceName='people/me',
            access_token=access_token,
            personFields='emailAddresses,organizations').execute()

        return connections
