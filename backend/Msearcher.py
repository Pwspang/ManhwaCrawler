from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import threading
from queue import Queue  

class MHandler(ABC):
    def __init__(self):

        # Config Driver
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080') # Set Window Size --> This is Required when use headless
        options.add_argument('--headless=new')
        options.add_argument('log-level=3')
        options.add_argument("--headless=new")
        self._driver = webdriver.Chrome(options=options)
    
    @abstractmethod
    def pop_up(self):
        pass
    
    @abstractmethod
    def search(self, text: str) -> list[tuple[str]]:
        pass
    
    @abstractmethod
    def get_chapters(self, link: str) -> list[tuple[str]]:
        pass
    
    @abstractmethod 
    def get_chapter_content(self, chapter_name: str, link: str) -> list[tuple[str]]:
        pass
    
    def get_chapter_bulk(self, q: Queue):
        while not q.empty():
            chapter_name, link = q.get()
            self.get_chapter_content(chapter_name, link)
        self.quit()
    
    def quit(self):
        self._driver.quit()

class MagakakalotHandler(MHandler):
    def __init__(self):
        super().__init__()
    
    def pop_up(self) -> None:
        # Detect if accept cookies is on screen 
        try:
            if self._driver.find_element(by=By.XPATH, value="//*[contains(text(), 'We value your privacy')]"):
                self._driver.find_element(by=By.XPATH, value="//*[contains(text(), 'DISAGREE')]").click()
        except Exception as e:
            pass 
        
    
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
    
    def get_chapter_content(self, chapter_name: str, link: str):
        self._driver.get(link)
        
        self.pop_up()
            
        #mangaName = self._driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[4]/h1').text
        
        content = self._driver.find_elements(by=By.XPATH, value="//img[contains(@alt, 'Chapter')]")
        
        for img in content:
            with Path("backend/images/{}/{}".format(chapter_name, img.get_attribute("src").split("/")[-1])) as file:
                file.parent.mkdir(exist_ok=True, parents=True)
                file.write_bytes(img.screenshot_as_png)

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
    
    def get_chapters(self, chapter_name: str, link: str) -> list:
        pass
    
    def get_chapter_content(self, link: str) -> list:
        pass

    def quit(self):
        self._driver.quit()     
        

def main():
    Searcher = MagakakalotHandler()
    #print(Searcher.search("Who"))
    manga_lst = Searcher.get_chapters('https://chapmanganato.to/manga-qp994350')
    
    Searcher.quit()
    
    # Queue for data 
    q = Queue()
    for chapter_name, link in manga_lst[:10]:
        q.put((chapter_name, link))
    
    # thread1 = threading.Thread(target=MagakakalotHandler().get_chapter_bulk, args=(q,))
    # thread2 = threading.Thread(target=MagakakalotHandler().get_chapter_bulk, args=(q,))
    # thread2.start()
    # thread1.start()
    # thread2.join()
    # thread1.join()
    
    #(*(MagakakalotHandler().get_chapter_content(chapter_name, chapter_link) for chapter_name, chapter_link in manga_lst[:5]))
    # [Searcher.get_chapter_content('Chapter-162', 'https://chapmanganato.to/manga-qp994350/chapter-162')]
    threads = [threading.Thread(target=MagakakalotHandler().get_chapter_bulk, args=(q ,)) for _ in range(5)]
    # MagakakalotHandler().get_chapter_bulk(q)
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    
    
    
    
    #Searcher.quit()

if __name__ == "__main__":
    main()