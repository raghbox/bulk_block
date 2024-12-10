

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


def safe_click(driver, element, wait_time=30):
    """Helper function to safely click on elements."""
    try:
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(element))
        driver.find_element(*element).click()
    except Exception as e:
        print(f"Error clicking on element {element}: {e}")

def safe_select(driver, element, value, wait_time=30):
    """Helper function to safely select from dropdowns."""
    try:
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(element))
        select_element = Select(driver.find_element(*element))
        select_element.select_by_value(value)
    except Exception as e:
        print(f"Error selecting value {value} from dropdown {element}: {e}")

def wait_for_file(download_dir, wait_time=30):
    """Wait for the file to be downloaded in the specified directory."""
    start_time = time.time()
    while time.time() - start_time < wait_time:
        downloaded_files = os.listdir(download_dir)
        if downloaded_files:
            return downloaded_files
        time.sleep(1)
    return []

def fetch_bse_bulk_block_deals(start_date_day, start_date_month, start_date_year,
                               end_date_day, end_date_month, end_date_year, download_dir):
    """Fetch BSE bulk/block deals data for a specified date range."""

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1900,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })


    chromedriver_path = "/home/micro2/.wdm/drivers/chromedriver/linux64/129.0.6668.100/chromedriver-linux64/chromedriver"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:

        #driver.get("https://www.bseindia.com/markets/equity/eqreports/bulknblockdeals.aspx")
        driver.get("https://www.bseindia.com/markets/equity/eqreports/bulknblockdeals.aspx")
        safe_select(driver, (By.ID, "ContentPlaceHolder1_rblDT"), "2")  # '2' is for Block Deal

        


        print("Waiting for checkbox to appear...")
        #safe_click(driver, (By.ID, "ContentPlaceHolder1_chkAllMarket"))
        element_locator = (By.ID, "ContentPlaceHolder1_chkAllMarket")

        try:

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(element_locator)
            )

            driver.find_element(*element_locator).click()
            print("Element clicked successfully.")
        except TimeoutException:
            print("Timeout: Element not clickable.")
        except Exception as e:
            print(f"An error occurred: {e}")
        print("Selecting start date...")
        start_date_input = driver.find_element(By.ID, "ContentPlaceHolder1_txtDate")
        start_date_input.click()
    #########################################################################################################################
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ui-datepicker-div")))
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-month"), start_date_month)
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-year"), "2014")
        #safe_select(driver, (By.CLASS_NAME, "ui-datepicker-year"), start_date_year)
        day_to_select_from = driver.find_element(By.XPATH, f"//a[@data-date='{start_date_day}']")
        day_to_select_from.click()
##########################################################################################################################
#########################################################################################################
#enddddddddddddddddddddddddddddd#
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ui-datepicker-div")))
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-month"), start_date_month)
        #safe_select(driver, (By.CLASS_NAME, "ui-datepicker-year"), 2014)
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-year"), start_date_year)
        day_to_select_from = driver.find_element(By.XPATH, f"//a[@data-date='{start_date_day}']")
        day_to_select_from.click()
        
        print("Selecting end date...")
        end_date_input = driver.find_element(By.ID, "ContentPlaceHolder1_txtToDate")
        driver.execute_script("arguments[0].scrollIntoView(true);", end_date_input)
        end_date_input.click()
###################################################################################################################################
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ui-datepicker-div")))
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-month"), end_date_month)
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-year"), "2014")
        day_to_select_to = driver.find_element(By.XPATH, f"//a[@data-date='{end_date_day}']")
        day_to_select_to.click()
#################################################################################################################
######################################################################################################################
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ui-datepicker-div")))
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-month"), end_date_month)
        safe_select(driver, (By.CLASS_NAME, "ui-datepicker-year"), end_date_year)
        day_to_select_to = driver.find_element(By.XPATH, f"//a[@data-date='{end_date_day}']")
        day_to_select_to.click()


        print("Clicking submit button...")
        safe_click(driver, (By.ID, "ContentPlaceHolder1_btnSubmit"))


        print("Waiting for the table data to load...")
        rows = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#ContentPlaceHolder1_divData1 tr'))
        )



        print("Attempting to click the download button...")
        download_button = driver.find_element(By.ID, 'ContentPlaceHolder1_btndownload1')
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(download_button))
        

        try:
            driver.execute_script("arguments[0].click();", download_button)
        except Exception as e:
            print(f"Error clicking with JS: {e}")
            download_button.click()


        print("Waiting for the file to be downloaded...")
        time.sleep(5)
        downloaded_files = wait_for_file(download_dir, wait_time=30)

        if downloaded_files:
            print("Downloaded files:", downloaded_files)


            for file in downloaded_files:
                old_file_path = os.path.join(download_dir, file)
                new_file_name = f"bse_bulk_block_deals_{start_date_day}_{start_date_month}_{start_date_year}_to_{end_date_day}_{end_date_month}_{end_date_year}.csv"
                download_dir1 ="/home/micro2/block/block"

                new_file_path = os.path.join(download_dir1, new_file_name)

                os.rename(old_file_path, new_file_path)
                print(f"File renamed to: {new_file_name}")
        else:
            print("No files were downloaded within the timeout period.")

    finally:
        driver.quit()


download_dir = "/home/micro2/block/filesa"


#fetch_bse_bulk_block_deals("1", "1", "2024", "9", "11", "2024", download_dir)
#for i in range(2023, 2025):
 #   fetch_bse_bulk_block_deals("1", "0", str(i), "31", "11", str(i), download_dir)
  #  print(i)