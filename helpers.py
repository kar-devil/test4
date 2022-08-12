import base64
import datetime
import io
import urllib
import numpy as np
import pandas as pd
from dash import html
from redpackage.azure.database import AzureSQL
from sqlalchemy import create_engine
from unidecode import unidecode


def create_db_connection(db):
    con = AzureSQL(db)

    return con

def get_all_projects(productType):
    azure_sql = AzureSQL(database='Products')
    with azure_sql.cursor() as cursor:
        conn = azure_sql.connection

        if productType == 'B':
            sql = f"SELECT * FROM [brandon].[ValidatedOutputs]"
        elif productType == 'S':
            #sql = f"SELECT * FROM [brandon].[ValidatedOutputs]"
            sql = ''
        else:
            raise ValueError("Product does not exist")
        df = pd.read_sql(sql, conn)

    return df
def check_duplicates(productType, job):
    azure_sql = AzureSQL(database='Products')
    with azure_sql.cursor() as cursor:
        conn = azure_sql.connection

        if productType == 'B':
            sql = f"SELECT * FROM [brandon].[ValidatedOutputs] WHERE JobNumber = '{job}'"
        elif productType == 'S':
            #sql = f"SELECT * FROM [brandon].[ValidatedOutputs] WHERE JobNumber = '{job}'"
            sql = ''
        else:
            raise ValueError("Product does not exist")

        df = pd.read_sql(sql, conn)

        if df.empty:
            result = False
        else:
            result = True
    return result, df

def delete_product(productType, job):
    """
    delete from 7 tables that are filled with info about mediaplan
    and save a log about delete operation with timestamp when it happened
    """
    now = datetime.datetime.now()
    products = create_db_connection('Products')
    params = urllib.parse.quote_plus(products.params)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    with engine.begin() as conn:

        if productType == 'B':
            conn.execute(
            f"DELETE FROM [brandon].[ValidatedOutputs] WHERE WHERE JobNumber = '{job}''"
        )
        elif productType == 'S':
            pass
        else:
            raise ValueError("Product does not exist")




# check duplicit
    # ano - smaz a vloz # NE - vloz

def write_product(productType, job):
    productType = productType
    job = job

    if check_duplicates(productType, job) == True:
        # smazat
    elif check_duplicates(productType, job) == False:
        continue

    # zapis
    products = create_db_connection('Products')
    params = urllib.parse.quote_plus(products.params)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    with engine.begin() as conn:
        conn.execute(
            f"UPDATE tv.MediaplanLineValues SET [primary] = 0 WHERE campaignId = '{campaign_id}' AND monthNumber = {int(month_number)} AND plan_name = '{plan_name}'"
        )
        rows_affected = res.rowcount
        return rows_affected

#
# def update_primary_version(campaign_id, month_number, plan_name, version):
#     planning = create_db_connection('Planning')
#     params = urllib.parse.quote_plus(planning.params)
#     engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
#     with engine.begin() as conn:
#         conn.execute(
#             f"UPDATE tv.MediaplanLineValues SET [primary] = 0 WHERE campaignId = '{campaign_id}' AND monthNumber = {int(month_number)} AND plan_name = '{plan_name}'"
#         )
#
#         res = conn.execute(
#             f"""UPDATE tv.MediaplanLineValues SET [primary] = 1
#             WHERE campaignId = '{campaign_id}' AND monthNumber = {int(month_number)} AND plan_name = '{plan_name}' AND version = '{int(version)}'
#             """)
#         rows_affected = res.rowcount
#         return rows_affected

def insert_overdelivery_values(month_number, input_overdelivery, campaign_id, version, plan_name):
    planning = AzureSQL('Planning')
    with planning.cursor(commit=True) as cursor:
        conn = planning.connection
        for input_ in input_overdelivery:
            overdelivery_value = input_[1]
            if overdelivery_value is not None:
                overdelivery_value = float(overdelivery_value)
            else:
                overdelivery_value = 0
            group_id = int(input_[0]['index'])

            try:
                res = cursor.execute(
                    f"""UPDATE tv.Overdelivery SET [overdelivery] = {overdelivery_value}
                    WHERE campaignId = '{campaign_id}' AND monthNumber = {int(month_number)} AND groupId = {int(group_id)} 
                    AND [version] = {int(version)} AND [plan_name] = '{plan_name}'
                    """
                )
                rows_affected = res.rowcount
                if rows_affected == 0:
                    cursor.execute(
                        "insert into tv.Overdelivery(campaignId, monthNumber, version, groupId, overdelivery, plan_name) values (?, ?, ?, ?, ?, ?)",
                        campaign_id, int(month_number), int(version), int(group_id), overdelivery_value, plan_name)
                    conn.commit()
            except Exception as e:
                print(e)
                print('oou')
    print('uf')
    print('jaj')


# def delete_plan(campaign_id, client, job_number, month, plan_name):
#     """
#     delete from 7 tables that are filled with info about mediaplan
#     and save a log about delete operation with timestamp when it happened
#     """
#     now = datetime.datetime.now()
#     planning = create_db_connection('Planning')
#     params = urllib.parse.quote_plus(planning.params)
#     engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
#     with engine.begin() as conn:
#         conn.execute(
#             f"DELETE FROM tv.SpotInfo WHERE campaignId = '{campaign_id}' AND monthNumber = {int(month)} AND plan_name = '{plan_name}'"
#         )
#
