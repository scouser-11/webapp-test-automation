from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BaseClass:
    driver = None

    @staticmethod
    def pre_condition():
        """Initialize a new browser instance for each test."""
        BaseClass.driver = webdriver.Chrome()
        BaseClass.driver.maximize_window()
        BaseClass.driver.implicitly_wait(10)
        BaseClass.driver.get("https://app-staging.nokodr.com/")

    @staticmethod
    def post_condition():
        if BaseClass.driver:
            BaseClass.driver.quit()

    @staticmethod
    def navigate_to_signup():
        wait = WebDriverWait(BaseClass.driver, 10)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign up"))).click()

    @staticmethod
    def fill_common_fields(email, check_terms=True):
        wait = WebDriverWait(BaseClass.driver, 10)

        email_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//input[@class='slds-input ng-untouched ng-pristine ng-valid'])[3]"))
        )
        email_input.clear()  
        email_input.send_keys(email)

        if check_terms:
            terms_checkbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "slds-checkbox__label")))
            terms_checkbox.click()

    @staticmethod
    def submit_form():
        wait = WebDriverWait(BaseClass.driver, 10)
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='slds-col slds-size_1-of-1']")))
        submit_button.click()

class SignupPage(BaseClass):
    @staticmethod
    def signup_test(email, check_terms=True):
        BaseClass.pre_condition()
        try:
            BaseClass.navigate_to_signup()
            BaseClass.fill_common_fields(email, check_terms)
            BaseClass.submit_form()

            wait = WebDriverWait(BaseClass.driver, 10)
            message_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'OTP')]")
            ))
            actual_message = message_element.text
            if "OTP" in actual_message:
                print("Test Passed: Found expected success message containing 'OTP'")
            else:
                print(f"Test Failed: Expected message containing 'OTP', but found '{actual_message}'")
        except TimeoutException:
            print("Test Failed: Timed out waiting for OTP message")
        except Exception as e:
            print(f"Test encountered an exception: {e}")
        finally:
            BaseClass.post_condition()

if __name__ == "__main__":
    print("Running valid input test...")
    SignupPage.signup_test(
        email="valid.email@example.com",
        check_terms=True
    )
