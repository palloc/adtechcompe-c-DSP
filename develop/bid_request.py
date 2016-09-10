import datetime

def predict_CTR(response_list):
    return 100

def time_pass_percent():
    now_datetime = datetime.datetime.now()
    now = now_datetime.hour * 60 + now_datetime.minute

    start_date = now_datetime.replace(hour=1, minute=00)
    start = start_date.hour * 60 + start_date.minute

    end_date = now_datetime.replace(hour=23, minute=00)
    end = end_date.hour * 60 + end_date.minute

    time_remain_percent = float((now - end)) / (start - end)
    return time_remain_percent

def percent(response_list):
    return 90

def bid(response_list):
    return predict_CTR(response_list) * percent(response_list)
