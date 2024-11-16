from datetime import datetime

from config.secrets import vbs_start_date, vbs_end_date

def validate_if_date_one_week() -> bool:
    pass

def validate_if_date_before(date_str: str) -> bool:
    date_obj = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S %p').date()

    if (date_obj < datetime.strptime(vbs_start_date, '%m-%d-%y').date()):
        print(date_obj, vbs_start_date)
        return True
    return False

def validate_if_date_after(date_str: str) -> bool:
    date_obj = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S %p').date()

    if (date_obj > datetime.strptime(vbs_end_date, '%m-%d-%y').date()):
        return True
    return False

def validate_data_status(status: str) -> bool:
    if status == 'AG':
        return True
    return False

def is_released(status: list) -> bool:
    if 'Released' in status:
        return True
    return False

def is_transferred(status: list) -> bool:
    if 'Transferred' in status:
        return True
    return False

def is_approved(status: list) -> bool:
    if 'Approved' in status or 'Approved-Inspected' in status:
        return True
    return False