import random

PEOPLE = ["Itai", "Hudefa", "Lakerda", "Kleiner"]
MSGS = ["You are shamen", "You've got a leak", "How are you doing, cannon?", "NANI"]
MSG_HEADER = 'SRC|DST|MSG\n'
SQN_HEADER = 'SQN\n'

sqn = -1

def get_header(mode):
    if mode == 'MSG':
        return MSG_HEADER
    elif mode == 'SQN':
        return SQN_HEADER
    else:
        raise Exception('Unknown mode')

def gen_record(mode):
    if mode == 'MSG':
        people = PEOPLE[:]
        src = people[random.randint(0, len(people) - 1)]
        people.remove(src)
        dst = people[random.randint(0, len(people) - 1)]
        msg = MSGS[random.randint(0, len(MSGS) - 1)]

        record = src + '|' + dst + '|' + msg + '\n'
        return record
    elif mode == 'SQN':
        global sqn
        sqn += 1
        return str(sqn) + '\n'
