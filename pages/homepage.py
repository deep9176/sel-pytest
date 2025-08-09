from selenium.webdriver.common.by import By


class HomePageLocators:
    locators = {
        "home" : (By.PARTIAL_LINK_TEXT, "Home"),
        "products" : (By.PARTIAL_LINK_TEXT, "Products"),
        "cart" : (By.PARTIAL_LINK_TEXT, "Cart"),
        "signup" : (By.PARTIAL_LINK_TEXT, "Signup"),
        "testcases" : (By.PARTIAL_LINK_TEXT, "Test"),
        "api" : (By.PARTIAL_LINK_TEXT, "API"),
        "contactus" : (By.PARTIAL_LINK_TEXT, "Contact")
    }


class HomePageActions:
    def __init__(self, driver):
        self.driver = driver

    def __click_button(self, button_name):
        locator = HomePageLocators.locators.get(button_name)
        if locator:
            self.driver.find_element(*locator).click()
        else:
            raise ValueError(f"No locator found for button: {button_name}")
    
    def _get_title(self, button_name):
        self.__click_button(button_name)
        return self.driver.title
    
    def get_home_page_title(self):
        return self._get_title("home")
    
    def get_products_page_title(self):
        return self._get_title("products")
    
    def get_cart_page_title(self):
        return self._get_title("cart")

    def get_signup_page_title(self):
        return self._get_title("signup")

    def get_testcases_page_title(self):
        return self._get_title("testcases")

    def get_api_page_title(self):
        return self._get_title("api")

    def get_contactus_page_title(self):
        return self._get_title("contactus")