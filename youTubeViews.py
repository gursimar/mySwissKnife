from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import mechanize
import cookielib
import clipboard
import time, random, string

class iBallRouter:
    ip = '192.168.1.2'
    url = 'http://' + ip
    uname = 'admin'
    password = 'admin'
    statusFrame = '/userRpm/StatusRpm.htm'
    surl = 'http://' + uname + ':' + password + '@' + ip

    def __init__(self):# url, uname, password):
        #self.url = url
        #self.uname = uname
        #self.password = password
        br = mechanize.Browser()
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        #br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        # br.set_debug_http(True)
        # br.set_debug_redirects(True)
        # br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.add_password(self.url, self.uname, self.password)
        self.br = br

        # set up selenium instance
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.http.phishy-userpass-length', 255)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get(self.surl)
        self.driver = driver

    def readStatusPage(self):
        result = {}
        response = self.br.open(self.url + self.statusFrame)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        js_array = soup.findAll('script', type="text/javascript")
        for js_text in js_array:
            if 'var wanPara' in str(js_text):
                js_elements = str(js_text).split('\n')
                publicIP = js_elements[4].split("\"")[1]
                result['publicIP'] = publicIP
        return result

    def __seleniumSwitchFrame(self, frameName):
        try:
            self.driver.switch_to_frame(self.driver.find_element_by_name(frameName))
        except NoSuchElementException:
            print 'Already entered the frame'


    def disconnectWAN(self):
        self.__seleniumSwitchFrame('mainFrame')
        button = self.driver.find_element_by_name('Disconnect')
        button.click()

    def connectWAN(self):
        self.__seleniumSwitchFrame('mainFrame')
        button = self.driver.find_element_by_name('Connect')
        button.click()

    def deleteAllCookies(self):
        self.driver.delete_all_cookies()

    def changeIP(self):
        time.sleep(4)
        print self.readStatusPage()
        time.sleep(2)
        self.disconnectWAN()
        time.sleep(6)
        self.connectWAN()
        time.sleep(6)
        print self.readStatusPage()


class seleniumYouTube:
    url = "http://www.youtube.com/"
    def __init__(self, vid, vTitle, searchTerms):
        self.vid = vid
        self.searchTerms = searchTerms
        self.vTitle = vTitle

        # set up selenium instance
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.http.phishy-userpass-length', 255)
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get(self.url)
        self.driver = driver

    def openYouTube(self):
        self.driver.get(self.url)
        time.sleep(3)

    #search one of the random search terms
    def searchVideo(self):
        searchTerm = self.__perturbateSearchTerm(self.__getRandomSearchTerm())
        print ' Search Term: ' + searchTerm
        elem = self.driver.find_element_by_name("search_query")
        elem.clear()
        elem.send_keys(searchTerm + Keys.RETURN)

    def playRandVideo(self):
        rand_vid_no = random.randrange(1,4)
        try:
            elem = self.driver.find_element_by_xpath("//ol[@class='item-section']/li[" + str(rand_vid_no) + "]/div/div/div[2]/*/a");
            elem.click()
            playTime = 60 + random.randrange(-30,30)
            time.sleep(playTime)
            self.driver.back()
            print " Random video played successfully: " + + str(rand_vid_no) + 'Time - ' + str(playTime)
        except:
            print ' Could not play random video: ' + str(rand_vid_no)
            pass

    def playTargetVideo(self):
        try:
            elem = self.driver.find_element_by_link_text(self.vTitle)
            elem.click()
            playTime = 170 + random.randrange(-30, 40)
            time.sleep(playTime)
            self.driver.back()
            print " Video played successfully: " + str(playTime)
        except:
            print ' Could not play target video'
            pass

    def hitTarget(self):
        self.driver.get(self.url + self.vid)
        time.sleep(170 + random.randrange(-40, 50))
        print " HIT: Video played successfully"

    def deleteAllCookies(self):
        self.driver.delete_all_cookies()

    def __getRandomSearchTerm(self):
        vidno = random.randrange(0,len(self.searchTerms)-1)
        searchTerm = self.searchTerms[vidno]
        return searchTerm

    def __perturbateSearchTerm(self, searchTerm):
        search_keywords = searchTerm.split()
        random.shuffle(search_keywords)

        # change keywords
        which_key = random.randrange(0,len(search_keywords)-1)
        keyword_to_change = list(search_keywords[which_key])
        which_letter = random.randrange(0,len(keyword_to_change)-1)
        keyword_to_change[which_letter] = random.choice(string.letters);
        search_keywords[which_key] = ''.join(keyword_to_change)

        result = ' '.join(search_keywords)
        return result


if __name__ == '__main__':
    vid = 'watch?v=vMlZwQZMwDs'
    vTitle = 'KDD2016 paper 798'
    searchTerms = [
        'kdd2016 aspiring minds kdd2016',
        'kdd2016 gursimran assessment of codes kdd2016',
        'kdd2016 automated assessment of prgramming codes kdd2016',
        'kdd2016 automated assessment kdd2016',
        'kdd2016 prgramming codes kdd2016',
        'automated assessment of programming codes gursimran kdd2016',
        'gursimran varun kdd kdd2016',
        'kdd gursimran kdd2016',
        #'gursimran machine learning',
        'aspiring minds machine leanring kdd2016',
        'KDD2016 paper 798 gursimran aspiring minds',
        'Case of Computer Program Grading kdd',
        'Question Independent Grading using Machine Learning',
        'grade open-ended responses kdd2016 gursimran'
    ]
    router = iBallRouter()
    youtube = seleniumYouTube(vid, vTitle, searchTerms)
    while(1):
        try:
            print '\r\n\r\n------ Process Started ------'
            router.changeIP()
            youtube.openYouTube()
            time.sleep(3)

            if random.choice([0,1,2]) == 0:
                #direct hit
                youtube.hitTarget()

            else:
                #simulate a user search
                print 'Video searching started'
                try:
                    youtube.searchVideo()
                except:
                    print "Search failed"
                    continue
                time.sleep(10)
                print 'Video searching complete'

                print 'Rand video process started'
                youtube.playRandVideo()
                waitTime = random.randrange(1,20)
                print 'Waiting for: ' + str(waitTime)
                time.sleep(waitTime)

                print 'Rand video process started'
                youtube.playRandVideo()
                waitTime = random.randrange(7,20)
                print 'Waiting for: ' + str(waitTime)
                time.sleep(waitTime)

                print 'Rand video process started'
                youtube.playRandVideo()
                waitTime = random.randrange(1,10)
                print 'Waiting for: ' + str(waitTime)
                time.sleep(waitTime)

                print 'Target video process started'
                youtube.playTargetVideo()
                waitTime = random.randrange(1,10)
                print 'Waiting for: ' + str(waitTime)
                time.sleep(waitTime)

                print 'Rand video process started'
                youtube.playRandVideo()
                waitTime = random.randrange(1,20)
                print 'Waiting for: ' + str(waitTime)
                time.sleep(waitTime)

                print 'Rand video process started'
                youtube.playRandVideo()

                # Final delay
                if random.choice([0, 1, 2, 3, 4 , 5]) == 0:
                    #large delay
                    waitTime = random.randrange(500, 800)
                    print 'Waiting for: ' + str(waitTime)
                    time.sleep(waitTime)
                else:
                    # small delay
                    waitTime = random.randrange(50, 600)
                    print 'Waiting for: ' + str(waitTime)
                    time.sleep(waitTime)

            youtube.deleteAllCookies()
            print '--DONE--'
        except:
            print 'Exception'
            pass

