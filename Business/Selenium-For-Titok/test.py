from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Cấu hình đường dẫn đến WebDriver (VD: chromedriver)
webdriver_path = "path/to/chromedriver"  # Thay bằng đường dẫn thực tế

# Khởi tạo trình duyệt
browser = webdriver.Chrome(executable_path=webdriver_path)

try:
    # Mở trang Facebook
    browser.get("https://www.facebook.com")
    print("Facebook opened successfully.")

    # Đợi vài giây để trang tải
    time.sleep(5)
    
finally:
    # Đóng trình duyệt
    browser.quit()
