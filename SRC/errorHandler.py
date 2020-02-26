import traceback


def error_handler(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
            return {
                "error": str(e)
            }, 404
    return wrapper