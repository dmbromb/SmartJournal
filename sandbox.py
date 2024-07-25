import calendar

cal = calendar.Calendar()
dict = [day for day in (cal.itermonthdays(2023, 2))]
print(dict)