from datetime import datetime


def class_to_dict(obj, depth=0):
    """
    Converts a class instance to a dictionary, formatting datetime objects as strings in "dd-mm-Y H:M:S" format.
    Recursively handles nested objects up to a specified depth.
    
    :param obj: The class instance to convert.
    :param depth: The maximum depth to recurse into nested objects.
    :return: A dictionary representation of the class instance.
    """
    result = {}
    if not obj or depth < 0:
        return None
    if hasattr(obj, '__dict__'):
        for attr_name, attr_value in vars(obj).items():
            if isinstance(attr_value, datetime):
                # Convert datetime object to string in "dd-mm-Y H:M:S" format
                attr_value = attr_value.strftime("%d-%m-%Y %H:%M:%S")
            elif isinstance(attr_value, list) and depth > 0:
                # Recursively convert list items
                attr_value = [class_to_dict(item, depth - 1) for item in attr_value]
            elif isinstance(attr_value, dict) and depth > 0:
                # Recursively convert dictionary items
                attr_value = class_to_dict(attr_value, depth - 1)
            result[attr_name] = attr_value
    return result

