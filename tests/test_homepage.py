from pages.homepage import HomePageActions
import pytest

data = [
    ("home", "Automation"),
    ("products", "Products"),
    ("cart", "Checkout"),
    ("signup", "Signup / Login"),
    ("testcases", "Test"),
    ("api", "API"),
    ("contactus", "Contact")
]

@pytest.mark.parametrize("page_name, expected_substring_title", data)
def test_page_title(browser, page_name, expected_substring_title):
    hompage = HomePageActions(browser)
    title = getattr(hompage, f"get_{page_name}_page_title")()
    assert expected_substring_title in title