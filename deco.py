
def deco(func):
    a=1
    def wrapper():
        print(a)
        func(*arg)
        print('end')
    return wrapper

@deco
def foo(x,y):
    print('hello foo',x+y)

# foo=deco(foo)
foo(3,4)