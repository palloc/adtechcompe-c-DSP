def predict_CTR(response_list):
    return 100

def percent(response_list):
    return 90

def bid(response_list):
    return predict_CTR(response_list) * percent(response_list)
