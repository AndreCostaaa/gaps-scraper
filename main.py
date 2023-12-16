from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pickle
import json
import os
import smtplib, ssl
from email.message import EmailMessage
from typing import Tuple, Union

AUTH_PATH = os.path.join(os.path.dirname(__file__), r"data/auth.json")
SMTP_AUTH_PATH = os.path.join(os.path.dirname(__file__), r"data/smtp_auth.json")

BASE_URL = r"https://gaps.heig-vd.ch/consultation/"
GRADES_URL = BASE_URL + r"controlescontinus/consultation.php"
REPORT_CARD_BASE_URL = BASE_URL + r"notes/bulletin.php?id="
STUDENT_DETAILS_URL = BASE_URL + r"etudiant"
SCHEDULE_URL = BASE_URL + r"horaires"


GRADES_SAVE_PATH = os.path.join(os.path.dirname(__file__), r"data/grades.p")
MODULES_SAVE_PATH = os.path.join(os.path.dirname(__file__), r"data/modules.p")
UNITS_SAVE_PATH = os.path.join(os.path.dirname(__file__), r"data/units.p")
EFFECTIFS_SAVE_PATH = os.path.join(os.path.dirname(__file__), r"data/effectifs.p")
NEXT_SCHEDULE_DATA_PATH = os.path.join(
    os.path.dirname(__file__), r"data/next_schedule.p"
)


def log(log_txt: str) -> None:
    """with open("logs", "w") as f:
    now = datetime.now()
    f.write("\n" + now.strftime("%d/%m/%Y %H:%M") + ": " + log_txt)
    """
    print(log_txt)


def get_login_data() -> Tuple[str, str]:
    auth = json.load(open(AUTH_PATH))
    return auth["username"], auth["password"]


def get_element(
    driver: webdriver.Chrome, by: By, element_name: str, wait_time=10
) -> WebElement:
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by, element_name))
        )
        return element
    except TimeoutException as e:
        print(e.msg)
    return None


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.BinaryLocation = "/usr/bin/chromium-browser"

    driver_path = "/usr/bin/chromedriver"
    service = Service(driver_path)
    driver = webdriver.Chrome(options=options, service=service)
    return driver


def open_url(driver: webdriver.Chrome, url: str) -> None:
    driver.get(url)


def skip_popup(driver):
    pop_up = get_element(driver, By.ID, "dialog-message", wait_time=2)

    if not pop_up:
        return
    pop_up.parent.find_element(By.TAG_NAME, "button").click()


def login(driver: webdriver.Chrome, username: str, password: str) -> bool:
    login_input = get_element(driver, By.NAME, "login")
    password_input = get_element(driver, By.NAME, "password")

    if not login_input or not password_input:
        return False

    login_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    skip_popup(driver)
    return True


def get_grades_array(driver: webdriver.Chrome) -> Union[str, set]:
    full_array = get_element(driver, By.CLASS_NAME, "displayArray")
    if not full_array:
        return (None, None)
    headers = driver.find_elements(By.CLASS_NAME, "bigheader")

    header_set = set()
    for header in headers:
        header_set.add(header.text)

    return (full_array.text, header_set)


def get_grades(full_array_str: str, module_headers: set) -> Union[dict, dict]:
    lines = full_array_str.split("\n")
    results = {}
    averages = {}
    module = ""
    for i, line in enumerate(lines):
        is_header = line in module_headers
        is_grade = "%" in line

        if is_grade:
            grade_name = lines[i - 1]
            splitted = line.split(" ")
            try:
                float(splitted[-1])
                results[module + " " + grade_name] = f"{splitted[-1]} ({splitted[0]})"
            except ValueError:
                pass

        if is_header:
            line_split = line.split(" ")
            module = line_split[0]
            averages[module] = line_split[-1]

    return results, averages


def go_to_report_card(driver: webdriver.Chrome) -> bool:
    if not get_element(driver, By.ID, "infoacademique"):
        return False
    page_html = driver.page_source
    url = REPORT_CARD_BASE_URL
    start_idx = page_html.find("DEFAULT_STUDENT_ID")
    end_idx = page_html.find(";", start_idx)
    id_definition_str = page_html[start_idx:end_idx]
    student_id = id_definition_str.split("= ")[-1]

    url += student_id

    open_url(driver, url)
    return True


def get_report_card(driver: webdriver.Chrome) -> Union[list, list]:
    record_table = get_element(driver, By.ID, "record_table")
    header_element = get_element(driver, By.CLASS_NAME, "bulletin_header_row")
    if not record_table or not header_element:
        return (None, None)
    modules_headers = []
    for col in header_element.find_elements(By.TAG_NAME, "td"):
        modules_headers.append(col.get_attribute("innerHTML").split(" ")[0])
    modules_headers.insert(1, "Description")
    unit_headers = ["Name", "Cours", "Laboratoire", "Projet", "Examen", "Moyenne"]
    modules = []
    units = []
    rows = record_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        is_module = "module" in row.get_attribute("class")
        is_unit = "unit" in row.get_attribute("class")
        module = {}
        unit = {}
        for i, col in enumerate(cols):
            if not col.get_attribute("class"):
                continue
            if is_module:
                text = col.text
                if modules_headers[i] == "Description":
                    text = text.split(" (")[0]
                module[modules_headers[i]] = text
            if is_unit:
                if i == 0:
                    unit["Name"] = col.text
                elif i == 1:
                    line_2 = col.text.split("\n")[1]
                    for sub_str in unit_headers[1:5]:
                        idx = line_2.find(sub_str)

                        if idx == -1:
                            unit[sub_str] = ""
                            continue
                        note_start_idx = line_2.find(":", idx) + 2
                        unit[sub_str] = line_2[
                            note_start_idx : line_2.find(" ", note_start_idx)
                        ]
                elif modules_headers[i] == "Note":
                    unit["Moy"] = col.text

        if is_module:
            modules.append(module)
        if is_unit:
            units.append(unit)

    return modules, units


def create_message_text(grades: set, averages: dict) -> str:
    notification_text = "Nouvelle(s) note(s) reçue(s):\n"
    for grade in sorted(grades):
        notification_text += f"{grade[0]}: {grade[1]}\n"

    notification_text += "\nMoyennes:\n"

    for key, val in averages.items():
        notification_text += f"{key}: {val}\n"
    notification_text += "\nMessage Envoyé automatiquement"
    return notification_text


def terminal_notification(text: str) -> None:
    print(text)


def email_notification(subject: str, message_content: str) -> None:
    smtp_auth_data = json.load(open(SMTP_AUTH_PATH))

    message = EmailMessage()
    username, _ = get_login_data()
    message["Subject"] = subject
    message["From"] = smtp_auth_data["email_address"]
    message["To"] = username + "@heig-vd.ch"
    message.set_content(message_content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        smtp_auth_data["smtp_server"],
        smtp_auth_data["smtp_server_port"],
        context=context,
    ) as server:
        server.login(smtp_auth_data["email_address"], smtp_auth_data["email_token"])
        server.send_message(message)


def create_report_card(modules: list[dict], units: list[dict]) -> str:
    text = "Modules:\n"
    for module in modules:
        text += f"{module['Module']} "
        if len(module["Module"]) < 4:
            text += " "
        if "Note" in module:
            text += f"{module['Note']} "
        if "Crédits" in module:
            credits = module["Crédits"]
            if not credits:
                credits = "X"
            text += f"ECTS: {credits} "

        text += f"({module['Description']}) "
        if "Situation" in module:
            text += f"{module['Situation']}"
        text += "\n"

    text += "\nUnités:\n"
    for unit in units:
        text += f"{unit['Name']} "
        if len(unit["Name"]) < 4:
            text += " "
        for key, val in unit.items():
            if key == "Name":
                continue
            grade = val
            while len(grade) < 3:
                grade += " "
            if "\n" in grade:
                grade = " ".join(grade.split("\n"))
            text += f"{key[0]} {grade} "
        text += "\n"
    return text


def send_report_card(modules: list[dict], units: list[dict]) -> None:
    report_card = create_report_card(modules, units)
    email_notification("Bulletin de notes", report_card)
    terminal_notification(report_card)


def notify(new_grades: set, averages: dict) -> None:
    if not new_grades:
        return

    message = create_message_text(new_grades, averages)
    email_notification("Nouvelle Note", message)
    terminal_notification(message)


def write_to_disk(object: set, path: str) -> None:
    pickle.dump(object, open(path, "wb"))


def get_differences(old_set: set, new_set: set) -> set:
    dif_set = new_set ^ old_set
    return {x for x in dif_set if x not in old_set}


def fetch_grades(driver: webdriver.Chrome) -> bool:
    try:
        old_grades = pickle.load(open(GRADES_SAVE_PATH, "rb"))
    except:
        old_grades = {}

    open_url(driver, GRADES_URL)
    username, password = get_login_data()

    if not login(driver, username, password):
        return False

    array, headers = get_grades_array(driver)

    if not array or not headers:
        return False

    grades, averages = get_grades(array, headers)

    dif_set = get_differences(set(old_grades.items()), set(grades.items()))

    notify(dif_set, averages)

    write_to_disk(grades, GRADES_SAVE_PATH)
    return True


def handle_report_card(driver: webdriver.Chrome) -> bool:
    try:
        old_modules = pickle.load(open(MODULES_SAVE_PATH, "rb"))
        old_units = pickle.load(open(UNITS_SAVE_PATH, "rb"))
    except:
        old_modules = []
        old_units = []
    open_url(driver, STUDENT_DETAILS_URL)

    username, password = get_login_data()

    if not login(driver, username, password):
        return False

    if not go_to_report_card(driver):
        return False

    modules, units = get_report_card(driver)

    if not modules or not units:
        return False

    if len(modules) != len(old_modules) or len(units) != len(old_units):
        send_report_card(modules, units)

    write_to_disk(modules, MODULES_SAVE_PATH)
    write_to_disk(units, UNITS_SAVE_PATH)
    return True


def fetch_nb_effectifs(driver: webdriver.Chrome) -> bool:
    try:
        old_effectifs = pickle.load(open(EFFECTIFS_SAVE_PATH, "rb"))
    except:
        old_effectifs = {}
    effectifs = {}

    open_url(driver, SCHEDULE_URL)

    username, password = get_login_data()

    if not login(driver, username, password):
        return False

    main_schedule = get_element(driver, By.ID, "mainSchedule")
    if not main_schedule:
        return False

    tooltips = main_schedule.find_elements(
        By.CSS_SELECTOR, "div[class='tooltip lesson--weekly']"
    )

    for tooltip in tooltips:
        module_name = tooltip.find_element(By.TAG_NAME, "p").get_attribute("innerHTML")
        a_tag = tooltip.find_element(
            By.CSS_SELECTOR, "a[class='tooltip--link tooltip__display-students']"
        )
        students = a_tag.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")

        if module_name not in effectifs:
            effectifs[module_name] = students
        elif students > effectifs[module_name]:
            effectifs[module_name] = students

    dif_set = set(old_effectifs.items()) ^ set(effectifs.items())
    text = ""
    for ele in sorted(dif_set):
        if ele in set(old_effectifs.items()):
            text += "[OLD]: "
        else:
            text += "[NEW]: "
        text += f"{ele[0]}: {ele[1]}\n"

    if dif_set:
        email_notification("Modification du nombre d'effectifs dans les horaires", text)
    write_to_disk(effectifs, EFFECTIFS_SAVE_PATH)
    return True


def fetch_new_schedule(driver: webdriver.Chrome) -> bool:
    try:
        next_schedule = pickle.load(open(NEXT_SCHEDULE_DATA_PATH, "rb"))
    except:
        next_schedule = ""

    open_url(
        driver,
        SCHEDULE_URL,
    )

    username, password = get_login_data()

    if not login(driver, username, password):
        return False

    schedule_div = get_element(driver, By.ID, "scheduleDiv")

    schedule_links = schedule_div.find_element(By.CLASS_NAME, "scheduleLinks")
    schedule_nav_bar = schedule_links.find_elements(By.TAG_NAME, "span")
    if len(schedule_nav_bar) < 3:
        return False
    schedule_nav_bar[2].click()
    driver.implicitly_wait(1)

    schedule_div = get_element(driver, By.ID, "scheduleDiv")

    schedule_html = schedule_div.get_attribute("innerHTML")

    if next_schedule != schedule_html and not "Aucun horaire" in schedule_html:
        email_notification(
            "Nouvel Horaire detecté",
            "",
        )

    write_to_disk(schedule_html, NEXT_SCHEDULE_DATA_PATH)
    return True


def main():
    log("Checking for new grades")

    driver = None
    name_func_dict = {
        "grades": fetch_grades,
        # "report card": handle_report_card,
        "nb d'effectifs": fetch_nb_effectifs,
        "new horaire": fetch_new_schedule,
    }
    try:
        for name, func in name_func_dict.items():
            driver = create_driver()
            if not func(driver):
                log(f"Couldn't get {name}")
            else:
                log(f"{name}: OK")
            driver.quit()
    except Exception as e:
        log(str(e))
    finally:
        if driver:
            driver.quit()
    log("Finished running")


if __name__ == "__main__":
    main()
