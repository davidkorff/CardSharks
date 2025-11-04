import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_to_mascot(driver):
    try:
        # Navigate to login page
        driver.get("https://app.withmascot.com/dashboard/portfolio?size=20&page=1")
        print("Page loaded")
        time.sleep(3)
        
        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_field.clear()
        time.sleep(1)
        email_field.send_keys("danielmargareten@gmail.com")
        print("Email entered")
        time.sleep(2)
        
        # Enter password
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        time.sleep(1)
        password_field.send_keys("6715Margareten!")
        print("Password entered")
        time.sleep(2)
        
        # Click login
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        print("Login button clicked")
        time.sleep(5)
        
        return True
    except Exception as e:
        print(f"Login error: {e}")
        return False

def process_all_pages(driver, start_page=1, end_page=59):
    try:
        # Create/open CSV with headers
        with open('card_titles.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Tag'])
        
        for page in range(start_page, end_page + 1):
            print(f"\nNavigating to page {page}")
            driver.get(f"https://app.withmascot.com/dashboard/portfolio?size=20&page={page}")
            time.sleep(3)
            
            # Process cards on current page
            items = driver.find_elements(By.CSS_SELECTOR, 
                "div.layout-container.css-0[style*='background-color: rgb(255, 255, 255)'][style*='flex-direction: row']")
            
            total_cards = len(items)
            print(f"Found {total_cards} cards on page {page}")
            
            # Process each card on the current page
            for i in range(total_cards):
                print(f"\nProcessing card {i+1} of {total_cards} on page {page}")
                time.sleep(2)
                
                # Refresh items list
                items = driver.find_elements(By.CSS_SELECTOR, 
                    "div.layout-container.css-0[style*='background-color: rgb(255, 255, 255)'][style*='flex-direction: row']")
                
                print(f"Clicking card {i+1}...")
                driver.execute_script("arguments[0].click();", items[i])
                time.sleep(3)
                
                # Extract title
                title_container = driver.find_element(By.CSS_SELECTOR, "div.layout-container.css-1lmx911")
                player_name = title_container.find_element(By.CSS_SELECTOR, "span.typography-h1").text
                card_details = title_container.find_element(By.CSS_SELECTOR, "span.typography-h3Light").text
                full_title = f"{player_name} {card_details}"
                print(f"Extracted title: {full_title}")
                
                # Extract tag
                try:
                    tag_element = driver.find_element(By.CSS_SELECTOR, 
                        "div.layout-container.selected-item span.typography-body")
                    tag = tag_element.text
                    print(f"Extracted tag: {tag}")
                except:
                    tag = ""
                    print("No tag found")
                
                # Save to CSV
                with open('card_titles.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([full_title, tag])
                
                # Close the modal
                print("Attempting to close card details...")
                try:
                    close_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 
                        "div.layout-container.icon-button-container.neutral.css-1wucykp"))
                    )
                    print("Found close button, clicking...")
                    close_button.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Error clicking close button: {e}")
                    
    except Exception as e:
        print(f"Error processing pages: {e}")

if __name__ == "__main__":
    driver = webdriver.Chrome()
    if login_to_mascot(driver):
        print("Starting to process all pages...")
        time.sleep(2)
        process_all_pages(driver)
        print("Processing complete!")
        time.sleep(2)
        driver.quit()
    else:
        print("Login failed")
        driver.quit()
