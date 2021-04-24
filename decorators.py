from functools import wraps


# 2.1
def greetings(name_surname):
    @wraps(name_surname)
    def format_string(*args):
        formatted_string = ""
        for word in name_surname(*args).split(" "):
            word = word[0].upper() + word[1:].lower() + " "
            formatted_string += word
        return "Hello " + formatted_string[:-1]  # without last space

    return format_string


@greetings
def name_surname():
    return "jan nowak"


# 2.2
def is_palindrome(sentence):
    @wraps(sentence)
    def inner(*args):
        string = sentence(*args)
        string2check = "".join(filter(str.isalnum, string)).lower()  # only alfanumeric symbols count
        if string2check == string2check[::-1]:
            return string + " - is palindrome"
        else:
            return string + " - is not palindrome"

    return inner


@is_palindrome
def sentence():
    return "Łapał za kran, a kanarka złapał."


# 2.3
def format_output(*decorator_args):
    def real_format_output(callable):
        @wraps(callable)
        def inner(*args):
            dict = callable(*args)
            # when decorator has arguments that are not returned by function - exception
            return_dict = {}
            for args in decorator_args:
                return_dict[args] = ""
                args_splitted = args.split("__")
                for arg in args_splitted:
                    if arg not in dict.keys():
                        raise ValueError
                return_dict[args] = " ".join([dict[arg] for arg in args_splitted])
            return return_dict

        return inner

    return real_format_output


@format_output("first_name__last_name", "city")
def first_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }


@format_output("first_name", "age")
def second_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }


# 2.4


class A:
    pass


def add_class_method(A):
    def decorator(foo):
        @wraps(foo)
        def inner(*args):
            return foo(*args)

        setattr(A, foo.__name__, inner)
        return inner

    return decorator


@add_class_method(A)
def foo():
    return "Hello!"


def add_instance_method(A):
    def decorator(bar):
        @wraps(bar)
        def inner(self):
            return bar()

        setattr(A, bar.__name__, inner)
        return bar

    return decorator


@add_instance_method(A)
def bar():
    return "Hello again!"


if __name__ == '__main__':
    print(A.foo())
    print(A().bar())
    print(first_func())
    print(second_func())
    print(name_surname())
    print(sentence())
