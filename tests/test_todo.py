import pytest
from selenium import webdriver
from db import initialise_database, log_result
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module", autouse=True) #autouse = true - automatically run even though it’s not passed
def prepare_db():
    initialise_database()

# initialize and quit the WebDriver
@pytest.fixture(scope="module") #run for th whole module and not for every single test
def driver():
    options = Options()
    options.add_argument("--headless")  # Run browser in the background (i.e headless)
    driver = webdriver.Chrome(options=options)
    yield driver  # Provide the driver to the test function
    driver.quit()  # Ensure the WebDriver is properly closed after tests are done

# Test to add a new item
def test_add_todo(driver):
    """
        Test that a new 'to-do' item

        Step-by-step approach:
        - Open the TodoMVC React app
        - Locate the input field
        - Enter a to-do item and submit
        - Verify that the item appears in the list
        - Log the result to the SQLite database
    """
    outcome = "failed"
    input_item = "get hired"
    try:
        # Open the TodoMVC React app - URL of the demo app I am targeting to test
        driver.get("https://todomvc.com/examples/react/dist/#/")
        # Wait for the input box to be present before interacting with it (can prevent a false negative fail)
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "new-todo"))
            #we are locating the element by looking at the class names
        )
        input_box.send_keys(input_item+"\n") #automatically input the data by simulating key presses
        items = driver.find_elements(By.CSS_SELECTOR, ".todo-list li")
        # Assert that at least one item exists and it matches the initial input
        assert len(items) > 0 and items[0].text == input_item
        # correct assertion will trigger the outcome to be 'passed'
        outcome = 'passed'
    finally:
        # a broad try ... finally block is used that we get a graceful closure of the browser even if the test fails
        log_result(input_item, outcome)
