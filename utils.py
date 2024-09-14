# utils.py

from datetime import datetime


def calculate_total_hours(start_time, finish_time):
    total_seconds = (datetime.combine(datetime.min, finish_time) - datetime.combine(datetime.min, start_time)).seconds
    return total_seconds / 3600.0

def calculate_total_mileage(start_mileage, end_mileage):
    return end_mileage - start_mileage
