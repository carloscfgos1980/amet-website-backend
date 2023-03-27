import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data.db", echo=True)

# SQL command to retrieve data
comm1 = "SELECT * FROM paintings"
comm2 = "SELECT * FROM customers"
comm3 = "SELECT * FROM fans"

# Read data from SQL using pandas
df1 = pd.read_sql_query(comm1, con=engine)
df2 = pd.read_sql_query(comm2, con=engine)
df3 = pd.read_sql_query(comm3, con=engine)

# Export data to excel
with pd.ExcelWriter('Amet_data1.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Paintings')
    df2.to_excel(writer, sheet_name='Customers')
    df3.to_excel(writer, sheet_name='Fans')
