from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Bugs:

    driver = webdriver.Chrome("/Users/light/Downloads/chromedriver_win32/chromedriver")

    def __del__(self):
        self.driver.close()

    def login(self, ID, PW):
        self.driver.implicitly_wait(3)

        # 페이코 로그인
        self.driver.get("https://id.payco.com/oauth2.0/authorize?response_type=code&redirect_uri=https%3A%2F%2Fsecure.bugs.co.kr%2Fmember%2Fpayco%2Fcallback&state=state&serviceProviderCode=FRIENDS&userLocale=ko_KR&client_id=3RDtEDzmjKV9oZ7VFhSy")

        self.driver.find_element_by_id('id').send_keys(ID)
        self.driver.find_element_by_id('pw').send_keys(PW)
        self.driver.find_element_by_id('loginBtn').click()

    def getlist(self, listname):

        #재생목록 이동
        self.driver.get("https://music.bugs.co.kr/user/library/myalbum/list")

        self.driver.find_element_by_xpath('//a[@title="'+listname + " -페이지 이동"+'"]').click()

        songs=self.driver.find_elements_by_class_name('title')[5:]
        # for song in songs:
        #     print(song.text)
        # print(len(songs))
        artists=self.driver.find_elements_by_class_name('artist')[1:]
        # print(len(artists))

        # for artist in artists:
        #     print(artist.text)

        return artists, songs

    def addlist(self, artists, songs, listname):

        for i in range(len(songs)):
            song=songs[i]
            artist=artists[i]
            url="https://music.bugs.co.kr/search/integrated?q="+song+" "+artist
            self.driver.get(url)
            button = self.driver.find_elements_by_class_name('addAlbum')
            button[1].click()
            try:
                WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, '//a[@title="' + listname + '"]')))
            finally:
                self.driver.find_element_by_xpath('//a[@title="' + listname + '"]').click()