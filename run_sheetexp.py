import argparse
import csv
import shutil
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def parse_arguments():
    """Parse arguments when executed from CLI"""
    parser = argparse.ArgumentParser(
        prog="GSheet",
        description="CLI tool for read/update Google Spread sheet",
    )
    parser.add_argument(
        "--environment",
        choices=["local", "dev", "prod"],
        default="dev",
        help="Environment parameter",
    )
    args = parser.parse_args()
    return args

SRC_DIR = Path(__file__).parent
LOCAL_DIR = SRC_DIR / "local"
DATA_DIR = SRC_DIR / "data"


def update_sheets():
    """Update sheets using the Google Sheets API"""
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    DATA_DIR.mkdir()

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        LOCAL_DIR / "credentials.json", scope
    )
    client = gspread.authorize(credentials)

    file_list = client.list_spreadsheet_files()
    print(file_list)

    workbook = client.open("Data tracking")
    for worksheet in workbook.worksheets():
    #     filename = DATA_DIR / (worksheet.title + ".csv")
        sheet_values = worksheet.get_all_values()
        print(sheet_values)
        header_row = worksheet.row_values(9)
        print(header_row)
        cell_list = worksheet.range('B10:N10')
        cell_values = [
                        ['SYMBOL', 'MARKET', 'NAME', 'DATE', 'OPEN', 'HIGH', 'LOW',
                            'CLOSE', 'COMMENT', '% DONE', 'FIXED COST', 'ESTIMATED HOURS', 'ACTUAL HOURS']
                       ]
        workbook.values_update(
            'Project Tracking!B10',
            params={
                'valueInputOption': 'RAW'
            },
            body={
                'values': cell_values
            }
        )


def main(args):
    print("### Update data from Google Sheets ###")
    update_sheets()

    pass


if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments)
