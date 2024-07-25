import datetime
from database import update_competition

def process_qr_code(qr_data, start_time):
    try:
        cpf, competition = qr_data.split('/')
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        final_time = getTimeDiff(start_time, datetime.datetime.strptime(current_time, "%H:%M:%S").time())
        print("current_time:", current_time)
        print("Final time:", final_time)
        update_competition(cpf, competition, final_time)
    except ValueError:
        print("Error processing QR code: invalid format")

def getTimeDiff(time1, time2):
    if isinstance(time1, datetime.time):
        time1 = datetime.datetime.combine(datetime.date.today(), time1)
    if isinstance(time2, datetime.time):
        time2 = datetime.datetime.combine(datetime.date.today(), time2)
    diff = time2 - time1
    return str(diff)
