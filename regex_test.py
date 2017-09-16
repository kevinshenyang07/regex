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
    "read my email"
    "read my sms message"
]
# Intent: “messaging”, action: “send/reply/query”, targetName: “facebook/slack/sms/email”
p1 = re.compile(r"(send|reply|read).*(facebook|slack|sms|email).*")


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
p2 = re.compile(r'(find|search).* a (.*) (on the|in|near|with) (.*)')


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
p3 = re.compile(r'(directions|get|direct|take).* to (.*)')


group4 = [
    "create event to buy milk at 6am next Monday",
    "create event meeting with John at 6 p.m tomorrow",
    "create event to call home tomorrow six p.m.",
    "what is on my calendar"
    "tell me my google calendar events"
]
# Intent: “calendarEvent”, action: “create/query”, eventName:”buy milk/meeting
# with john/call home”, eventTime: “6 am”, eventDate: “tomorrow”

p4 = re.compile(r'(create event) to |(.*) at (\w+[ ]?[ap].?m.?) (.*)|(.* calendar .*)')


if __name__ == '__main__':
    for sentence in group2:
        result = p2.match(sentence)
        print result.group()