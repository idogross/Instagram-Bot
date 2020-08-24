from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as error
import time
from pandas import Series


class IgBot:
    def __init__(self, driver_path, username, password):
        self.driver = webdriver.Chrome(driver_path)
        self.username = username
        self.password = password

    def close_driver(self):
        self.driver.close()

    def login_save_info(self):
        try:
            save_info_options = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "sqdOP.yWX7d.y3zKF")))
            save_info_options.click()
        except:
            return

    def login(self):
        self.driver.get('https://www.instagram.com/')
        login_user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#loginForm > div > div:nth-child(1) > div > label > input')))
        login_user.click()
        login_user.send_keys(self.username)
        password_user = self.driver.find_element_by_xpath\
                        ('//*[@id="loginForm"]/div/div[2]/div/label/input')
        password_user.click()
        password_user.send_keys(self.password)
        time.sleep(1)
        login_button = self.driver.find_element_by_class_name("Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB")
        login_button.click()
        time.sleep(4.5)
        self.login_save_info()
        try:
            popup_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "aOOlW.HoLwm")))
            popup_btn.click()
        except error.ElementClickInterceptedException:
            raise ValueError
        except error.TimeoutException:
            raise ValueError
        else:
            print(f'Log in for {self.username} succeeded!')

    def follow_user(self, follow_username):
        # this function searches user and follows them
        # function will work if login(self) is executed first.
        user_url = f'https://www.instagram.com/{follow_username}'
        self.driver.get(user_url)
        try:
            follow_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='Follow']")))
            follow_btn.click()
            print('Following!')
        except error.TimeoutException:
            try:
                check_follow = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'YBx95')))
                print('This bot already follows the client, or client has not yet approved the request!\n\
                 Please try another bot')

            except:
                print('This username does not exist')

    def unfollow_client(self, unfollow_username):
        # This function searches user and unfollows them
        # function will work if login(self) is executed first.
        user_url = f'https://www.instagram.com/{unfollow_username}'
        self.driver.get(user_url)
        try:
            unfollow_btn1 = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'glyphsSpriteFriend_Follow.u-__7')))
            unfollow_btn1.click()
            unfollow_btn2 = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, "aOOlW.-Cab_")))
            unfollow_btn2.click()
        except:
            print(f'This bot doest not follow {unfollow_username}')

    def like_posts(self, followed_username):
        # this function makes the bot to like {followed_username} posts
        user_url = f'https://www.instagram.com/{followed_username}'
        self.driver.get(user_url)
        time.sleep(2)
        for i in range(1, 3):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
        href = self.driver.find_elements_by_tag_name('a')
        posts = [elem.get_attribute('href') for elem in href if '.com/p/' in elem.get_attribute('href')]
        count = 0
        for post in posts:
            self.driver.get(post)
            maybe_like_btn = self.driver.find_elements_by_tag_name('svg')
            for like_btn in maybe_like_btn:
                if like_btn.get_attribute('aria-label') == "Unlike":
                    count += 1
                    break
                elif like_btn.get_attribute('aria-label') == "Like":
                    count = 0
                    like_btn.click()
                    break
            if count == 5:
                break
        
    def check_unfollowers(self, last_checked_flwers):
        # this function can be executed only after login()
        # last_checked_flwers is a list which contains the followers from previous check
        # this function will compare current followers with that last_checked_flwers
        client_url = f'https://www.instagram.com/{self.username}'
        self.driver.get(client_url)
        flwers_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, '/followers')]")))
        flwers_btn.click()
        flwers_popup = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "isgrP")))
        last_popup_height, popup_height = 0, 1
        while last_popup_height != popup_height:
            last_popup_height = popup_height
            time.sleep(1)
            popup_height = self.driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;', flwers_popup)
            try:
                stop_when_suggerstions = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
                self.driver.execute_script('arguments[0].scrollIntoView()', stop_when_suggerstions)
            except error.NoSuchElementException:
                continue
            else:
                break
        links_usernames = flwers_popup.find_elements_by_class_name("FPmhX.notranslate._0imsa")
        usernames = []

        for name in links_usernames:
            if name.text != '':
                usernames.append(str(name.text))
        self.driver.close()
        if len(last_checked_flwers) == 0:
            print('No previous followers check. Saving the current followers')
            return usernames
        else:
            names_copy = usernames.copy()
            recent_unfollowers = []
            for flw_name in last_checked_flwers:
                if flw_name not in usernames:
                    recent_unfollowers.append(flw_name)
                else:
                    names_copy.pop(names_copy.index(flw_name))
            if len(recent_unfollowers) > 0:
                print(f'Recent unfollowers: {recent_unfollowers}')
            else:
                print('No new unfollowers')
            if len(names_copy) > 0:
                print(f'New followers:{names_copy}')
            else:
                print('No new followers')
            print('Do not forget to save')
            return Series(usernames)
