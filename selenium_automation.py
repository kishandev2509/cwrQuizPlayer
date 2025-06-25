import json
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def initialize_driver():
    """
    Initializes and returns a Selenium WebDriver.
    Requires the appropriate WebDriver executable (e.g., chromedriver.exe)
    to be in your system's PATH or specified directly.
    """
    try:
        # Configure Chrome options (headless for background execution, if desired)
        chrome_options = ChromeOptions()
        # Uncomment the line below to run in headless mode (without opening a browser window)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")  # Suppress logs
        chrome_options.add_argument("--disable-software-rasterizer")

        # Path to your chromedriver.exe (if not in PATH)
        # service = ChromeService(executable_path="path/to/your/chromedriver.exe")
        # For simplicity, assuming chromedriver is in PATH or automatically found
        driver = webdriver.Chrome(options=chrome_options)
        print("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        print("Please ensure you have the correct WebDriver installed and in your system's PATH,")
        print("or specify its path in the script (e.g., ChromeService(executable_path='path/to/driver')).")
        return None


def read_credentials(filepath="credentials.json"):
    """
    Reads username and password from a JSON file.
    """
    try:
        with open(filepath, "r") as f:
            credentials = json.load(f)
            return credentials.get("username"), credentials.get("password")
    except FileNotFoundError:
        print(f"Credentials file not found at {filepath}.")
        return None, None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filepath}. Ensure it's valid JSON.")
        return None, None


def login(driver: WebDriver, url, username, password):
    """
    Navigates to the login page and attempts to log in.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL of the login page.
        username (str): The user's username.
        password (str): The user's password.
    Returns:
        bool: True if login appears successful, False otherwise.
    """
    print(f"Navigating to login page: {url}")
    if driver.current_url != url:
        driver.get(url)

    try:
        # yesIn_button = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, "//*[@id=\"onesignal-slidedown-allow-button\"]")
        #     )
        # )
        # if yesIn_button.is_displayed:
        #     yesIn_button.click()

        username_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "email")))
        password_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
        signIn_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/div[2]/div/form/div/button"))
        )

        print("Entering credentials...")
        username_field.send_keys(username)
        password_field.send_keys(password)
        signIn_button.click()

        # Wait for navigation to complete or a specific element on the post-login page
        # Adjust the URL or element to wait for based on the website's behavior after login
        WebDriverWait(driver, 20).until(EC.url_to_be("https://codiny.codewithrandom.com/leaderboard"))

        print("Login button clicked. Waiting for page to load...")
        time.sleep(5)  # Give some time for client-side rendering/redirects

        try:
            tryAgain_button = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/div[5]/div/button")
                )
            )

            if tryAgain_button.is_displayed():
                raise Exception("Invalid Credentials")

        except TimeoutException:
            table_head = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/div[5]/div/table/thead/tr")
                )
            )

            if table_head:
                print("'Logged in Succesfully.")
                return True

    except Exception as e:
        print(f"Error during login: {e}")
        return False


def get_question(driver: WebDriver):
    try:
        nextBattleButton = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/main/div[2]/div[3]/div/button[2]"))
        )
        nextBattleButton.click()
    except TimeoutException:
        pass
    try:
        question = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/main/div[2]/div[3]/div/div[2]/div[2]/p"))
        )
        option0 = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div[1]/main/div[2]/div[3]/div/div[2]/div[3]/button[1]/div/span/p")
            )
        )
        option1 = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div[1]/main/div[2]/div[3]/div/div[2]/div[3]/button[2]/div/span/p")
            )
        )
        option2 = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div[1]/main/div[2]/div[3]/div/div[2]/div[3]/button[3]/div/span/p")
            )
        )
        option3 = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div[1]/main/div[2]/div[3]/div/div[2]/div[3]/button[4]/div/span/p")
            )
        )
        questionOptions = {
            "question": question,
            "option0": option0,
            "option1": option1,
            "option2": option2,
            "option3": option3,
        }
        return questionOptions
    except Exception as e:
        print(f"Timed out waiting for questions to load: {e}")
        print("The page might be empty or the locator needs adjustment.")
        return {
            "question": "default",
            "option0": 1,
            "option1": 2,
            "option2": 3,
            "option3": 4,
        }


def answer_questions(driver: WebDriver, questions_url, login_url, questionsAndAnswers):
    """
    Navigates to the questions page and returns its HTML content.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        questions_url (str): The URL of the page containing the questions.
    Returns:
        str: The HTML content of the questions page.
    """
    print(f"Navigating to questions page: {questions_url}")
    if driver.current_url != questions_url:
        driver.get(questions_url)
        time.sleep(5)
        try:
            if driver.current_url != questions_url:
                username, password = read_credentials()
                logged_in = login(driver, login_url, username, password)
                if not logged_in:
                    raise Exception("Login failed.")
        except Exception as e:
            print(f"Error: {e}")
            return ""
    driver.get(questions_url)
    for _ in range(10):
        try:
            adButton = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "fc-list-item-button"))
            )
            adButton.click()
            time.sleep(35)
            closeBtn = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.ID,"close-button")))
            closeBtn.click()
        except TimeoutException:
            pass
        quesOp = get_question(driver)
        if any([isinstance(element, str) for element in quesOp.values()]):
            try:
                emptyBtn = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/main/div[2]/div[3]/div/div[2]/div[3]/button[3]")))
                emptyBtn.click()
            except TimeoutException:
                pass
            continue
        print(*[element.text for element in quesOp.values()], sep="\n")
        question = quesOp["question"].text
        if question not in questionsAndAnswers:
            answer = input("answer the question:\t")
            qWithA = {
                "options": {
                    1: quesOp["option0"].text,
                    2: quesOp["option1"].text,
                    3: quesOp["option2"].text,
                    4: quesOp["option3"].text,
                },
                "answer": answer,
            }
            questionsAndAnswers[question] = qWithA
            save_data_to_json(questionsAndAnswers)

        answer = int(questionsAndAnswers[question]["answer"])
        print(answer)
        match answer:
            case 1:
                quesOp["option0"].click()
            case 2:
                quesOp["option1"].click()
            case 3:
                quesOp["option2"].click()
            case 4:
                quesOp["option3"].click()
            case _:
                pass
    print("All questions answered.")


def save_data_to_json(data, filename="scraped_questions_and_answers.json"):
    """
    Saves extracted data to a JSON file.
    Args:
        data (list or dict): The data to save.
        filename (str): The name of the JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")


def start():
    LOGIN_URL = "https://codiny.codewithrandom.com/login"
    QUESTIONS_URL = "https://codiny.codewithrandom.com/battle"

    questionsAndAnswers = {}

    try:
        with open("scraped_questions_and_answers.json", "r", encoding="utf-8") as file:
            questionsAndAnswers = json.load(file)
        print("JSON loaded successfully.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

    driver: WebDriver | None = None
    try:
        driver = initialize_driver()
        if driver:
            while True:
                try:
                    answer_questions(driver, QUESTIONS_URL, LOGIN_URL, questionsAndAnswers)
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    start()