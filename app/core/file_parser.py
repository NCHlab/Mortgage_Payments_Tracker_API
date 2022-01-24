from typing import List, Type
import pandas as pd
from datetime import datetime


def csv_parser(data: List[dict], filename: str) -> None:

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def xlsx_parser(data: List[dict], filename: str, is_multi: bool = False) -> None:

    writer = pd.ExcelWriter(filename, engine="openpyxl")

    if is_multi:
        list_of_sheet_data, list_of_users = xlsx_complex_parser(data)
        list_to_df_xlsx(writer, list_of_sheet_data, list_of_users)
    else:
        xlsx_simple_parser(data, writer)

    writer.save()


def xlsx_simple_parser(data: dict, writer: Type[pd.ExcelWriter]):
    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name="data", index=False)


def xlsx_complex_parser(data: dict):
    """
    Takes in a dictionary that is unordered

    Returns List of data sectioned by name
    """

    list_of_users = []

    for x in data:
        if x["user_id"] not in list_of_users:
            list_of_users.append(x["user_id"])

    list_of_sheet_data = [[] for x in range(len(list_of_users))]

    for idx, username in enumerate(list_of_users):
        for _dict in data:
            if _dict["user_id"] == username:
                list_of_sheet_data[idx].append(_dict)

    return list_of_sheet_data, list_of_users


def list_to_df_xlsx(writer: Type[pd.ExcelWriter], list_of_sheet_data, list_of_users):
    df = []
    for data in list_of_sheet_data:
        df.append(pd.DataFrame(data))

    for idx, dataframe in enumerate(df):
        dataframe.to_excel(writer, sheet_name=list_of_users[idx], index=False)


def multiple_dfs(df_list, sheets, spaces, writer):

    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
        row = row + len(dataframe.index) + spaces + 1


def xlsx_combined_parser(data_list):

    sheet_data = []
    sheet_names = ["payments", "overpayments", "home_improvements"]

    date = str(datetime.now().isoformat())

    writer = pd.ExcelWriter(f"User_Totals-{date[0:10]}.xlsx", engine="openpyxl")

    # data_dict is unordered, xlsx_complex_parser returns data ordered by name
    for data_dict in data_list:
        list_sheet_data_by_name, _ = xlsx_complex_parser(data_dict)
        sheet_data.append(list_sheet_data_by_name)

    dfs = []

    for e, list_sheet_data_by_name in enumerate(sheet_data):
        for data in list_sheet_data_by_name:
            dfs.append(pd.DataFrame(data))

        multiple_dfs(dfs, sheet_names[e], 2, writer)
        dfs = []

    writer.save()

    return sheet_data
