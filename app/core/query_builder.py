from flask import abort


def query_extractor(query: str) -> list:
    return query.split(",")


def query_formatter(query_list: list, accepted_query: list) -> str:

    built_sub_query = ""

    for value in query_list:
        if value in accepted_query:
            if len(built_sub_query) != 0:
                built_sub_query += ","

            built_sub_query += f'"{value}"'

    if not built_sub_query:
        abort(400)

    return built_sub_query


def query_builder(
    table_query: str, state_query: str, less_than: bool, date: str, limit: str
):

    final_query = f"""SELECT * FROM logs WHERE table_name IN ({table_query}) AND state IN ({state_query}) """
    final_query = date_limit_builder(final_query, less_than, date, limit)

    return final_query


def date_limit_builder(query: str, less_than: bool, date: str, limit: str):

    if less_than:
        query += f'AND date <= "{date}" '
    else:
        query += f'AND date >= "{date}" '

    query += f"ORDER BY date DESC "

    query += f"LIMIT {limit}"

    return query
