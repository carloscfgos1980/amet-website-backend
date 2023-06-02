# App.py
* I must create an id variable for the table when I am creating the database but I must delete later when I do the POST and PATCH

# helper.py 
* I use it to populate the database

* I must check what is wrong when I print the excel. I got an extra column on the left with the index number

* Solved the problem of the extra index:

    df1.to_excel(writer, index=False, sheet_name='paintingsData')
    df2.to_excel(writer, index=False, sheet_name='customers')
    df3.to_excel(writer, index=False, sheet_name='fans')

* I need to git a nice format to the excel file and send automatically email