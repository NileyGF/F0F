

class Mfun:
    def __init__(self,function:function):
        self.fun = function

    def __call__(self,x, *args, **kwds):
        return self.fun(x)

# class Point:
#     def __init__(self,X,Y):
#         pass

