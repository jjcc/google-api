# Basic framework for accessing google sheet
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
import pandas as pd


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = ''
RANGE_NAME = ''


def load_env():
    global SPREADSHEET_ID, RANGE_NAME
    load_dotenv()
    SPREADSHEET_ID = os.getenv('SHEET_ID')
    RANGE_NAME = os.getenv('RANGE_NAME')

def load_creds():
    """
    load credentials from json file. The json file is a OAuth credential available for download in developer console
    :return: credential
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def load_data():
    """
    """
    # load SPREADSHEET_ID from environment file
    load_env()
    # load credentials
    creds = load_creds()
    # initiate service
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values')

    df = pd.DataFrame(values)
    return df


def main():
    data = load_data()
    print(data.head())



if __name__ == '__main__':
    main()
