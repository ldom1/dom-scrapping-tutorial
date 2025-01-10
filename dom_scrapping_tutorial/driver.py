import selenium.webdriver
from faker import Faker
from selenium.webdriver.chrome.service import Service

from dom_scrapping_tutorial import config, constant


def get_local_web_driver():
    """
    Initialize a local Chrome driver using Docker.

    :return: selenium.webdriver.Chrome
    """
    chrome_options = selenium.webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")

    # Add a random user agent
    user_agent = Faker().user_agent()
    chrome_options.add_argument(f"user-agent={user_agent}")

    try:
        driver = selenium.webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=chrome_options,
        )
    except Exception as e:
        config.logger.error(f"Failed to initialize the Chrome driver: {e}")
        driver = None
    return driver


def get_remote_web_driver():
    """
    Initialize a Chrome driver for remote.

    :return: selenium.webdriver.Chrome
    """
    chrome_options = selenium.webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")

    # Add a random user agent
    user_agent = Faker().user_agent()
    chrome_options.add_argument(f"user-agent={user_agent}")

    try:
        service = Service(executable_path="/opt/chromedriver")
        driver = selenium.webdriver.Chrome(
            service=service,
            options=chrome_options,
        )
    except Exception as e:
        config.logger.error(f"Failed to initialize the Chrome driver: {e}")
        driver = None
    return driver


def get_web_driver() -> selenium.webdriver.Chrome:
    """
    Initialize a Chrome driver based on the environment (local or AWS Lambda)

    :return: selenium.webdriver.Chrome
    """
    if config.RUN_ENV == constant.RUN_ENV_LOCAL:
        config.logger.info("Running locally - using local Chrome driver")
        driver = get_local_web_driver()
    elif config.RUN_ENV == constant.RUN_ENV_REMOTE:
        config.logger.info("Running remotely - using Remote Chrome driver")
        driver = get_remote_web_driver()
    else:
        config.logger.error("Invalid job type")
        raise ValueError("Invalid job type")

    if driver is None:
        raise ValueError(
            f"""Failed to initialize the Chrome driver (run env:
            {config.RUN_ENV})..."""
        )
    return driver
