import base64
import datetime
import io

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table
# from redpackage.azure.blob import Blob
# from redpackage.azure.database import  AzureSQL
from dash import html

from Components.components import button_send, alert_failed_tests, jobInput

file_name_brandon = 'EXCEL_DATA_BrandON_Budvar33_II_v01_1BUD0014I.xlsx'
path_brandon = 'C:\\Users\\kardasek1\\PycharmProjects\\AnalyticsProductProcessing\\data\\' + str(file_name_brandon)
df_brandon_input = pd.read_excel(path_brandon)
#print(df_brandon_input.columns)

path_verifier = 'C:\\Users\\kardasek1\\PycharmProjects\\AnalyticsProductProcessing\\data\\BrandOn_StarTrack_questionnaire_V03AM.xlsx'
df_verifier_input = pd.read_excel(path_verifier,sheet_name='columns_verify')
#df_verifier_input = df_verifier_input[df_verifier_input['allowed_columnNamesVariations'] == 'RESPID']
#print(df_verifier_input.columns)

df_verify_brandon = df_verifier_input[df_verifier_input['product']=='BrandON']
#df_verify_startrack = df_verifier_input[df_verifier_input['product']=='StarTrack']
#print(df_verify_brandon)

# Porovnání přítomnosti sloupců ze dvou dataframe, na výstupu dává název sloupce a stav (OK, ERROR)
def CompareColumns(input_df, root_df):
    input_columns = list(input_df.columns)
    root_columns = list(root_df['allowed_columnNamesVariations'])
    resulList = []
    outputDict = {}
    outputDict['outputState'] = None

    for x in root_columns:
        if x in input_columns:
            tempDict = {'Sloupec': x, 'Výsledek': 'OK - Povinný sloupec je v nahraném souboru'}
            resulList.append(tempDict)
        else:
            tempDict = {'Sloupec': x, 'Výsledek': 'ERROR - V nahraném souboru chybí tento sloupec'}
            resulList.append(tempDict)
            outputDict['outputState'] = False
    outputDict['outputData'] = resulList
    return outputDict

# Zhodnocení, zda jsou všechny sloupce přítomny
def CheckResult(input_df, root_df):
    input_columns = list(input_df.columns)
    root_columns = list(root_df['allowed_columnNamesVariations'])
    for x in root_columns:
        if x not in input_columns:
            return False
        else:
            return True


def TestFunction(contents, productType, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if productType == 'B':

            #input_columns = list(df.columns)
            #input_columns = ['Propíše se tento Brandon?']
            try:
                if 'csv' in filename:
                    # Assume that the user uploaded a CSV file
                    df = pd.read_csv(
                        io.StringIO(decoded.decode('utf-8')))
                elif 'xlsx' in filename:
                    # Assume that the user uploaded an excel file
                    df = pd.read_excel(io.BytesIO(decoded))
                    #df = pd.DataFrame(df)
                   # df = pd.read_excel(contents)

            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])

            # blok, který nám skryje nebo odhalí tlačítko pro nahrání do databáze
            try:
                getStatus = CompareColumns(df, df_verify_brandon)['outputState']
                if getStatus == False:
                    showButton = ''
                    showJobInput = ''
                    showErrorMessage = alert_failed_tests
                else:
                    showButton = button_send
                    showJobInput = jobInput
                    showErrorMessage = ''
            except Exception as e:
                print(e)
                return html.Div(['Nepovedlo se načíst status finálního testu: ' + str(e)])

            # blok, který nám dá výstupní tabulku testů s výsledky
            return html.Div([
                html.H5(filename),
                html.H6('Poslední editace souboru: ' + str(datetime.datetime.fromtimestamp(date))),
                html.Div(id='ResultsTable', children=dash_table.DataTable(
                    data=CompareColumns(df, df_verify_brandon)['outputData'], columns=[{"name": 'Sloupec', "id": 'Sloupec'}, {"name": 'Výsledek', "id": 'Výsledek'}]
                )),
                html.Hr(),  # horizontal line
                html.Hr(),  # horizontal line
                dbc.Row([
                    dbc.Col(html.Div(), width=4),
                    dbc.Col(html.Div(showJobInput), width=2),
                    dbc.Col(html.Div(showButton), width=4),
                    dbc.Col(html.Div(), width=2) #showErrorMessage
                ], className="g-0", align="center", justify="center"),
                html.Hr(),  # horizontal line
                dbc.Row([
                    dbc.Col(html.Div(showErrorMessage), width=12),
                ], className="g-0", align="center", justify="center"),
                html.Hr(),  # horizontal line
                html.Div(id='my-output', children='TEST'),

                # For debugging, display the raw contents provided by the web browser
                html.Div('Raw Content'),
                html.Pre(contents[0:200] + '...', style={
                    'whiteSpace': 'pre-wrap',
                    'wordBreak': 'break-all'
                })
            ])
        elif productType == 'S':
            # input_columns = list(contents.columns)
            input_columns = ['ANEBO tento Startrack?']

    except Exception as e:
        print(e)
        input_columns = ['Někde ve čtení souboru nastala chyba a chtělo by to asi opravit:   ' + str(e)]
    return input_columns

# def createFinalExport(): #content, jobNumber
#     # načíst df z dbo
#     # podívej se, jestli daný JOB už není v dbo uložený
#         # pokud ano, tak záznamy jobu smaž
#     # appenduj input k dbo dataframe a nahraj do dbo
#     return alert_success_upload
#
# def read_dbo():
#     planning = create_db_connection('Planning')
#     params = urllib.parse.quote_plus(planning.params)
#     engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
#     return True
#
# def create_db_connection(db):
#     con = AzureSQL(db)
#
#     return con
#
# def get_all_projects(productType):
#     azure_sql = AzureSQL(database='Products')
#     with azure_sql.cursor() as cursor:
#         conn = azure_sql.connection
#
#         if productType == 'B':
#             sql = f"SELECT * FROM [brandon].[ValidatedOutputs]"
#         elif productType == 'S':
#             #sql = f"SELECT * FROM [brandon].[ValidatedOutputs]"
#             sql = ''
#         else:
#             raise ValueError("Product does not exist")
#         df = pd.read_sql(sql, conn)
#
# get_all_projects('B')