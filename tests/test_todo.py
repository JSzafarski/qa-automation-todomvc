import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# initialize and quit the WebDriver
@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")  # Run browser in the background (i.e headless)
    driver = webdriver.Chrome(options=options)
    yield driver  # Provide the driver to the test function
    driver.quit()  # Ensure the WebDriver is properly closed after tests are done

# Test to add a new item
def test_add_todo(driver):
    # Open the TodoMVC React app
    driver.get("https://todomvc.com/examples/react/dist/#/")  # URL of the demo app

    # Wait for the input box to be present before interacting with it
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "new-todo"))
    )

    input_box.send_keys("Buy milk\n")

    items = driver.find_elements(By.CSS_SELECTOR, ".todo-list li")

    # Assert that at least one item exists and it matches the expected text
    assert len(items) > 0 and items[0].text == "Buy milk"

