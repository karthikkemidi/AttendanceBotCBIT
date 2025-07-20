from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_attendance(roll_no, password):
    print("🚀 Starting attendance fetch...")
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        print("🤖 Initializing Chrome driver...")
        driver = webdriver.Chrome(options=options)

        print("🌐 Navigating to login page...")
        driver.get("https://erp.cbit.org.in")

        print("👤 Entering roll number...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "txtUserName"))
        ).send_keys(roll_no)
        driver.find_element(By.ID, "btnNext").click()

        print("🔑 Entering password...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "txtPassword"))
        ).send_keys(password)
        driver.find_element(By.ID, "btnSubmit").click()

        print("👉 Clicking to enter student dashboard...")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Student Dashbord"))
        ).click()

        print("📊 Extracting overall percentage...")
        overall = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_cpStud_lblTotalPercentage"))
        ).text.strip()

        driver.quit()
        return f"✅ Your Latest Attendance is: {overall}"

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        try:
            print("📸 Saving screenshot for debugging...")
            driver.save_screenshot("error_debug.png")
            print("Screenshot saved as error_debug.png")
        except Exception as screenshot_error:
            print(f"Could not save screenshot: {screenshot_error}")
            pass
        return f"❌ Error: {str(e) if str(e) else 'Unknown Selenium crash — check screenshot.'}"
