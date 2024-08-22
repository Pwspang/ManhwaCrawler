from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By


class MHandler(ABC):
    def __init__(self):
        self._driver = webdriver.Chrome()
    
    @abstractmethod
    def pop_up(self):
        pass
    
    @abstractmethod
    def search(self, text: str) -> list:
        pass
    
    @abstractmethod
    def get_chapters(self, link: str) -> list:
        pass
    
    @abstractmethod 
    def get_chapter_content(self, link: str) -> list:
        pass

    def quit(self):
        self._driver.quit()

class MagakakalotHandler(MHandler):
    def __init__(self):
        super().__init__()
    
    def pop_up(self):
        # Detect if accept cookies is on screen 
        if self._driver.find_element(by=By.XPATH, value="//*[contains(text(), 'We value your privacy')]"):
            self._driver.find_element(by=By.XPATH, value="//*[contains(text(), 'DISAGREE')]").click()
        
    
    def search(self, text: str) -> list:
        self._driver.get("https://mangakakalot.com/")
        
        self.pop_up()
        
        search_box = self._driver.find_element(by=By.ID,  value="search_story")
        search_box.send_keys(text)
        
        self._driver.implicitly_wait(5)
        
        search_result = self._driver.find_element(by=By.ID, value="search_result")
        
        links_lst =  [i.get_attribute("href") for i in search_result.find_elements(by=By.XPATH, value="//ul/a[@href]")]
        name_lst = [i.text for i in search_result.find_elements(by=By.XPATH, value="//p[@class='search_result_row1']")]
        
        return list(zip(name_lst, links_lst))
    
    def get_chapters(self, link: str) -> list:
        self._driver.get(link)
        
        self.pop_up()
            
        chapter_lst = self._driver.find_elements(by=By.CLASS_NAME, value="chapter-name")
        #print([i.get_attribute("href") for i in chapter_lst])
        
        return list(zip([i.text for i in chapter_lst], [i.get_attribute("href") for i in chapter_lst]))
    
    def get_chapter_content(self, link: str):
        self._driver.get(link)
        
        self.pop_up()
            
        #mangaName = self._driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[4]/h1').text
        
        content = self._driver.find_elements(by=By.XPATH, value="//img[contains(@alt, 'Chapter')]")
        
        for img in content:
            
            with open("backend/images/" + img.get_attribute("src").split("/")[-1], 'wb') as file:
                file.write(img.screenshot_as_png)

class MangaBTTHandler(MHandler):
    def __init__(self):
        super().__init__()
        
    def pop_up(self):
        # Detect if accept cookies is on screen 
        if self._driver.find_element(by=By.XPATH, value="//*[@id='sd-cmp']/div[2]/div[1]/div/div/div/div/div[1]/div[3]/button/span"):
            self._driver.find_element(by=By.XPATH, value="//*[@id='sd-cmp']/div[2]/div[1]/div/div/div/div/div[1]/div[3]/button/span").click()
        
    
    def search(self, text: str) -> list:
        self._driver.get("https://manhwalampo.com/")
        
        self.pop_up()
        
        search_box = self._driver.find_element(by=By.XPATH,  value="/html/body/header/div/div[1]/div/div[2]/div/input")
        search_box.send_keys(text)
        
        self._driver.implicitly_wait(5)
        
        search_result = self._driver.find_element(by=By.XPATH, value="/html/body/header/div/div[1]/div/div[2]/div/div[2]/ul")
        
        links_lst =  [i.get_attribute("href") for i in search_result.find_elements(by=By.XPATH, value="//a[@href]")]
        name_lst = [i.text for i in self._driver.find_elements(by=By.XPATH, value="//a/span")]
        
        return list(zip(name_lst, links_lst))
    
    def get_chapters(self, link: str) -> list:
        pass
    
    def get_chapter_content(self, link: str) -> list:
        pass

    def quit(self):
        self._driver.quit()     
        

def main():
    Searcher = MagakakalotHandler()
    
    print(Searcher.search("Who"))
    #print(Searcher.get_chapters('https://chapmanganato.to/manga-qp994350'))
    
    #Searcher.get_chapter_content('https://chapmanganato.to/manga-qp994350/chapter-162')
    
    Searcher.quit()

if __name__ == "__main__":
    main()