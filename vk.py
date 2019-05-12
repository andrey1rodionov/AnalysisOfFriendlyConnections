import settings
import vk_api

# авторизация Вк
vk = vk_api.VkApi(login=settings.login, password=settings.password)
vk.auth()


class Parser:
    def deep_friends(self=0, depth=0):
        # информация о текущем пользователе
        if not self:
            person = vk.method('users.get')
            self = person[0]['id']
        else:
            person = vk.method('users.get', {'user_ids': self})

        person_name = person[0]['first_name']
        person_last_name = person[0]['last_name']
        person_id = str(person[0]['id'])

        # Получаем список друзей текущего пользователя
        friends = vk.method('friends.get', {'user_id': self})

        # Получаем информацию о друзьях текущего пользователя
        friends_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in friends['items']])})

        f = open('friends.list', 'a', encoding='utf-8')
        for friend in friends_info:
            friend_name = friend['first_name']
            friend_last_name = friend['last_name']
            friend_id = str(friend['id'])
            node = '{}/{}/{}:{}/{}/{}:'.format(person_name,
                                               person_last_name,
                                               person_id,
                                               friend_name,
                                               friend_last_name,
                                               friend_id) + '{}\n'
            f.write(node)
        f.close()

        # Если глубина не равна 0 - вызываем функцию для всех друзей текущего пользователя
        if depth == 0:
            return
        else:
            for friend in friends['items']:
                try:
                    Parser.deep_friends(friend, depth - 1)
                except:
                    print('Cant get friends of id ' + str(friend))

    def mutual_friends_with_colors(self=0):
        # Информация о текущем пользователе
        if not self:
            person = vk.method('users.get')
            self = person[0]['id']
        else:
            person = vk.method('users.get', {'user_ids': self})

        person_name = person[0]['first_name']
        person_last_name = person[0]['last_name']
        person_id = str(person[0]['id'])

        # Получаем список друзей текущего пользователя
        friends = vk.method('friends.get', {'user_id': self})

        # Получаем информацию о друзьях текущего пользователя
        friends_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in friends['items']])})

        # Составляем словарь "популярности"
        powers = {}
        for friend in friends['items']:
            try:
                mutual = vk.method('friends.getMutual', {'source_uid': person_id, 'target_uid': friend})
                powers[str(friend)] = {'count': len(mutual), 'items': mutual}
            except:
                powers[str(friend)] = {'count': 0, 'items': []}

        f = open('friends.list', 'w', encoding='utf-8')
        for friend in friends_info:
            friend_name = friend['first_name']
            friend_last_name = friend['last_name']
            friend_id = str(friend['id'])
            node = '{}/{}/{}/{}:{}/{}/{}/{}:'.format(person_name,
                                                     person_last_name,
                                                     person_id, 0,
                                                     friend_name,
                                                     friend_last_name,
                                                     friend_id,
                                                     powers[friend_id]['count']) + '{}\n'
            f.write(node)

            # Получаем информацию о связях текущего друга
            mutual = powers[friend_id]['items']
            if mutual:
                mutual_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in mutual])})
                for mutual in mutual_info:
                    mutual_name = mutual['first_name']
                    mutual_last_name = mutual['last_name']
                    mutual_id = str(mutual['id'])
                    node = '{}/{}/{}/{}:{}/{}/{}/{}:'.format(friend_name,
                                                             friend_last_name,
                                                             friend_id,
                                                             powers[friend_id]['count'],
                                                             mutual_name,
                                                             mutual_last_name,
                                                             mutual_id,
                                                             powers[mutual_id]['count']) + '{}\n'
                    f.write(node)
        f.close()

        maximum = 0
        for i in powers:
            if powers[i]['count'] > maximum:
                maximum = powers[i]['count']
        return maximum

    def mutual_friends(self=0):
        # Информация о текущем пользователе
        if not self:
            person = vk.method('users.get')
            self = person[0]['id']
        else:
            person = vk.method('users.get', {'user_ids': self})

        person_name = person[0]['first_name']
        person_last_name = person[0]['last_name']
        person_id = str(person[0]['id'])

        # Получаем список друзей текущего пользователя
        friends = vk.method('friends.get', {'user_id': self})

        # Получаем информацию о друзьях текущего пользователя
        friends_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in friends['items']])})

        f = open('friends.list', 'w ', encoding='utf-8')
        for friend in friends_info:
            friend_name = friend['first_name']
            friend_last_name = friend['last_name']
            friend_id = str(friend['id'])
            node = '{}/{}/{}:{}/{}/{}:'.format(person_name,
                                               person_last_name,
                                               person_id,
                                               friend_name,
                                               friend_last_name,
                                               friend_id) + '{}\n'
            f.write(node)

            try:
                # Получаем информацию о связях текущего друга
                mutual = vk.method('friends.getMutual', {'source_uid': person_id, 'target_uid': friend['id']})
                mutual_info = vk.method('users.get', {'user_ids': ','.join([str(i) for i in mutual])})
                for mutual in mutual_info:
                    mutual_name = mutual['first_name']
                    mutual_last_name = mutual['last_name']
                    mutual_id = str(mutual['id'])
                    node = '{}/{}/{}:{}/{}/{}:'.format(friend_name,
                                                       friend_last_name,
                                                       friend_id,
                                                       mutual_name,
                                                       mutual_last_name,
                                                       mutual_id) + '{}\n'
                    f.write(node)
            except:
                print('Cant get mutual of id ' + str(person_id), ' with id ' + str(friend['id']))
        f.close()
