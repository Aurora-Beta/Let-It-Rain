#!/usr/bin/python3

from bottle import route, run, static_file
from alexa import Alexa
import json

alexa = Alexa("Let it rain")  # Setup a object for the Alexa class
response = alexa.response  # Use the Alexa response attribute to return responses
url = "http://localhost:8080/rain.ogg"

# Create your Lambda handler
def lambda_handler(event, context):
    """Lambda Handler."""
    return alexa.route(event)


@alexa.launch
def launch():
    """Launch Function."""
    return response.statement("Welcome to hello world!")


@alexa.intent("GetHello", mapping={"person": "name"})
def get_hello(session, person):
    """Get Hello Intent."""
    if "previous" in session.keys():
        response.card("Welcome to Hello World!")
        return response.question("<p>Welcome</p><p>Hello to you {}".format(person))
    else:
        response.session.set_attribute("previous", True)
        return response.question("<p>Welcome</p><p>Hello AGAIN to you {}".format(person))

@alexa.intent("AMAZON.ResumeIntent")
def start_rain(session):
    """Gebe Regen zurück"""
    return response.audiostart(url)

#    if "previous" in session.keys():
#        response.card("Welcome to Hello World!")
#        return response.question("<p>Welcome</p><p>Hello to you {}".format(person))
#    else:
#        response.session.set_attribute("previous", True)
#        return response.question("<p>Welcome</p><p>Hello AGAIN to you {}".format(person))


@alexa.session_end
def close():
    """Close function."""
    return response.statement("Good bye")

@route('/letitrain/rain.ogg')
def file():
    """Die Datei zurückgeben-"""
    return static_file("rain.ogg", root='./')

@route('/lassesregnen')
def lassessregnen():
    with open("./regen.json") as d:
        tests = json.load(d)
        print(tests)


    print(
        json.dumps(
            lambda_handler(
                tests['launch'],
                2
            ),
        indent=2
        )
    )


    print(
        json.dumps(
            lambda_handler(
                tests['intent_rain'],
                2
            ),
            indent=2
        )
    )

    print(
        json.dumps(
            lambda_handler(
                tests['end'],
                2
            ),
            indent=2
        )
    )

# Serverpart
@route('/start')
def start():
    with open("./test_events.json") as d:
        tests = json.load(d)
        print(tests)

    print(
        json.dumps(
            lambda_handler(
                tests['launch'],
                2
            ),
        indent=2
        )
    )
    print(
        json.dumps(
            lambda_handler(
                tests['intent_hello'],
                2
            ),
            indent=2
        )
    )
    print(
        json.dumps(
            lambda_handler(
                tests['end'],
                2
            ),
            indent=2
        )
    )




run(host='localhost', port=8080, debug=True)
