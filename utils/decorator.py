def exception_decorator(func):
    def new_func(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            if 'errors' in e.message:
                return e.message['errors']
            if 'error' in e.message:
                return e.message['error']
    return new_func
