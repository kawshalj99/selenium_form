from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()


url = "https://demoqa.com/automation-practice-form"

def open_form():
    driver.get(url)
    driver.maximize_window()


report = []

def add_to_report(test_name, status, message):
    report.append({"test_name": test_name, "status": status, "message": message})

def validate_submission(expected):
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        modal_title = driver.find_element(By.ID, "example-modal-sizes-title-lg").text
        return modal_title == expected
    except TimeoutException:
        return False


def test_valid_form_submission():
    open_form()

    try:
        driver.find_element(By.ID, "firstName").send_keys("Amal")
        driver.find_element(By.ID, "lastName").send_keys("Perera")
        driver.find_element(By.ID, "userEmail").send_keys("amal@gmail.com")


        gender_radio = driver.find_element(By.CSS_SELECTOR, "input[name='gender'][value='Male']")
        driver.execute_script("arguments[0].click();", gender_radio)

        driver.find_element(By.ID, "userNumber").send_keys("1234567890")


        date_input = driver.find_element(By.ID, "dateOfBirthInput")
        driver.execute_script("arguments[0].click();", date_input)
        time.sleep(1)  
        driver.find_element(By.CLASS_NAME, "react-datepicker__day--015").click()

        driver.find_element(By.ID, "subjectsInput").send_keys("Maths")
        driver.find_element(By.ID, "subjectsInput").send_keys(Keys.RETURN)


        hobbies_checkbox = driver.find_element(By.ID, "hobbies-checkbox-1")
        driver.execute_script("arguments[0].click();", hobbies_checkbox)

        driver.find_element(By.ID, "currentAddress").send_keys("123 Main Street")


        driver.execute_script("document.querySelectorAll('iframe').forEach(iframe => iframe.remove());")


        state_dropdown = driver.find_element(By.ID, "state")
        driver.execute_script("arguments[0].click();", state_dropdown)


        state_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='NCR']"))
        )
        driver.execute_script("arguments[0].click();", state_option)


        city_dropdown = driver.find_element(By.ID, "city")
        driver.execute_script("arguments[0].click();", city_dropdown)


        city_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[text()='Delhi']"))
        )
        driver.execute_script("arguments[0].click();", city_option)

        driver.find_element(By.ID, "submit").send_keys(Keys.RETURN)

        assert validate_submission("Thanks for submitting the form")
        add_to_report("Valid Form Submission", "Passed", "Form submitted successfully with valid data.")
    except Exception as e:
        add_to_report("Valid Form Submission", "Failed", str(e))


def test_mandatory_fields():
    open_form()
    
    try:
        driver.find_element(By.ID, "submit").send_keys(Keys.RETURN)
        
        errors = driver.find_elements(By.CLASS_NAME, "was-validated")
        assert errors, "Mandatory field validation failed."
        add_to_report("Mandatory Fields Validation", "Passed", "Errors displayed for mandatory fields.")
    except Exception as e:
        add_to_report("Mandatory Fields Validation", "Failed", str(e))


def test_invalid_email():
    open_form()

    try:
        driver.find_element(By.ID, "firstName").send_keys("Amal")
        driver.find_element(By.ID, "lastName").send_keys("Perera")
        driver.find_element(By.ID, "userEmail").send_keys("abc@xyz")
        driver.find_element(By.ID, "submit").send_keys(Keys.RETURN)

        error_message = driver.find_element(By.ID, "userEmail").get_attribute("validationMessage")
        assert error_message, "Invalid email validation failed."
        add_to_report("Invalid Email Validation", "Passed", "Proper validation message displayed for invalid email.")
    except Exception as e:
        add_to_report("Invalid Email Validation", "Failed", str(e))


test_valid_form_submission()
test_mandatory_fields()
test_invalid_email()


print("\nTest Execution Report")
print("="*30)
for entry in report:
    print(f"Test Name: {entry['test_name']}")
    print(f"Status: {entry['status']}")
    print(f"Message: {entry['message']}\n")


driver.quit()
