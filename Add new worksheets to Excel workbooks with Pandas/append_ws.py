import pandas as pd
import openpyxl as pxl

# DataFrame to be inserted in the first worksheet
firstMockData = {
    'a': [1,2],
    'b': [3,4]
}
firstMockDF = pd.DataFrame(firstMockData)

# Name of the workbook we'll be using
filename = 'test_wb.xlsx'

# This creates a new workbook, which will contain only one sheet: sheetA
firstMockDF.to_excel(filename, 'sheetA', index=False)
# This recreates the workbook test_wb, again with a single sheet: sheetB
# firstMockDF.to_excel(filename, 'sheetB')

# --------------------------------------------------------

# Properly load the workbook
excel_book = pxl.load_workbook(filename)

# Inside this context manager, handle everything related to writing new data to the file\
# without overwriting existing data
with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    # Your loaded workbook is set as the "base of work"
    writer.book = excel_book

    # Loop through the existing worksheets in the workbook and map each title to\
    # the corresponding worksheet (that is, a dictionary where the keys are the\
    # existing worksheets' names and the values are the actual worksheets)
    writer.sheets = {worksheet.title: worksheet for worksheet in excel_book.worksheets}

    secondMockData = {
        'c': [10,20],
        'd': [30,40]
    }
    # This is the new data to be written to the workbook
    secondMockDF = pd.DataFrame(secondMockData)

    # Write the new data to the file without overwriting what already exists
    secondMockDF.to_excel(writer, 'sheetB', index=False)

    # Save the file
    writer.save()