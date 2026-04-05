from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def launch_govt_portal(target_scheme_name):
    # Setup Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # 1. Target Portal pe jao (Example: Digital Gujarat)
        driver.get("https://www.digitalgujarat.gov.in/LoginApp/Login.aspx")
        
        # 2. Wait karo jab tak user Login aur Captcha khud na bhar de
        # Hum check karenge ki kya Dashboard URL load hua?
        print("Waiting for user to solve Captcha and Login...")
        
        # 3. 60 seconds ka time dete hain login karne ke liye
        WebDriverWait(driver, 60).until(
            EC.url_contains("Dashboard") or EC.url_contains("Service")
        )
        
        # 4. Login hote hi, seedha Scheme Search bar mein jao
        # (Yahan hum portal ke search element ki ID use karenge)
        search_box = driver.find_element(By.ID, "txtSearch") 
        search_box.send_keys(target_scheme_name)
        
        # 5. Search button click karo
        search_box.submit()
        
        print("User successfully landed on Scheme Page!")
        
    except Exception as e:
        print(f"Automation Stopped: {e}")