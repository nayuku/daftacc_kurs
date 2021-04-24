import unittest

from decorators import greetings, is_palindrome, format_output, add_class_method, add_instance_method


class ExampleClass:
    pass


@add_class_method(ExampleClass)
def cls_method():
    return "Hello!"


@add_instance_method(ExampleClass)
def inst_method():
    return "Hello!"


class ExampleTest(unittest.TestCase):
    @greetings
    def show_greetings(self):
        return "joe doe"

    @is_palindrome
    def show_sentence(self):
        return "annA"

    @format_output("first_name")
    def show_dict(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
        }

    def test_greetings(self):
        self.assertEqual(self.show_greetings(), "Hello Joe Doe")

    def test_sentence(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")

    def test_dict(self):
        self.assertEqual(self.show_dict(), {"first_name": "Jan"})

    def test_class(self):
        self.assertEqual(ExampleClass.cls_method(), cls_method())
        self.assertEqual(ExampleClass().inst_method(), inst_method())


if __name__ == "__main__":
    unittest.main()
