#!/usr/bin/env python
#coding:utf-8
import xlsxwriter
workbook = xlsxwriter.Workbook('chart.csv')
#workbook = xlsxwriter.Workbook('chart.xlsx')
worksheet = workbook.add_worksheet()
# Create a new Chart object.
chart = workbook.add_chart({'type': 'line'})

# Write some data to add to plot on the chart.
data = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
]

worksheet.write_column('A1', data[0])
worksheet.write_column('B1', data[1])
worksheet.write_column('C1', data[2])
worksheet.write_column('D2',(1,3,5,7,9))
for i in range(5):
    worksheet.set_row(i,30)

# Configure the chart. In simplest case we add one or more data series.
chart.add_series({'values': '=Sheet1!$A$1:$A$5'})
chart.add_series({'values': '=Sheet1!$B$1:$B$5'})
chart.add_series({'values': '=Sheet1!$C$1:$C$5'})

# Insert the chart into the worksheet.
#worksheet.insert_chart('E1', chart)

workbook.close()
