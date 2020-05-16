

# def doiteration(thing):
#     print("doiteration: " + str(thing))
#     print("is it a string?: " + str(isString(thing)))
#     if isString(thing):
#         thing = [ thing ]
#     for item in thing:
#         print("  item: " + item)

def doiteration(*thing):
    print("doiteration: " + str(thing))
    print("type of thing: " + str(type(thing)))
    print("is it a string?: " + str(isString(thing)))
    if isString(thing):
        thing = [ thing ]
    for item in thing:
        print("  item: " + str(item))



def iterable(obj):
    return isinstance(obj, Iterable)

def isString(obj):
    return isinstance(obj, str)


print("---------- 1")
doiteration("hello")
print("---------- 2")
doiteration(["hello", "world"])
print("---------- 3")
doiteration("hello", "world")


