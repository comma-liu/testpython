
from functools import wraps

def logging(file_name = "out.log"):
  def my_decorator(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        print(func.__name__ + " is called.")
        with open(file_name, 'a') as f:
            f.write(func.__name__ + "!\n")
        return func(*args, **kwargs)
    return wrap_func
  return my_decorator

@logging("out1.log")
def a_func(x, y, z):
    #print(f"I am the a_func {x+y+z}.")
    return f"I am the a_func {x+y+z}."
    
print(a_func(2, 1, 2))
