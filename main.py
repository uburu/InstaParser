import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class InstagramParse:

    def __init__(self, user_path):
        self._user_path = user_path
        response = requests.get(self._user_path, headers={'User-Agent': UserAgent().firefox})
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        for i,elem in enumerate(soup.body):
            if (i == 11):
                self._ProfilePageContainer ="https://www.instagram.com" + str(elem).split("src")[1].split('"')[1]
                print(self._ProfilePageContainer)

    def get_connection(self):
        pass


    def get_first_twelve(self, user_array):
        pass


    def get_photos_from_user_page(self, user_path, photo_num):
        pass


    def get_user_information(self, user_path):
        pass


link = "https://www.instagram.com/cappub/"
parse = InstagramParse(link)