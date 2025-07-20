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
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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

        print("👋 Extracting student name and roll number...")
        welcome_text = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ctl00_cpHeader_ucStud_lblStudentName"))
        ).text.strip()

        print("📊 Extracting overall attendance percentage...")
        overall = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ctl00_cpStud_lblTotalPercentage"))
        ).text.strip()

        print("📚 Waiting for subject-wise attendance table...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ctl00_cpStud_grdSubject"))
        )

        print("📝 Processing subject-wise attendance data...")
        rows = driver.find_elements(By.XPATH, '//*[@id="ctl00_cpStud_grdSubject"]/tbody/tr')

        attendance_data = []

        for i, row in enumerate(rows[1:]):  # Skip header row
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 6:
                subject = cells[1].text.strip()
                faculty = cells[2].text.strip()
                classes_held = cells[3].text.strip()
                classes_attended = cells[4].text.strip()
                att_percent = cells[5].text.strip()
                attendance_data.append(
                    f"📚 Subject: {subject}\n"
                    f"👨‍🏫 Faculty: {faculty}\n"
                    f"🕒 Classes Held: {classes_held}, Attended: {classes_attended}\n"
                    f"📈 Attendance: {att_percent}%"
                )

        print("✅ Attendance fetch successful!")
        driver.quit()

        summary = f"👋 {welcome_text}\n\n✅ Your Latest Attendance: {overall}"
        if attendance_data:
            return f"{summary}\n\n" + "\n\n".join(attendance_data)
        else:
            return f"{summary}\n❗ No subject-wise attendance data found."

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        try:
            driver.save_screenshot("error_debug.png")
            print("📸 Screenshot saved as error_debug.png")
        except Exception as ss_err:
            print(f"❌ Could not save screenshot: {ss_err}")
        return f"❌ Error: {str(e) if str(e) else 'Unknown Selenium error — check screenshot.'}"
