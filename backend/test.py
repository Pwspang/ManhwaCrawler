
def log(func):
    def wrapper(*args, **kwargs):
        print(args)
        result = func(*args, **kwargs)
        print(result)
        return result
    return wrapper

@log
def add(a, b):
    return a+b 

add(1, 2)