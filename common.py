import time
import json
import random
import copy
from json import JSONDecodeError

from otree.models import Participant
from otree.views.abstract import FormPageOrInGameWaitPage

FIRST_APP_NAME = "initial_app"

def update_participant_current_app(player, first_app, model):
    print('update participant current app called')
    if first_app == FIRST_APP_NAME:
        participant = Participant.objects.get(code=player.participant.code)
        participant._current_app_name = first_app
        participant._index_in_pages = 1
        participant.save()
        model._is_frozen = False
        model.set_attributes(model.participant)

def app_after_this_page_internal(upcoming_apps, player):
    print("App after this page called")
    participant = Participant.objects.get(code=player.participant.code)
    if participant._current_app_name == FIRST_APP_NAME:
        app_sequence = player.participant.vars['app_sequence']
        print("app_sequence:", app_sequence)
        if not len(app_sequence):
            print('upcomming_apps:', upcoming_apps)
            return upcoming_apps[-2]

        next_app = player.participant.vars['app_sequence'].pop(0)
        print('next app', next_app)
        return next_app

def buttons_time_track(unix_time, player):
    if player.click_time_list == '':
        player.click_time_list = "[]"

    click_times = json.loads(player.click_time_list)
    click_times.append(unix_time)
    player.click_time_list = json.dumps(click_times)

def time_interval_track(unix_time:float, player):
    """
    Stores time spent since last call of method in the data. 
    Player must have following StringFields:
    ```
    submission_times = models.StringField(initial='') 
    start_time = models.StringField() # Then set to equal str(time.time()) when the tracked task begins
    total_time_spent = models.StringField(initial="0")
    ```
    """
    if player.submission_times == '':
        player.submission_times = '[]'
    elif player.submission_times == '0':
        player.submission_times = '[0]'
    if player.click_time_list == '':
        player.click_time_list = "[]"

    submission_times = json.loads(player.submission_times)
    time = unix_time - float(player.participant.vars['start_time']) - float(player.total_time_spent)
    player.total_time_spent = str(float(player.total_time_spent) + time)
    submission_times.append(time)
    player.submission_times = json.dumps(submission_times)       

def reset_participant_vars(player):
    player.participant.vars = dict()