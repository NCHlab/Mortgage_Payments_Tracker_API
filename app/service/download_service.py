from app.core.session import get_session
from app.core.parsers import parse_filename
from app.service.common import get_from_table, get_all_from_table
from app.core.file_parser import csv_parser, xlsx_parser, xlsx_combined_parser


def download_single_user(tablename: str) -> str:
    data = get_from_table(tablename)
    filename = parse_filename("single", tablename, "xlsx")
    xlsx_parser(data, filename)

    return filename


def download_multi_user(tablename: str) -> str:
    data = get_all_from_table(tablename)
    filename = parse_filename("multi", tablename, "xlsx")
    xlsx_parser(data, filename, is_multi=True)

    return filename


def download_csv_single_user(tablename: str) -> str:

    data = get_from_table(tablename)
    filename = parse_filename("single", tablename, "csv")
    csv_parser(data, filename)

    return filename


def download_csv_multi_user(tablename: str) -> str:

    data = get_all_from_table(tablename)
    filename = parse_filename("multi", tablename, "csv")
    csv_parser(data, filename)

    return filename


def download_combined() -> str:

    payments = get_all_from_table("payments")
    overpayments = get_all_from_table("overpayments")
    other_payments = get_all_from_table("other_payments")

    payment_information = [payments, overpayments, other_payments]

    filename = xlsx_combined_parser(payment_information)

    return filename
