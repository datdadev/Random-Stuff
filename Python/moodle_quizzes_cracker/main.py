from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException

import time
import json

waitingTime = 0.5

init = True
training = True
result = True
isReviewMode = False # there is no table to review

def get_children_text(driver, parent_element):
    """
    Extracts the text content of all child elements of a parent element.
    """
    children_text = []
    for child in parent_element.find_elements(By.XPATH, ".//*"):
        children_text.append(child.text.strip())
    return children_text

def start_attempt_clicker(driver):
    button = WebDriverWait(driver, waitingTime).until(
    EC.element_to_be_clickable((By.XPATH, '''//button[contains(text(),'Attempt quiz') 
                                or contains(text(),'Re-attempt quiz') 
                                or contains(text(),'Continue your attempt')]'''))
    )
    button.click()

    try:
        start_attempt_button = WebDriverWait(driver, waitingTime).until(
            EC.element_to_be_clickable((By.ID, "id_submitbutton"))
        )
        button_value = start_attempt_button.get_attribute("value")
        if button_value.lower() == "start attempt":
            start_attempt_button.click()
    except TimeoutException:
        print("Timed out waiting for 'Start attempt' button")

def get_score(driver):
    table = driver.find_element(By.CSS_SELECTOR, "table.generaltable.quizattemptsummary")
    last_row = table.find_element(By.XPATH, "//tr[@class='lastrow']")

    # attempt_number = last_row.find_element(By.CSS_SELECTOR, ".c0").text.strip()
    marks = last_row.find_element(By.CSS_SELECTOR, ".c2").text.strip()
    # print("Attempt Number:", attempt_number)

    return float(marks)

def submit_all_and_finish_clicker(driver):
    submit_all_button = driver.find_element(By.XPATH, "//button[contains(text(),'Submit all and finish')]")
    if submit_all_button.is_displayed():
        submit_all_button.click()

    time.sleep(0.3)

    submit_all_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Submit all and finish')]")
    for submit_all_button in submit_all_buttons:
        if submit_all_button.is_displayed():
            last_submit_all_button = submit_all_button

    last_submit_all_button.click()

driver = webdriver.Chrome()
# driver.implicitly_wait(1)
# driver.set_page_load_timeout(1)

url = 'https://lms.hcmut.edu.vn/'
testUrl = 'https://lms.hcmut.edu.vn/mod/quiz/view.php?id=36259'

driver.get(url)

cookies = [
    {
        'name': 'MOODLEID1_',
        'value': r'%25CF%2560%25EBM%257D%251C'
    },
    {
        'name': 'MoodleSession',
        'value': r'bg2ejsq2stk39a54av3q00r81f'
    }
]
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

# Let the show begins...

start_time = time.time()

if init == True:
    driver.get(testUrl)
    start_attempt_clicker(driver)

    # Playing...
        
    data = []
    questionCount = 0
    stopped = False

    while(stopped == False):
        qtext_divs = driver.find_elements(By.CSS_SELECTOR, ".qtext")
        for qtext_index, qtext_div in enumerate(qtext_divs, start=1):
            qtext_children_text = get_children_text(driver, qtext_div)
            question = qtext_children_text[0]

            data.append({
                "question": question,
                "answers": [],
                "tried": [],
                "real": ""
            })
            
            sibling_element = qtext_div.find_element(By.XPATH, "following-sibling::*[1]")
            answernumber_spans = sibling_element.find_elements(By.CSS_SELECTOR, ".answernumber")
            for answer_index, answernumber_span in enumerate(answernumber_spans, start=1):
                answer_text = answernumber_span.find_element(By.XPATH, "following-sibling::div").text.strip()

                data[-1]["answers"].append(answer_text)

                if questionCount == 0 and answer_index == 1:
                    parent_element = answernumber_span.find_element(By.XPATH, "./parent::*")
                    radio_button = parent_element.find_element(By.XPATH, "preceding-sibling::input[@type='radio']")
                    ActionChains(driver).move_to_element(radio_button).click().perform()

                    data[-1]["tried"].append(answer_text)

            questionCount += 1

        finish_attempt_button = driver.find_element(By.ID, "mod_quiz-next-nav")
        finish_attempt_value = finish_attempt_button.get_attribute("value")
        if finish_attempt_value.lower().startswith("finish attempt"):
            finish_attempt_button.click()
            submit_all_and_finish_clicker(driver)

            stopped = True
        else:
            next_page_button = driver.find_element(By.ID, "mod_quiz-next-nav")
            next_page_value = next_page_button.get_attribute("value")
            if next_page_value.lower() == "next page":
                next_page_button.click()

    if isReviewMode == False:
        driver.get(testUrl)

        mark = get_score(driver)
        if mark != 0:
            data[0]["real"] = data[0]["answers"][0]
    else:
        state_divs2 = driver.find_elements(By.XPATH, "//div[@class='state']")
        for div_index, div in enumerate(state_divs2, start=1):
            if div.text == "Not answered" or div.text == "Incorrect":
                pass
            elif div.text == "Correct":
                data[0]["real"] = data[0]["answers"][0]

        driver.get(testUrl)

    with open("org_quiz_data.json", "w") as json_file:
        json.dump(data, json_file)

    with open("quiz_data.json", "w") as json_file:
        json.dump(data, json_file)

# If you already have initial JSON data, you do not have to run the previous code:

if training == True:
    loaded_data = []
    with open("org_quiz_data.json", "r") as json_file:
        loaded_data = json.load(json_file)

    selected = {
        "questionId": "",
        "selection": ""
    }

    progress = 0
    for question in loaded_data:
        if question["real"] != "":
            progress += 1

    driver.get(testUrl)

    while progress < len(loaded_data):
        driver.get(testUrl) # for sure
        start_attempt_clicker(driver)

        questionCount = 0

        isSelected = False
        while(isSelected == False):
            qtext_divs = driver.find_elements(By.CSS_SELECTOR, ".qtext")
            for qtext_index, qtext_div in enumerate(qtext_divs, start=1):
                qtext_children_text = get_children_text(driver, qtext_div)
                question = qtext_children_text[0]
                print(question)

                question_index = None
                for index, data in enumerate(loaded_data):
                    if data["question"] == question:
                        question_index = index
                        break
                
                if loaded_data[question_index]["real"] != "":
                    questionCount += 1
                    continue

                selected["questionId"] = question_index

                sibling_element = qtext_div.find_element(By.XPATH, "following-sibling::*[1]")
                answernumber_spans = sibling_element.find_elements(By.CSS_SELECTOR, ".answernumber")
                for answer_index, answernumber_span in enumerate(answernumber_spans, start=1):
                    answer_text = answernumber_span.find_element(By.XPATH, "following-sibling::div").text.strip()

                    if answer_text not in loaded_data[question_index]["tried"]:
                        loaded_data[question_index]["tried"].append(answer_text)

                        parent_element = answernumber_span.find_element(By.XPATH, "./parent::*")
                        radio_button = parent_element.find_element(By.XPATH, "preceding-sibling::input[@type='radio']")
                        ActionChains(driver).move_to_element(radio_button).click().perform()

                        selected["selection"] = answer_text
                        
                        while True:
                            finish_attempt_button = driver.find_element(By.ID, "mod_quiz-next-nav")
                            finish_attempt_value = finish_attempt_button.get_attribute("value")
                            if finish_attempt_value.lower().startswith("finish attempt"):
                                finish_attempt_button.click()
                                submit_all_and_finish_clicker(driver)
                                break
                            
                            next_page_button = driver.find_element(By.ID, "mod_quiz-next-nav")
                            next_page_value = next_page_button.get_attribute("value")
                            if next_page_value.lower() == "next page":
                                next_page_button.click()

                        isSelected = True
                        break

                if isSelected == True:
                    break

            if isSelected == False:
                if questionCount >= len(loaded_data) + 1:
                    finish_attempt_button = driver.find_element(By.ID, "mod_quiz-next-nav")
                    finish_attempt_value = finish_attempt_button.get_attribute("value")
                    if finish_attempt_value.lower().startswith("finish attempt"):
                        finish_attempt_button.click()

                    break

                next_page_button = driver.find_element(By.ID, "mod_quiz-next-nav")
                next_page_value = next_page_button.get_attribute("value")
                if next_page_value.lower() == "next page":
                    next_page_button.click()

        time.sleep(0.3)

        if isReviewMode == False:
            driver.get(testUrl)
            time.sleep(0.3)
            mark = get_score(driver)
            if mark != 0:
                loaded_data[selected["questionId"]]["real"] = selected["selection"]
        else:
            state_divs2 = driver.find_elements(By.XPATH, "//div[@class='state']")
            for div_index, div in enumerate(state_divs2, start=1):
                if div.text == "Not answered" or div.text == "Incorrect":
                    pass
                elif div.text == "Correct":
                    loaded_data[selected["questionId"]]["real"] = selected["selection"]
                    driver.get(testUrl)
                    time.sleep(0.3)
                    break

        progress = 0
        for question in loaded_data: # for more general cases
            if question["real"] != "":
                progress += 1

        with open("quiz_data.json", "w") as json_file:
            json.dump(loaded_data, json_file)

# Now, enjoy...

if result == True:
    driver.get(testUrl)
    start_attempt_clicker(driver)

    questionCount = 0

    result_data = []
    with open("quiz_data.json", "r") as json_file:
        result_data = json.load(json_file)

    while questionCount < len(result_data):
        qtext_divs = driver.find_elements(By.CSS_SELECTOR, ".qtext")
        for qtext_index, qtext_div in enumerate(qtext_divs, start=1):
            qtext_children_text = get_children_text(driver, qtext_div)
            question = qtext_children_text[0]

            question_index = None
            for index, data in enumerate(result_data):
                if data["question"] == question:
                    question_index = index
                    break
            
            sibling_element = qtext_div.find_element(By.XPATH, "following-sibling::*[1]")
            answernumber_spans = sibling_element.find_elements(By.CSS_SELECTOR, ".answernumber")
            for answer_index, answernumber_span in enumerate(answernumber_spans, start=1):
                answer_text = answernumber_span.find_element(By.XPATH, "following-sibling::div").text.strip()

                if answer_text == result_data[question_index]["real"]:
                    parent_element = answernumber_span.find_element(By.XPATH, "./parent::*")
                    radio_button = parent_element.find_element(By.XPATH, "preceding-sibling::input[@type='radio']")
                    ActionChains(driver).move_to_element(radio_button).click().perform()

                    questionCount += 1
                    break
            
        next_page_button = driver.find_element(By.ID, "mod_quiz-next-nav")
        next_page_value = next_page_button.get_attribute("value")
        if next_page_value.lower() == "next page":
            next_page_button.click()

        if questionCount >= len(result_data):
            finish_attempt_button = driver.find_element(By.ID, "mod_quiz-next-nav")
            finish_attempt_value = finish_attempt_button.get_attribute("value")
            if finish_attempt_value.lower().startswith("finish attempt"):
                finish_attempt_button.click()
                submit_all_and_finish_clicker(driver)

    driver.get(testUrl)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    with open("result.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write("------\n")
        for entry in result_data:
            txt_file.write("[Q]: " + entry["question"] + "\n")
            txt_file.write("[A]: " + entry["real"] + "\n")
            txt_file.write("------\n")

end_time = time.time()
runtime = end_time - start_time

print(f"Cracking {questionCount} questions in", runtime, "seconds")

time.sleep(5)

driver.quit()