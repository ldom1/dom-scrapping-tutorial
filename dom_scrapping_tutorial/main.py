from mistralai import Mistral
from dom_scrapping_tutorial.driver import get_web_driver
from dom_scrapping_tutorial import config, constant
import bs4


def dom_scrapping(url: str):
    """
    Scrap the input url and summarize the content using Mistral AI

    :param url: The url to scrap
    :return: The summary of the content
    """
    # Initialize the web driver

    config.logger.info("Initializing the web driver...")
    web_driver = get_web_driver()

    web_driver.get(url)

    # Extract the content from the website
    config.logger.info("Extracting the content from the website...")

    html_data: bs4.BeautifulSoup = bs4.BeautifulSoup(
        web_driver.page_source, "html.parser"
    )
    website_content = html_data.find(
        "div", {"class": "mw-content-ltr mw-parser-output"}
    )

    # Summarize the content with Mistral AI
    client = Mistral(api_key=config.MISTRAL_API_KEY)

    config.logger.info("Summarizing the website content...")
    chat_response = client.chat.complete(
        model=constant.MISTRAL_AI_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following content: {website_content}",
            },
        ],
    )

    config.logger.info(f"Chat response: {chat_response}")

    # Close the web driver
    web_driver.quit()

    # Write the result to a text file
    return chat_response.choices[0].message.content
