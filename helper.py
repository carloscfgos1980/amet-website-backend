import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("sqlite:///instance/amet.db", echo=True)

df = pd.read_excel('Amet_data.xlsx')
print(df)


wb = pd.ExcelFile('Amet_data.xlsx')
for sheet in wb.sheet_names:
    df = pd.read_excel('Amet_data.xlsx', sheet_name=sheet)
    df.to_sql(sheet, con=engine, index=False, if_exists="append")
