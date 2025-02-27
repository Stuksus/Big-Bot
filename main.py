import random
import vk_api
import requests
import traceback


def write_msg(session, user_id, message, repost, attachment='0'):  # Write message to user
    rand = random.randint(-9223372036854775807, 9223372036854775807)
    if repost:
        session.method('messages.send',
                       {'peer_id': user_id, 'random_id': rand, 'message': str(message), 'attachment': str(attachment)})
    else:
        session.method('messages.send', {'peer_id': user_id, 'random_id': rand, 'message': str(message)})


def auth(token="token' #need token
         scope="manage"):  # Auth like group
    return vk_api.VkApi(token=token, scope=scope)


def get_long_loll(session, id_group=191239236):  # create or update LongPoll server
    return session.method("groups.getLongPollServer", {"group_id": id_group})


def get_members_of_group(session, group_id):
    return session.method("groups.getMembers", {"group_id": group_id})


def get_last_post(session, group_id):
    return session.method('wall.get', {"owner_id": group_id})


def up(poll):
    response = requests.get(poll["server"] + "?act=a_check&key=" + poll['key'] + "&ts=" + poll[
        'ts'] + "&wait=25").json()
    if str(response).find('failed') < 0:
        update = response['updates']
        return response, update
    return response, []


admin_ids = [163298402, 344128222, 170470556, 96140795, 221060898, 363721185]
starter_message = []
while True:
    try:
        vk = auth()
        long_poll = get_long_loll(vk)
        while True:
            res, updates = up(long_poll)
            if updates and updates[0]['type'] == 'message_new':
                if not (updates[0]['object']['from_id'] in starter_message):
                    write_msg(vk, updates[0]['object']['from_id'],
                              "Свадьба пела и гармонь играла! Рады, что ты с нами!", False)
                    starter_message.append(updates[0]['object']['from_id'])
                if updates[0]['object']['from_id'] in admin_ids:
                    from_id = updates[0]['object']['from_id']
                    if updates[0]['object']['attachments']:
                        if updates[0]['object']['attachments'][0]['type'] == 'wall':
                            write_msg(vk, from_id, "Хей, привет, начинаю обработку", False)
                            if updates[0]['object']['attachments'][0]['wall']['from_id'] == -191239236:
                                id_post = updates[0]['object']['attachments'][0]['wall']['id']
                                total = 'wall-191239236_' + str(id_post)
                                write_msg(vk, from_id, 'Отправляю', False)
                                ids = get_members_of_group(vk, 191239236)['items']
                                for i in ids:
                                    try:
                                        write_msg(vk, i, '', True, total)
                                    except:
                                        error = traceback.format_exc()
                                        print('INNER ERROR', error)

                            else:
                                write_msg(vk, from_id, 'Фу, он не из нашей группы? Убери эту гадость! И попробуй снова',
                                          False)
                        else:
                            write_msg(vk, from_id, 'Это вообще пост? Попробуй снова', False)

            long_poll['ts'] = res['ts']
    except:
        var = traceback.format_exc()
        print(var)
