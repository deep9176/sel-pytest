import os
import pytest
import logging
import datetime
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

def pytest_configure(config):
    log_level = config.getoption("--loglevel").upper()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"Logs/test_log_{timestamp}.html"

    logging.basicConfig(filename=log_file, 
                        level=getattr(logging, log_level, logging.INFO), 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    if not os.path.exists('Logs'):
        os.makedirs('Logs')
       

    config.option.htmlpath = log_file
    config.option.self_contained_html = True

    for noisy_logger in ['selenium', 'urllib3', 'WDM']:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    
    config.option.log_cli_level = log_level
    config.option.log_file_level = log_level
    config.option.show_capture = 'log'
    if config.getoption("--help-options"):
        print("""
        Available command-line options:
        
        --headless: Run tests in headless mode(without opening a browser window).
        --loglevel=<level>L Set log level (options: DEBUG, INFO, WARNING).
        --repeat=<n>: Repeat the tests n times.
        --reruns=<n>: Rerun failed tests n times.
        --xdist=<n>: Run tests in parallel with n workers.
        
        Example usage: pytest --headless --logllevel=debug --repeat=5 --reruns=3 --xdist=4
        """)
        pytest.exit("Exiting after displaying available options")


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help = "Run Tests in headless mode")
    parser.addoption("--loglevel", action="store", default="INFO", help = "Enable DEBUG mode")
    parser.addoption("--repeat", action="store", default=1, type=int, help = "Repeat tests n times")
    parser.addoption("--xdist", action="store", default=1, type=int, help = "Run tests in parallel with n workers")
    parser.addoption("--help-options", action="store_true", help = "Show all available options")

def initialize_chrome(headless=False):
    options = ChromeOptions()
    logging.debug("Checking if tests needs to be run in headless mode...")
    if headless:
        logging.debug("Enabling headless mode")
        options.add_argument("--headless")
    else:
        logging.debug("Headless mode not enabled")
    logging.debug("Maximizing the browser window")
    options.add_argument("--start-maximized")
    
    driver = ChromeDriverManager(driver_version="138.0.7204.183").install()
    service = ChromeService(driver)

    return webdriver.Chrome(service=service, options=options)

@pytest.fixture(scope="module")
def browser(request):
    headless = request.config.getoption("headless")
    logging.debug("Initiazing chrome driver")
    driver = initialize_chrome(headless)

    try:
        logging.info("Navingating to Automation Exercise website")
        driver.get("https://automationexercise.com/")
        homepage_title = driver.title

        if 'Automation' in homepage_title:
            logging.info(f"Home page loaded successfully with title: {homepage_title}")
        else:
            logging.error(f"Failed to load homepage, Title found: {homepage_title}")

    except TimeoutException:
        logging.error("Timed out while trying to load homepage")

    except Exception as e:
        logging.error(f"An error occured while loading the page: {e}")

    yield driver
    driver.quit()