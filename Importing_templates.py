import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 5)

wlTmpInitialStatuses = ["To Do", "Doing", "Done"]
wlTmpInitialPriorities = ["Low", "Medium", "High"]
wlTmpInitialPhases = []
wlTmpInitialTasks = []
wlTmpInitialLabels = []

driver.get("https://worklenz.com/authenticate")
driver.maximize_window()


# first custom function to login and go to project tab
def main():
    login()
    go_to_projects()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "coyonic318@hupoi.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "Test@12345")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()
    time.sleep(5)


def go_to_projects():
    driver.get("https://worklenz.com/worklenz/projects")
    time.sleep(10)


def go_to_project_temp():
    wait.until(EC.visibility_of_element_located((By.XPATH,
                                                 "//button[@class='ant-btn ant-dropdown-trigger ant-btn-primary ant-btn-icon-only ng-star-inserted']"))).click()
    time.sleep(1)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@class='ant-dropdown-menu-item']"))).click()
    time.sleep(1)


def get_need_temp():
    wlTemplatesList = driver.find_element(By.CLASS_NAME, "side-menu")
    wlTemplates = wlTemplatesList.find_elements(By.TAG_NAME, "li")
    wlTemplates[2].click()
    time.sleep(10)


def get_description_data():
    description = driver.find_element(By.CLASS_NAME, "worklenz_value_sec")
    descriptionText = description.text
    if len(descriptionText) > 0:
        print(" description is success")


def get_template_phase_data():
    phasesMenu_ = driver.find_element(By.CSS_SELECTOR,
                                      "div[class='cdk-global-overlay-wrapper'] div:nth-child(3) div:nth-child(2)")
    phases = phasesMenu_.find_elements(By.TAG_NAME, "nz-tag")
    for phase in phases:
        wlTmpInitialPhases.append(phase.text.strip())
    print("************** Start : Template phases *******************")
    print(wlTmpInitialPhases)
    print("************** End : Template phases ******************")


def get_template_label_data():
    labelsMenu = driver.find_element(By.CSS_SELECTOR,
                                     "div[class='cdk-global-overlay-wrapper'] div:nth-child(6) div:nth-child(2)")
    labels = labelsMenu.find_elements(By.TAG_NAME, "nz-tag")
    for label in labels:
        wlTmpInitialLabels.append(label.text)
    print("************** Start : Template Labels *******************")
    print(wlTmpInitialLabels)
    print("************** End : Template Labels ******************")


def get_template_tasks_data():
    tasksMenu = driver.find_element(By.CSS_SELECTOR, ".ant-list-items.ng-star-inserted")
    tasks = tasksMenu.find_elements(By.TAG_NAME, "li")
    # wlTmpInitialTasks.append(tasks)
    for task in tasks:
        wlTmpInitialTasks.append(task.text)
    print("************** Start : Template Tasks *******************")
    print(wlTmpInitialTasks)
    print("************** End : Template Tasks ******************")


def get_template_data():
    get_description_data()
    get_template_phase_data()
    get_template_label_data()
    get_template_tasks_data()


def check_tasks_data():
    taskListTasks = driver.find_elements(By.CLASS_NAME, "task-name-text")
    print(len(taskListTasks))
    print(len(wlTmpInitialTasks))
    if len(taskListTasks) == len(wlTmpInitialTasks):
        for taskListTask in taskListTasks:
            if taskListTask.text.strip() in wlTmpInitialTasks:
                print("Suceesfully added ", taskListTask.text, "Task")
            if taskListTask.text.strip() not in wlTmpInitialTasks:
                print("Not addded", taskListTask.text)
    else:
        print("Tasks not import correctly")


def check_statues_data():
    statusesMenus = driver.find_elements(By.TAG_NAME, "worklenz-task-list-group-settings")
    for statusesMenu in statusesMenus:
        statusesButton = statusesMenu.find_elements(By.TAG_NAME, "button")[0]
        statuses = statusesButton.find_elements(By.TAG_NAME, "span")[1]

        if statuses.text.strip() in wlTmpInitialStatuses:
            print("Successfully added", statuses.text, "Status")

        if statuses.text.strip() not in wlTmpInitialStatuses:
            print("Not added", statuses.text, "Status")


def check_labels_data():
    table_rows = driver.find_elements(By.TAG_NAME, "worklenz-task-list-row")
    for table_row in table_rows:
        cellsLabel = table_row.find_element(By.TAG_NAME, "worklenz-task-list-labels")
        cellsLabel.click()
        time.sleep(3)
        items = driver.find_elements(By.TAG_NAME, "li")
        for item in items:
            item_class_name = item.get_attribute("class")
            included_class_name = r'\bant-checkbox-wrapper-checked\b'
            check_label_class_name = re.search(included_class_name, item_class_name)
            if check_label_class_name:
                label = item.find_element(By.CLASS_NAME, "ant-badge-status-text")
                if label.text in wlTmpInitialLabels:
                    print("Successfully added ", label.text, "Label")
                else:
                    print("Not added", label.text, "Label")
                time.sleep(3)
        temp = driver.find_element(By.XPATH, "//label[normalize-space()='Group by:']")
        temp.click()
        time.sleep(3)


def check_priorities_data():
    buttonsList = driver.find_element(By.CLASS_NAME, "ant-col")
    groupByBtn = buttonsList.find_elements(By.TAG_NAME, "button")[5]
    groupByBtn.click()
    time.sleep(1)
    dropDownMain = driver.find_elements(By.CLASS_NAME, "cdk-overlay-pane")[-1]
    dropDownMenu = dropDownMain.find_element(By.CLASS_NAME, "ant-dropdown-menu")
    dropDownItems = dropDownMenu.find_elements(By.TAG_NAME, "li")[1]
    dropDownItems.click()
    time.sleep(2)

    priorityMenus = driver.find_elements(By.TAG_NAME, "worklenz-task-list-group-settings")
    for priorityMenu in priorityMenus:
        priorityButton = priorityMenu.find_elements(By.TAG_NAME, "button")[0]
        priorities = priorityButton.find_elements(By.TAG_NAME, "span")[1]
        prioritiesFullText = priorities.text
        prioritiesOnlyText = re.sub(r'\(\d+\)', '', prioritiesFullText).strip()

        if prioritiesOnlyText in wlTmpInitialPriorities:
            print("Successfully added ", prioritiesOnlyText, "Priority")

        else:
            print("Not added", prioritiesOnlyText, "Priority")


def check_phases_data():
    buttonsList = driver.find_element(By.CLASS_NAME, "ant-col")
    groupByBtn = buttonsList.find_elements(By.TAG_NAME, "button")[5]
    groupByBtn.click()
    time.sleep(1)
    dropDownMain = driver.find_elements(By.CLASS_NAME, "cdk-overlay-pane")[-1]
    dropDownMenu = dropDownMain.find_element(By.CLASS_NAME, "ant-dropdown-menu")
    dropDownItems = dropDownMenu.find_elements(By.TAG_NAME, "li")[2]
    dropDownItems.click()
    time.sleep(2)

    extractedPriorityText = []

    phaseMenus = driver.find_elements(By.TAG_NAME, "worklenz-task-list-group-settings")
    for phaseMenu in phaseMenus:
        phaseButton = phaseMenu.find_elements(By.TAG_NAME, "button")[0]
        phases = phaseButton.find_elements(By.TAG_NAME, "span")[1]
        fullText = phases.text.strip()

        onlyText = re.sub(r'\(\d+\)', '', fullText).strip()
        if onlyText in wlTmpInitialPhases:
            print("Succesully added ", onlyText, "Phase")

        else:
            print("Not added ", onlyText, "Phase")


def check_data_import_correctly():
    check_tasks_data()
    check_statues_data()
    check_labels_data()
    check_priorities_data()
    check_phases_data()


main()
expected_URL = "https://worklenz.com/worklenz/projects"
current_URL = driver.current_url
print(current_URL)
if expected_URL == current_URL:
    print("Projects tab page is loaded")
    go_to_project_temp()
    get_need_temp()
    get_template_data()
    createBtn = driver.find_element(By.CSS_SELECTOR,
                                    "button[class='ant-btn ant-btn-primary'] span[class='ng-star-inserted']")
    createBtn.click()
    check_data_import_correctly()
    time.sleep(3)


else:
    print("Projects tab page not loaded")

driver.quit()
