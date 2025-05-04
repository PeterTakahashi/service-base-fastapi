from app.lib.camel_to_snake import camel_to_snake


def test_camel_to_snake():
    assert camel_to_snake("CamelCase") == "camel_case"
    assert camel_to_snake("CamelCaseTest") == "camel_case_test"
    assert camel_to_snake("CamelCaseTest123") == "camel_case_test123"
    assert camel_to_snake("CamelCaseTest123ABC") == "camel_case_test123_abc"
