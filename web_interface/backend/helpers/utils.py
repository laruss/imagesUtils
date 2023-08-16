def make_response(status_code, message, data=None):
    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }
