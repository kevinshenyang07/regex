# -*- coding:utf-8 -*-

import re

'''
Example regex:
"Play (Xbox|PS4)[ ]?(360|One|pro)?"
Example output:
“Play PS4pro”, -> (Intent: “playGame”, machine: “PS4”, machineType: “pro”)
'''

group1 = [
    "send a message",
    "send a text message on facebook messenger",
    "reply to last message on facebook messenger",
    "send text on slack",
    "read my email",
    "read my sms message"
]
# Intent: “messaging”, action: “send/reply/query”, targetName: “facebook/slack/sms/email”
p1 = re.compile(r"(send|reply|read).*(facebook|slack|sms|email|message).*")


group2 = [
    "find me a gas station on the way",
    "find me a gas station on the way home",
    "search gas station near stanford University",
    "find me a sushi place with over four star reviews",
    "search me a chinese restaurant in palo alto",
    "search a parking garage near 845 Market Street",
    "find me a nearest gas station",
]
# Intent: “poiSearch”, targetType: “gas station/restaurant/parking”,
# targetName: ”gas station / sushi place / chinese restaurant / parking lot / parking
# garage”, targetDestination: “way home / stanford university / palo alto / 845 market
# st”, targetReview: “over four star”
p2 = re.compile(
    r'(find|search)( me)?( a)?( nearest)? (\w+ \w+)( (on the|in|near|with) (.*))?')


group3 = [
    "directions to fish market in san francisco",
    "get me to 845 Market Street",
    "direct me to 845 Market Street",
    "take me to SFO",
    "take me to san francisco international airport",
    "route to San Francisco airport"
]
# Intent: “navigation”, targetName:”fish market/845 market st/sfo”,
# targetDestination: “ ”, targetReview: “ ”
p3 = re.compile(r'(directions|get|direct|take|route).* to (.*)')


group4 = [
    "create event to buy milk at 6am next Monday",
    "create event meeting with John at 6 p.m tomorrow",
    "create event to call home tomorrow six p.m.",
    "what is on my calendar",
    "tell me my google calendar events"
]
# Intent: “calendarEvent”, action: “create/query”, eventName:”buy milk/meeting
# with john/call home”, eventTime: “6 am”, eventDate: “tomorrow”
p4 = re.compile(
    r'(create event)( to)? (.*?) (tomorrow|next Monday)?[ ]?(at )?(\b\w+[ ]?[ap].?m.?)(.*)?|(.*calendar.*)')
# the 4th group need to be expanded to match more date options


def handle_group1(result):
    output = {'intent': 'messaging'}
    output['action'] = result.group(1)
    target_name = result.group(2)
    if target_name == 'message':
        target_name = 'sms'
    output['targetName'] =  target_name
    return output


def handle_group2(result):
    output = {'intent': 'poiSearch'}
    # set target type
    place = result.group(5)
    if 'gas station' in place:
        target_type = 'gas station'
    elif 'parking' in place:
        target_type = 'parking'
    else:  # need more domain knowledge to clarify here
        target_type = 'restaurant'
    output['targetType'] = target_type
    output['targetName'] = place
    # only one with value
    if result.group(6) == 'with':
        output['targetReview'] = result.group(8)
    else:
        output['targetDestination'] = result.group(8)
    return output


def handle_group3(result):
    output = {'intent': 'navigation'}
    output['targetName'] = result.group(2)
    return output
    

def handle_group4(result):
    output = {'intent': 'calendarEvent'}
    if result.group(8):
        output['action'] = 'query'
    else:
        output['action'] = 'create'
        output['eventName'] = result.group(3)
        if result.group(7):
            output['eventDate'] = result.group(7)
        else:
            output['eventDate'] = result.group(4)
        output['eventTime'] = result.group(6)
    return output


def test_sentence(s, patterns, methods):
    print 'Testing sentence: "{}"'.format(s)
    for i, pattern in patterns.iteritems():
        res = pattern.match(s)
        if res:
            output = methods[i](res)
            print 'Matching pattern {}, output is: {}'.format(i, output)
        else:
            print 'Not matching pattern {}'.format(i)
    print '\n'


def test_patterns():
    patterns = {
        1: p1, 2: p2, 3: p3, 4: p4
    }
    handle_methods = {
        1: handle_group1, 2: handle_group2,
        3: handle_group3, 4: handle_group4
    }
    for s in group1 + group2 + group3 + group4:
        test_sentence(s, patterns, handle_methods)


if __name__ == '__main__':
    test_patterns()
