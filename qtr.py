import duckdb
import pandas as pd


def query_to_result(query):
    res = duckdb.sql(query).fetchall()
    return res


# query = """SELECT "Product line", SUM("Total") AS total_sales FROM supermarket_sales.csv GROUP BY "Product line" ORDER BY total_sales DESC LIMIT 1;"""
# print(query_to_result(query))

