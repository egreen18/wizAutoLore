from datetime import datetime
count = 1
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("{} runs completed at {}".format(str(count), str(current_time)))