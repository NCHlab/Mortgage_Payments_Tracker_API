from typing import List, Type
import pandas as pd


def csv_parser(data: List[dict], filename: str) -> None:

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def xlsx_parser(data: List[dict], filename: str, is_multi: bool = False) -> None:

    writer = pd.ExcelWriter(filename, engine="openpyxl")

    if is_multi:
        xlsx_complex_parser(data, writer)
    else:
        xlsx_simple_parser(data, writer)

    writer.save()


def xlsx_simple_parser(data: dict, writer: Type[pd.ExcelWriter]):
    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name="data", index=False)


def xlsx_complex_parser(data: dict, writer: Type[pd.ExcelWriter]):

    list_of_users = []

    for x in data:
        if x["user_id"] not in list_of_users:
            list_of_users.append(x["user_id"])

    list_of_sheet_data = [[] for x in range(len(list_of_users))]

    for idx, username in enumerate(list_of_users):
        for _dict in data:
            if _dict["user_id"] == username:
                list_of_sheet_data[idx].append(_dict)

    df = []
    for data in list_of_sheet_data:
        df.append(pd.DataFrame(data))

    for idx, dataframe in enumerate(df):
        dataframe.to_excel(writer, sheet_name=list_of_users[idx], index=False)
