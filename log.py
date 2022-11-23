import logging
import requests
import VK
import YaDisk
import JSON_init

response = requests.get(url='https://api.vk.com/method/users.get',
                        params = {'access_token': VK.access_token,
                                  'user_id': VK.user_id,
                                  'v': '5.131'})

class ContextFilter(logging.Filter):
    ''' Фильтр, который записывает контекстную информацию в журнал.'''

    USER = VK.name_user + ' ' + VK.last_name_user
    ID = VK.user_id

    def filter(self, record):

        record.ip = (ContextFilter.ID)
        record.user = (ContextFilter.USER)
        return True

if __name__ == '__main__':
    levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    logging.basicConfig(handlers=[logging.FileHandler('LOGS/activeApp.log', 'w', 'utf-8')],
                        level=logging.DEBUG,
                        format='%(asctime)-15s %(name)-5s %(levelname)-8s Id: %(ip)-15s User: %(user)-8s %(message)s',
                        encoding='utf-8')

link = logging.getLogger('Ссылки     ')
authenticity = logging.getLogger('Подлинность')

filt = ContextFilter()
link.addFilter(filt)
authenticity.addFilter(filt)
     
if len(YaDisk.ya_token) == 39:
    link.info('Информация корректна')
    link.debug([i for i, q in VK.links])
else:
    link.error(f'Данные не верны. Проверьте формат переменных "ya_token" или "user_id"!')

if response.status_code == 200:
    authenticity.info('Информация доступна')
    authenticity.debug(response.json())
else:
    authenticity.error('Внимание! Ошибка доступа!', response.status_code)
    authenticity.critical(VK.__dict__)

JSON_init.get_create_json
 
print('Смотрите логи в файле "activeApp.log"')