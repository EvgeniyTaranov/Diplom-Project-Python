import json
import VK

def get_create_json(date, links, name, second_name):
    # соединяем в единый список количество лайков по дате и типоразмер
    ready_lst = []
    size_lst = [size for url, size in links]
    lst = [[x, y] for x, y in (list(zip(date, size_lst)))]
    for item in lst:
        json_dict = {'file_name': item[0],
                     'size': item[1]}
        ready_lst.append(json_dict)
    with open(rf'JSON/{name}_{second_name}.json', 'w') as write_file:
        return json.dump(ready_lst, write_file)

json_file = get_create_json(VK.file_name,
                            VK.links,
                            VK.name_user,
                            VK.last_name_user)

print('Смотрите JSON-файлы в папке JSON')