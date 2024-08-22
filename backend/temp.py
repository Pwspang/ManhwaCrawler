from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def main():
    driver = webdriver.Chrome()

    driver.get("https://mangakakalot.com/")

    driver.implicitly_wait(2)
    
    #title = driver.title 

    SEARCH_TEXT = "The Story About Time"
    
    # Detect if accept cookies is on screen 
    if driver.find_element(by=By.XPATH, value="//*[contains(text(), 'We value your privacy')]"):
        driver.find_element(by=By.XPATH, value="//*[contains(text(), 'DISAGREE')]").click()
    
    searchBox = driver.find_element(by=By.ID,  value="search_story")

    searchBox.send_keys(SEARCH_TEXT)
    
    driver.implicitly_wait(2)
    
    result = driver.find_element(by=By.ID, value="search_result")
    
    #result_lst = result.find_elements(by=By.XPATH, value="//ul/a[@href]")
    result_lst = result.find_elements(by=By.XPATH, value="//p[@class='search_result_row1']")
    print(result_lst)
    for i in result_lst:
        print(i.text)
    
    
       
    
    driver.quit()
    
if __name__ == "__main__":
    main()

