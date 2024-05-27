from datetime import datetime

def change_date_time_format(date_str):
    date_obj = datetime.strptime(date_str, '%d-%b %Y %H:%M%p')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date
