from datetime import datetime, timedelta
import json


def get_dates_last_n_days(n: int):
    """
    Use this function to get start date and end date given the last N days.
    
    Args:
        n: Number of days ago from today. Required
        
    Return: 
        str: JSON with start_date and end_date range.
    """
    start_date = datetime.now() - timedelta(days=int(n))
    end_date = datetime.now()
    return json.dumps({
        "start_date": start_date.strftime("%d-%m-%Y %H:%M:%S"),
        "end_date": end_date.strftime("%d-%m-%Y %H:%M:%S")
    })

def get_dates_last_n_hours(n: int):
    """
    Use this function to get start date and end date given the last N hours.
    
    Args:
        n: Number of hours that have passed from now. Required
        
    Return: 
        str: JSON with start_date and end_date range.
    """
    start_date = datetime.now() - timedelta(hours=int(n))
    end_date = datetime.now()
    return json.dumps({
        "start_date": start_date.strftime("%d-%m-%Y %H:%M:%S"),
        "end_date": end_date.strftime("%d-%m-%Y %H:%M:%S")
    })


def get_dates_from_to(start_date, end_date):
    """
    Use this function to get start date and end date as datetime objects given string start date and end date.
    
    Args:
        start_date: Start date as a string in "DD-MM-YYYY" format. Required
        end_date: Start date as a string in "DD-MM-YYYY" format. Required
        
    Return: 
        str: JSON with start_date and end_date range.
    """
    s_date = datetime.strptime(start_date, "%d-%m-%Y")
    e_date = datetime.strptime(end_date, "%d-%m-%Y")
    return  json.dumps({
        "start_date": s_date.strftime("%d-%m-%Y %H:%M:%S"),
        "end_date": e_date.strftime("%d-%m-%Y %H:%M:%S")
    })
