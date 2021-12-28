import datetime

now = datetime.datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print("Current Date =", datetime.date.today())