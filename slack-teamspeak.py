#!/usr/bin/env python3

import sys

sys.path.append('/opt/py')

import basedir
import slacker
import time
import ts3

CONFIG = basedir.config_dirs('slack-teamspeak.json').json()

def join(sequence, *, word='and', default=None):
    sequence = [str(elt) for elt in sequence]
    if len(sequence) == 0:
        if default is None:
            raise IndexError('Tried to join empty sequence with no default')
        else:
            return str(default)
    elif len(sequence) == 1:
        return sequence[0]
    elif len(sequence) == 2:
        return '{} {} {}'.format(sequence[0], word, sequence[1])
    else:
        return ', '.join(sequence[:-1]) + ', {} {}'.format(word, sequence[-1])

def update_users(last_users):
    srv = ts3.TS3Server(CONFIG['hostname'], CONFIG.get('port', 10011), 1)
    srv.login(CONFIG.get('username', 'serveradmin'), CONFIG['password'])
    clientlist = srv.clientlist()
    current_users = {client['client_database_id']: client['client_nickname'] for client in clientlist.values() if client['client_type'] == '0'}
    new_users = sorted(current_users[client] for client in current_users if client not in last_users)
    former_users = sorted(last_users[client] for client in last_users if client not in current_users)
    return new_users, current_users, former_users

if __name__ == '__main__':
    slack = slacker.Slacker(CONFIG['apiToken'])
    last_users = {} # Now contains the id as key and the nickname as value
    while True:
        new_users, last_users, former_users = update_users(last_users)
        if len(new_users) > 0 and len(former_users) == 0:
            slack.chat.post_message(CONFIG.get('channel', '#teamspeak'), CONFIG.get('joinMessage', '{} joined. There are now {} active users.').format(join(new_users), len(last_users)), as_user=True)
        elif len(new_users) == 0 and len(former_users) > 0:
            slack.chat.post_message(CONFIG.get('channel', '#teamspeak'), CONFIG.get('leaveMessage', '{} left. There are now {} active users.').format(join(former_users), len(last_users)), as_user=True)
        elif len(new_users) > 0 and len(former_users) > 0:
            slack.chat.post_message(CONFIG.get('channel', '#teamspeak'), CONFIG.get('joinLeaveMessage', '{} left and {} joined. There are now {} active users.').format(join(former_users), join(new_users), len(last_users)), as_user=True)
        time.sleep(CONFIG.get('checkInterval', 5))
