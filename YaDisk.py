import requests
import VK

ya_token = input('Введите OAuth-токен, полученный через Полигон Яндекса: ')


class YaDisk:
    '''Метод загружает по ссылкам фотографии на Яндекс.Диск'''

    def __init__(self, ya_token, name, last_name, file_name):
        self.token = ya_token
        self.name = name
        self.last_name = last_name
        self.file_name = file_name
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'OAuth {self.token}'}

    def create_folder(self):
        # Создаем общую папку на Яндекс.Диске для загрузки фотографий из ВКонтакте,
        # затем, в этой папке создаём именованные папки под каждый профиль.
        print('Создаём папки на Яндекс.Диске...')
        # запрос для создания папки на Я.Диске для фотографий
        create_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=%2FVK_Photos'
        # запрос для создания папки по имени и фамилии профиля
        create_folder_profile_url = f'https://cloud-api.yandex.net/v1/disk/resources?path=%2FVK_Photos%2F{self.name}_{self.last_name}'
        response_create_url = requests.put(create_url, headers=self.headers)
        if response_create_url.status_code == 201:
            response_create_folder_profile_url = requests.put(create_folder_profile_url, headers=self.headers)
            if response_create_folder_profile_url.status_code == 201:
                return 'Успешно!'
            else:
                return f'Ошибка! Код ошибки: {response_create_folder_profile_url.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'
        elif response_create_url.status_code == 409:
            response_create_folder_profile_url = requests.put(create_folder_profile_url, headers=self.headers)
            if response_create_folder_profile_url.status_code == 201:
                return 'Успешно!'
            elif response_create_folder_profile_url.status_code == 409:
                return 'Папка уже существует.'
            else:
                return f'Ошибка! Код ошибки: {response_create_folder_profile_url.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'
        else:
            return f'Ошибка! Код ошибки: {response_create_url.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'

    def uploader(self):
        # Загружаем фотографии в папку
        print('Скачиваем фотографии с профиля и загружаем на Яндекс.Диск')
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        what_to_upload = [i for i, x in VK.links]
        lst = list(zip(what_to_upload, self.file_name))
        for item in lst:
            where_to_upload = f'VK_Photos/{self.name}_{self.last_name}'
            params = {'url': f'{item[0]}', 'path': f'{where_to_upload}/{item[1]}.jpeg', 'disable_redirects': 'false'}
            person_response = requests.post(url, headers=self.headers, params=params)
        if person_response.status_code == 202:
            return 'Успешно! Проверьте в Яндекс.Диске папку "VK_Photos"'
        else:
            f'Ошибка! Код ошибки: {person_response.status_code}\nПерейдите по ссылке, чтобы узнать причину: https://yandex.ru/support/webmaster/error-dictionary/http-codes.html#redirect-3xx'


YaDisk_info = YaDisk(ya_token,
                     VK.name_user,
                     VK.last_name_user,
                     VK.file_name)
ready_create_folder = YaDisk_info.create_folder()
ready_to_upload = YaDisk_info.uploader()
