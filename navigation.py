from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_class import BaseClass

class LoginPage(BaseClass):

    @staticmethod
    def login(email, password):
        BaseClass.setUp()

        email = email.strip()
        password = password.strip()

        wait = WebDriverWait(BaseClass.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))

        email_field.send_keys(email)
        password_field.send_keys(password)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Log In']"))).click()

        try:
            error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content-margin']"))).text
            if "Invalid Email or Password" in error_message:
                print(f"❌ Invalid credentials error shown for {email}.")
            elif "Please enter a valid email" in error_message:
                print(f"❌ Invalid email format for {email}.")
            else:
                print(f"❌ Unexpected error for {email}: {error_message}")
            BaseClass.tearDown()
            return False
        except:
            print(f"✅ Login successful for {email}!")
            return True

if __name__ == "__main__":
    valid_email = "atomic.sam.03@gmail.com"
    valid_password = "Atomic@2020"
    print(f"\n🔍 Logging in with credentials: {valid_email}, {valid_password}")
    LoginPage.login(valid_email, valid_password)
