from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base_class import BaseClass

class ForgotPasswordTests(BaseClass):

    @staticmethod
    def go_to_forgot_password():
        """Navigate to the forgot password page."""
        BaseClass.driver.get("https://app-staging.nokodr.com/")
        wait = WebDriverWait(BaseClass.driver, 10)
        forgot_password_link = (By.LINK_TEXT, "Forgot Password?")
        wait.until(EC.element_to_be_clickable(forgot_password_link)).click()
        wait.until(EC.presence_of_element_located((By.ID, "email")))

    @staticmethod
    def test_empty_email():
        print("Testing empty email validation...")
        wait = WebDriverWait(BaseClass.driver, 10)
        proceed_button = (By.XPATH, "//div[@title='Proceed']")
        wait.until(EC.element_to_be_clickable(proceed_button)).click()
        try:
            error_locator = (By.XPATH, "//div[contains(@class, 'MuiFormHelperText-root') and contains(@class, 'Mui-error')]")
            error_element = wait.until(EC.visibility_of_element_located(error_locator))
            error_text = error_element.text
            assert "Please enter email" in error_text, f"Empty email validation failed! Message was: '{error_text}'"
            print("Empty email validation passed.")
        except TimeoutException:
            print("Empty email validation failed. Error message not found!")

    @staticmethod
    def test_non_registered_email():
        print("Test Case: Verifying error message for a non-registered email.")
        wait = WebDriverWait(BaseClass.driver, 10)
        email_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//input[@class='slds-input ng-untouched ng-pristine ng-valid'])[3]"))
        )
        email_field.clear()
        email_field.send_keys("nonregistered@example.com")
        proceed_button = (By.XPATH, "//div[@title='Proceed']")
        wait.until(EC.element_to_be_clickable(proceed_button)).click()
        try:
            error_message = (By.XPATH, "//div[@class='content-margin']")
            message = wait.until(EC.visibility_of_element_located(error_message)).text
            assert "User does not exists" in message, "Non-registered email validation Failed!"
            print(f"Test Passed: Correct error message '{message}' displayed for non-registered email.")
        except TimeoutException:
            print("Test Failed: No error message appeared for non-registered email within the time limit.")

    @staticmethod
    def test_valid_email():
        print("Test Case: Verifying success message for a valid registered email.")
        wait = WebDriverWait(BaseClass.driver, 10)
        email_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//input[@class='slds-input ng-untouched ng-pristine ng-valid'])[3]"))
        )
        email_field.clear()
        email_field.send_keys("atomic.sam.03@gmail.com")
        proceed_button = (By.XPATH, "//div[@title='Proceed']")
        wait.until(EC.element_to_be_clickable(proceed_button)).click()
        try:
            success_message = (By.XPATH, "//div[@class='content-margin']")
            message = wait.until(EC.visibility_of_element_located(success_message)).text
            assert "Verification code sent successfully" in message, "Test Passed!"
            print(f"Test Passed: Correct success message {message} displayed for valid email.")
        except TimeoutException:
            print("Test Failed: No success message appeared for valid email within the time limit.")

if __name__ == "__main__":
    BaseClass.setUp()
    ForgotPasswordTests.go_to_forgot_password()
    ForgotPasswordTests.test_empty_email()

    ForgotPasswordTests.go_to_forgot_password()
    ForgotPasswordTests.test_non_registered_email()

    ForgotPasswordTests.go_to_forgot_password()
    ForgotPasswordTests.test_valid_email()
    BaseClass.tearDown()
