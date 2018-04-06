import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import time


class InstagramParse:

    def __init__(self, user_path):
        self._user_path = user_path
        response = requests.get(self._user_path, headers={'User-Agent': UserAgent().firefox})
        self._json = response.content
        soup = BeautifulSoup(self._json, 'html.parser')
        for i,elem in enumerate(soup.body):
            if ('ProfilePageContainer.js' in str(elem)):
                ProfilePageContainer ="https://www.instagram.com" + str(elem).split("src")[1].split('"')[1]
                get_js = requests.get(ProfilePageContainer,
                                      headers={'User-Agent': UserAgent().firefox})
                content_js = get_js.content
                arr_js = str(content_js).split('null!=(o=e.profilePosts.byUserId.get(t))?o.pagination:o},queryId:')
                self._queryId = arr_js[1].split(",")[0].split('"')[1]

    def get_connection(self):
        '''Return data with all user information'''

        arr = str(self._json).split("window._sharedData = ")
        jsn = arr[1].split(";</script>")
        user_array = json.loads(str(jsn[0]))

        return user_array


    def get_first(self, photo_num, save_path):
        '''Save first photo's urls in save_path of user'''

        user_array = self.get_connection()
        photos = user_array['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        if (len(photos) != 0):
            for i, src in enumerate(photos):
                if (i < photo_num):
                    photo_link = src['node']['display_url']
                    response = requests.get(photo_link, headers={'User-Agent': UserAgent().chrome})
                    out = open(save_path + "img" + str(i) + ".jpg", "wb")
                    out.write(response.content)
                    out.close()
                    time.sleep(5)



    def get_photos_from_user_page(self, photo_num, save_path):
        '''Save specified numbers of photo in save_path of user'''

        self.get_first(photo_num ,save_path) # first photo

        if (photo_num > 12):
            user_array = self.get_connection()
            user_id = user_array['entry_data']['ProfilePage'][0]['graphql']['user']['id']
            user_data = user_array['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']
            if(user_data['has_next_page'] == True):
                end_cursor = user_data['end_cursor']
                url = "https://www.instagram.com/graphql/query/?query_hash=" \
                      + str(self._queryId) + "&variables=%7B%22id%22%3A%22"\
                      + str(user_id) +"%22%2C%22first%22%3A"+ str(photo_num - 12) +"%2C%22after%22%3A%22"\
                      + str(end_cursor) +"%22%7D"
                response = requests.get(url, headers={'User-Agent': UserAgent().firefox})
                photos = json.loads(str(response.content.decode('utf-8')))['data']['user']['edge_owner_to_timeline_media']['edges']
                if (len(photos) != 0):
                    for i,src in enumerate(photos):
                        photo_link = src['node']['display_url']
                        response = requests.get(photo_link, headers={'User-Agent': UserAgent().chrome})
                        out = open(save_path + "img" + str(i+11) + ".jpg", "wb")
                        out.write(response.content)
                        out.close()
                        time.sleep(5)


    def get_user_information(self, user_path):
        pass
