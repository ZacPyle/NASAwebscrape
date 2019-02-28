import xlsxwriter
import datetime

# Save the date so you can know the last time it was updated
date = str(datetime.date.today())

print(date)

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('NASA_Small_Business.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'This sheet is up to date as of: ')
worksheet.write(0, 1, date)

'''

# Start from the first cell. Rows and columns are zero indexed.
row = 3
col = 0

# Iterate over the data and write it out row by row.
for item, cost, thing in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    worksheet.write(row, col + 2, thing)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')


'''
workbook.close()
