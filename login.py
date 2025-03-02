from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseClass:
    driver = None

    @staticmethod
    def pre_condition():
        BaseClass.driver = webdriver.Chrome()
        BaseClass.driver.maximize_window()
        BaseClass.driver.implicitly_wait(10)
        BaseClass.driver.get("https://app-staging.nokodr.com/")

    @staticmethod
    def post_condition():
        BaseClass.driver.quit()

    @staticmethod
    def sign_up():
        wait = WebDriverWait(BaseClass.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@class='slds-input ng-untouched ng-pristine ng-valid'])[3]")))
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "slds-checkbox__label"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='slds-col slds-size_1-of-1']"))).click()

class LoginPage(BaseClass):

    @staticmethod
    def login(email, password):
        BaseClass.pre_condition()

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
        except:
            print(f"✅ Login successful for {email}!")

        BaseClass.post_condition()

if __name__ == "__main__":
    test_cases = [
        ("atomic.sam.03@gmail.com", "Atomic@2020"),  
        ("", ""),  
        ("user@example.com", ""),  
        ("", "securepassword"),  
        ("invalid@gmail.com", "wrongpassword"),  
        ("john.doe@gmail.com", "wrongpassword"),  
        ("user@invalid.com", "ValidPass123"),  
        ("  user@gmail.com  ", "password123"),  
        ("user@gmail.com", "  password123  "),  
        ("invalid@!@gmail.com", "invalid@123"),  
        ("test@fake_domain.com", "SecurePass!@#"),  
        ("user123@gmail.com", "pa ss word"),  
        ("user@example.com", "short"),  
        ("USER@GMAIL.COM", "CaseSensitivePass123"),  
    ]

    for email, pwd in test_cases:
        print(f"\n🔍 Testing login with: {email}, {pwd}")
        LoginPage.login(email, pwd)
