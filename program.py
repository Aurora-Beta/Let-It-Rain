#!/usr/bin/python3

from bottle import route, run, static_file, request
from alexa import Alexa
import json

alexa = Alexa("Let It Rain")  # Setup a object for the Alexa class
response = alexa.response  # Use the Alexa response attribute to return responses
url = "https://deimos.bytekeeper.de/letitrain/rain_comp.ogg"
debug=True

# Returns Locale from intent
def get_locale():
    locale = request.json["request"]["locale"]
    return locale

# Create your Lambda handler
def lambda_handler(event, context):
    """Lambda Handler."""
    return alexa.route(event)


@alexa.launch
def launch():
    """Launch Function."""
    return response.audiostart(url, get_locale())

@alexa.intent("AMAZON.ResumeIntent")
def start_rain(session):
    """Gebe Regen zurück"""
    return response.audiostart(url, get_locale())

@alexa.intent("AMAZON.NextIntent")
def next_item(session):
    return response.audiostart(url, get_locale())

@alexa.intent("AMAZON.StopIntent")
def stop_rain(session):
    return response.audiostop(get_locale())

@alexa.intent("AMAZON.PauseIntent")
def pause_rain(session):
    """ Pause """
    return response.audiopause()
    #return response.audiostop()

@alexa.intent("sunsunsun")
def pause_rain(session):
    """ Beatles-Gag - Say: Here i come """
    return response.sunsunsun(get_locale)


@alexa.intent("AudioPlayer.PlaybackNearlyFinished")
def acknowlede(session):
    return ""
@alexa.intent("AudioPlayer.PlaybackStopped")
def acknowlede(session):
    return ""
@alexa.intent("AudioPlayer.PlaybackStarted")
def acknowlede(session):
    return ""

@alexa.intent("System.ExceptionEncountered")
def nix(session):
    return ""


@alexa.session_end
def close():
    """Close function."""
    return response.statement("Good bye")

@route('/letitrain/rain_comp.ogg')
def file():
    """Die Datei zurückgeben-"""
    return static_file("rain_comp.ogg", root='./')


@route('/letitrain', method='POST')
def letitrain():
    if debug:
        print("LOCALE:\t" + get_locale())
        print("REQUEST:\n")
        print(request.json)
        print("ANTWORT:\n")
        print(json.dumps(lambda_handler(request.json,2)))

    return json.dumps(lambda_handler(request.json,2))

#@route('/lassesregnen/')
#def lassessregnen():
#    with open("./regen.json") as d:
#        tests = json.load(d)
#        print(tests)

run(host='localhost', port=8080, debug=True)

