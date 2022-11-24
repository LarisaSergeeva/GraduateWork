import json
from pprint import pprint

import requests

# from TOKENS_ID import id_VK
from TOKENS_ID import token_VK
from TOKENS_ID import token_YD

import time


class UserVK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self, album, number):
        URL = 'https://api.vk.com/method/photos.get'
        if album == '1':
            params = {'owner_id': self.id, 'album_id': 'profile', 'extended': '1', 'count': number}
        elif album == '2':
            params = {'owner_id': self.id, 'album_id': 'wall', 'extended': '1', 'count': number}
        elif album == '3':
            album_id = input('Введите id, интересующего Вас альбома: ')
            params = {'owner_id': self.id, 'album_id': album_id, 'extended': '1', 'count': number}
        else:
            print('При выборе альбома произошла ошибка.')
        responce = requests.get(URL, params={**self.params, **params})
        try:
            responce.raise_for_status()
            print('Соединение с Api VK установлено.')
        except Exception as e:
            print('Ошибка при загрузке страницы: ' + str(e))
        return responce.json()

    def urls_list(self, dict_info):
        photos_list = list()
        url_dict = {}
        names_list = list()
        for _ in range(len(dict_info['response']['items'])):
            photos_dict = {}
            name = str(dict_info['response']['items'][_]['likes']['count'])
            names_list += [name]
            for elem in range(len(names_list)-1):
                if name == names_list[elem]:
                    data = dict_info['response']['items'][_]['date']
                    data = time.strftime("%d %b %Y", time.localtime(data))
                    name = name + '.' + data
            url = dict_info['response']['items'][_]['sizes'][-1]['url']
            name += '.jpg'
            url_dict[name] = url
            print("Информация о фотографии ", _ + 1, 'получена.')
            photos_dict['file name'] = name
            photos_dict['size'] = dict_info['response']['items'][_]['sizes'][-1]['type']
            photos_list.append(photos_dict)
        print('Создан словарь со значениями url-фотографий нужного размера.')
        print('Создан список словарей с полями file name и size.')
        photos_json = json.dumps(photos_list)
        print('Файл в формате json получен: ')
        pprint(photos_json)
        return url_dict


class UserYD:
    def __init__(self, _token: str):
        self.token = "OAuth " + _token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f'OAuth {self.token}'}

    def create_folder(self, name_folder: str):
        responce_ = requests.put(f'{self.url}?path={name_folder}', headers=self.headers)
        try:
            responce_.raise_for_status()
            print('Соединение с Яндекс,Диск для создания папки установлено.')
        except Exception as e:
            print('Ошибка при загрузке страницы: ' + str(e))
        print("Папка успешно создана.")

    def upload_file(self, name_folder, photos_name, photos_url):
        url_ = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        path = str(name_folder) + '/' + str(photos_name)
        params = {'path': path, 'url': photos_url}
        responce = requests.post(url_, params=params, headers=self.headers)
        try:
            responce.raise_for_status()
            print('Соединение с Яндекс.Диском для загрузки фотографий установлено.')
        except Exception as e:
            print('Ошибка при загрузке страницы: ' + str(e))


def main():
    id_vk = input('Введите id пользователя Вконтакте: ')
    album_choice = input('Выберете фотографии из какого альбома Вконтакте Вы хотите загрузить на Яндекс.Диск: '
                         '1 - фотографии профиля,'
                         '2 - фотографии со стены,'
                         '3 - фотографии из других альбомов: ')
    number_of_photos = input('Введите число фотографий для загрузки: ')

    user_vk = UserVK(token_VK, id_vk)
    info_dict = user_vk.get_photos(album_choice, number_of_photos)
    url_dict = user_vk.urls_list(info_dict)
    folder_name = input('Введите имя папки на Яндекс.Диске для загрузки фотографий: ')
    user_yd = UserYD(token_YD)
    user_yd.create_folder(folder_name)
    number = 0
    for k, v in url_dict.items():
        number += 1
        user_yd.upload_file(folder_name, k, v)
        print('Загружена фотография ', number)
    print('Все фотографии успешно загружены в папку.')


if __name__ == '__main__':
    main()




