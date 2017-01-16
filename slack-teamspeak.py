#!/usr/bin/env python3

import sys

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
    current_users = {client['client_database_id'] for client in clientlist.values() if client['client_type'] == '0'}
    new_users = current_users - last_users
    return sorted(client['client_nickname'] for client in clientlist.values() if client['client_database_id'] in new_users), current_users

if __name__ == '__main__':
    slack = slacker.Slacker(CONFIG['apiToken'])
    last_users = set()
    while True:
        new_users, last_users = update_users(last_users)
        if len(new_users) > 0:
            slack.chat.post_message(CONFIG.get('channel', '#teamspeak'), CONFIG.get('message', '{} joined').format(join(new_users)), as_user=True)
        time.sleep(CONFIG.get('checkInterval', 5))
