from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import win32com.client as win32
import pickle
import os

URL = r"https://gaps.heig-vd.ch/consultation/controlescontinus/consultation.php"
USERNAME = "andremig.serzedel"
PASSWORD = "SalamiPicant3?"

SAVE_PATH = os.path.join(os.path.dirname(__file__), r"grades.p")


def get_element(driver: webdriver.Chrome, by: By, element_name: str) -> WebElement:
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, element_name))
        )
        return element
    except:
        driver.quit()
        raise Exception("Couldn't get element")


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )
    return driver


def open_url(driver: webdriver.Chrome, url: str) -> None:
    driver.get(url)


def login(driver: webdriver.Chrome, username: str, password: str) -> None:
    login_input = get_element(driver, By.NAME, "login")
    login_input.send_keys(username)

    password_input = get_element(driver, By.NAME, "password")
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)
    return True


def get_grades(driver: webdriver.Chrome) -> dict:
    full_array = get_element(driver, By.CLASS_NAME, "displayArray")

    module_header_elements = driver.find_elements(By.CLASS_NAME, "bigheader")

    module_header = set()
    for header in module_header_elements:
        module_header.add(header.text)

    lines = full_array.text.split("\n")
    results = {}
    module = ""
    for i in range(len(lines)):
        line = lines[i]
        is_header = line in module_header
        is_grade = "%" in line

        if is_grade:
            grade_name = lines[i - 1]
            results[module + " " + grade_name] = line.split(" ")[-1]
        if is_header:
            module = line.split(" ")[0]

    return results


def create_message_text(grades: set) -> str:
    notification_text = "Nouvelle(s) note(s) reçue(s):\n"
    for grade in sorted(grades):
        try:
            float(grade[1])
            notification_text += f"{grade[0]}: {grade[1]}\n"
        except ValueError:
            pass
    notification_text += "\nMessage Envoyé automatiquement"
    return notification_text


def terminal_notification(new_grades: set) -> None:
    if not new_grades:
        print("Nothing new")
        return

    print("New Grades:")
    for grade in new_grades:
        print(grade)


def email_notification(new_grades: set) -> None:
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = USERNAME + "@heig-vd.ch"
    mail.Subject = "Nouvelle note reçue"
    mail.Body = create_message_text(new_grades)
    mail.Send()


def notify(new_grades: set) -> None:
    terminal_notification(new_grades)


def save_dic(grades: set) -> None:
    pickle.dump(grades, open(SAVE_PATH, "wb"))


def main():
    try:
        old_dic = pickle.load(open(SAVE_PATH, "rb"))
    except:
        old_dic = {}

    driver = create_driver()
    open_url(driver, URL)
    login(driver, USERNAME, PASSWORD)
    dic = get_grades(driver)
    driver.quit()
    curr_set = set(dic.items())
    old_set = set(old_dic.items())
    dif_set = curr_set ^ old_set
    notify(dif_set)
    old_dic = dic
    save_dic(old_dic)


if __name__ == "__main__":
    main()
