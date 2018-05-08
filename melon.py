from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Melon:

    driver = webdriver.Chrome("/Users/light/Downloads/chromedriver_win32/chromedriver")

    def __del__(self):
        self.driver.close()

    def login(self, ID, PW):
        self.driver.implicitly_wait(3)

        #카카오로 멜론에 로그인
        self.driver.get(
            "https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D6cfb479f221a5adc670fe301e1b6690c%26redirect_uri%3Dhttps%253A%252F%252Fmember.melon.com%252Foauth.htm%26response_type%3Dcode%26state%3DQoPOExRFFYvp3zu2pt%252Fp8lbwAb7uQYgIMV4AC3CyIn73LPNs2NSI23e4ErQuwD8S%26encode_state%3Dfalse")

        self.driver.find_element_by_name('email').send_keys(ID)
        self.driver.find_element_by_name('password').send_keys(PW)
        self.driver.find_element_by_class_name('btn_login').click()

        #멜론 사이트로 이동
        self.driver.get("https://melon.com")

        self.driver.find_element_by_class_name('btn_login').click()
        self.driver.find_element_by_class_name('btn_kakao_login').click()
        time.sleep(3)

    def getlist(self, listname):

        #재생목록 페이지로 이동
        self.driver.find_element_by_xpath('//a[@href="'+"javascript:MELON.WEBSVC.POC.menu.goMyMusicMain();"+'"]').click()
        self.driver.find_element_by_xpath('//a[@title="'+ "플레이리스트 - 페이지 이동"+'"]').click()
        self.driver.find_element_by_xpath('//a[@title="'+ listname + " - 페이지 이동"+'"]').click()

        tmp = self.driver.find_elements_by_class_name('cnt')
        num = int(tmp[0].text[1:-1])
        idx=1
        songNames=[]
        artistNames=[]

        #멜론은 페이지가 50개 단위로 나뉘어져 있기 때문에 페이지에 따라 저장
        while True:

            try:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME,'table')))
            finally:
                artists = self.driver.find_elements_by_id('artistName')
                for artistName in artists:
                    artistNames.append(artistName.text)
                    print("artist: " + artistName.text)

                songs = self.driver.find_elements_by_class_name('fc_gray')
                for songName in songs:
                    songNames.append(songName.text)
                    print("song " + songName.text)
                idx += 50
                if idx>num:
                        break
                self.driver.find_element_by_xpath('//a[@href="'+"javascript:pageObj.sendPage('"+str(idx)+"');"+'"]').click()

        return artistNames, songNames

    def addlist(self, artists, songs, listname):


        for i in range(len(songs)):
            song=str(songs[i].text)
            artist=str(artists[i].text)
            #노래 제목에 포함된 특수문자 제거
            song=song.replace("'", "")
            song=song.replace("’", "")
            song=song.replace("&", "")

            #아티스트 이름 오류 수정
            if artist[len(artist)//2]=="\n":
                artist=artist[0:len(artist)//2]

            #괄호로 영어와 한글로 나뉜 경우
            start = artist.find('(')
            if start>0:
                artist=artist[:start]

            url="http://www.melon.com/search/song/index.htm?q="+song+" "+artist
            self.driver.get(url)
            try:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,'add')))
                self.driver.find_elements_by_class_name('add')[0].click()

                window_after = self.driver.window_handles[1]
                self.driver.switch_to_window(window_after)

                button = self.driver.find_element_by_xpath('//a[@title="' + listname + " 플레이리스트 선택" + '"]').click()

            except:
                # 영어나 한글 중 하나로 노래를 찾지 못한 경우
                if start>0:
                    artist=artists[i].text[start+1:-1]
                    url = "http://www.melon.com/search/song/index.htm?q=" + song + " " + artist
                    self.driver.get(url)
                    try:
                        element = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, 'add')))
                        self.driver.find_elements_by_class_name('add')[0].click()

                        window_after = self.driver.window_handles[1]
                        self.driver.switch_to_window(window_after)

                        button = self.driver.find_element_by_xpath(
                            '//a[@title="' + listname + " 플레이리스트 선택" + '"]').click()

                    except:
                        print(song+" "+artist)
            finally:
                for j in range(len(self.driver.window_handles)-1,1,-1):
                    self.driver.switch_to_window(self.driver.window_handles[j])
                    self.driver.close()
                self.driver.switch_to_window(self.driver.window_handles[0])
