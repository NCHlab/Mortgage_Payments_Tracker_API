from typing import TextIO

from app.core.session import get_session
from app.service.download_service import (
    download_single_user,
    download_multi_user,
    download_csv_single_user,
    download_csv_multi_user,
    download_combined,
)
from flask import send_file


def get_download(tablename: str) -> TextIO:
    get_session()
    filename = download_single_user(tablename)

    return send_file(filename)


def get_all_download(tablename: str) -> TextIO:
    get_session()
    filename = download_multi_user(tablename)

    return send_file(filename)


def get_csv_download(tablename: str) -> TextIO:
    get_session()
    filename = download_csv_single_user(tablename)

    return send_file(filename)


def get_csv_all_download(tablename: str) -> TextIO:
    get_session()
    filename = download_csv_multi_user(tablename)

    return send_file(filename)


def get_combined_all_download():
    get_session()
    filename = download_combined()

    return filename

    # return send_file(filename)
