import random
import json

from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from alien_game_4p.alienProductExchange import AlienProductExchange
from common import buttons_time_track, time_interval_track

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'alien_game_4p'
    players_per_group = 4
    num_rounds = 4
    conversion_rate = 0.002


class Subsession(BaseSubsession):
    def creating_session(self):
        self.initialize()

    def initialize(self):
        for group in self.get_groups():
            g_id = group.id_in_subsession

            if g_id not in self.session.vars.keys():
                self.session.vars[g_id] = {
                    "is_training": {},
                    "selections": {},
                    "selections_id": {},
                    "selections_payoff": {},
                    #"p1_payoffs": {},
                    #"p2_payoffs": {},
                    "search_distance": {},
                    "active_search": {},
                    "alien_market": {},
                    "trial_number": {},
                    "payoff": {},
                    "best_selection": {},
                    "best_payoff": {},
                    "alien_randomized_order": {},
                    "submit_count": {},
                    "results": {},
                    "chat": {}
                }

                for p in group.get_players():
                    self.session.vars[g_id][f'p{p.id_in_group}_payoffs'] = {}

            # initialize your fields or perform any setup here
            indexes_to_shuffle = list(range(1, Constants.num_rounds + 1))
            # create array of indexes, the first is fixed and the others are randomized
            randomized_order = random.sample(indexes_to_shuffle, len(indexes_to_shuffle))
            self.session.vars[g_id]['alien_randomized_order'][self.round_number - 1] = randomized_order

            if self.round_number == 1 and not 'round_1_initiated_alien' in self.session.vars[g_id].keys():
                self.session.vars[g_id]["is_training"][self.round_number - 1] = True
                self.session.vars[g_id]["selections"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                self.session.vars[g_id]["selections_id"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                self.session.vars[g_id]["selections_payoff"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                # self.session.vars[g_id]["p1_payoffs"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                # self.session.vars[g_id]["p2_payoffs"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))

                for p in group.get_players():
                    self.session.vars[g_id][f'p{p.id_in_group}_payoffs'][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))

                self.session.vars[g_id]["search_distance"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                self.session.vars[g_id]["active_search"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                self.session.vars[g_id]["submit_count"][self.round_number - 1] = [0 for i in range(0, self.session.vars["training_trials"]-1)]
                self.session.vars[g_id]["results"][self.round_number - 1] = [[[""] for j in range(0, len(self.get_players()))] for i in range(0, self.session.vars["training_trials"]-1)]
                # self.session.vars[g_id]['comprehension_trials'][self.round_number - 1] = 1
                self.session.vars[g_id]['round_1_initiated_alien'] = True
                self.initialize_common(group)
            else:
                self.session.vars[g_id]["is_training"][self.round_number - 1] = False
                self.session.vars[g_id]["submit_count"][self.round_number - 1] = [0 for i in range(0, self.session.vars["max_trials"]-1)]
                self.session.vars[g_id]["results"][self.round_number - 1] = [[[""] for j in range(0, len(self.get_players()))] for i in range(0, self.session.vars["max_trials"]-1)]
                self.initialize_common(group)

    def initialize_common(self, group):
        g_id = group.id_in_subsession
        randomized_order = self.session.vars[g_id]['alien_randomized_order'][self.round_number - 1]
        self.session.vars[g_id]["alien_market"][self.round_number - 1] = AlienProductExchange(self.session.config['modules'], len(self.get_players()), self.session.config['number_of_pictures'], Constants.num_rounds, self.round_number)
        group.presentation_order = randomized_order[self.round_number - 1]
        self.session.vars[g_id]['trial_number'][self.round_number - 1] = 1
        self.session.vars[g_id]["selections"][self.round_number - 1] = []
        self.session.vars[g_id]["selections_id"][self.round_number - 1] = []
        self.session.vars[g_id]["search_distance"][self.round_number - 1] = []
        self.session.vars[g_id]["active_search"][self.round_number - 1] = []
        self.session.vars[g_id]["selections_payoff"][self.round_number - 1] = []
        # self.session.vars[g_id]["p1_payoffs"][self.round_number - 1] = []
        # self.session.vars[g_id]["p2_payoffs"][self.round_number - 1] = []
        self.session.vars[g_id]['payoff'][self.round_number - 1] = 0.0
        self.session.vars[g_id]["best_selection"][self.round_number - 1] = 0
        self.session.vars[g_id]["best_payoff"][self.round_number - 1] = 0

        for p in group.get_players():
            self.session.vars[g_id][f"p{p.id_in_group}_payoffs"][self.round_number - 1] = []

        group.trial_0_activation()


class Group(BaseGroup):
    presentation_order = models.IntegerField()
    Chat = models.StringField(initial="")

    def add_player_selections(self):
        g_id = self.id_in_subsession
        for player in self.get_players():
            player.nk_landscape_list = str(self.session.vars[g_id]["selections"][player.round_number - 1])
            player.landscape_id_list = str(self.session.vars[g_id]["selections_id"][player.round_number - 1])
            player.landscape_payoff_list = str(self.session.vars[g_id]["selections_payoff"][player.round_number - 1])
            player.search_distance_list = str(self.session.vars[g_id]["search_distance"][player.round_number - 1])
            player.active_search_list = str(self.session.vars[g_id]["active_search"][player.round_number - 1])

    def set_alien_selection_result(self, bitstring):
        values = self.session.vars[self.id_in_subsession]["alien_market"][self.round_number - 1].get_new_lookup_values(bitstring)
        self.add_new_selections(values)
        #payoff = self.session.vars[self.id_in_subsession]["alien_market"][self.round_number - 1].get_lookup_value(bit_string, self.round_number)
        #self.add_selection(bit_string, payoff)

    def trial_0_activation(self):
        alien = self.session.vars[self.id_in_subsession]["alien_market"][self.round_number - 1]
        values = alien.get_new_smallest_performance()
        self.add_new_selections(values)

    def add_selection(self, bit_string, payoff):
        g_id = self.id_in_subsession
        if len(self.session.vars[g_id]["selections"][self.round_number - 1]) > 0:
            active_search = 0 if self.session.vars[g_id]["selections"][self.round_number - 1][-1] == bit_string else 1
            self.session.vars[g_id]["active_search"][self.round_number - 1].append(active_search)
        else:
            self.session.vars[g_id]["active_search"][self.round_number - 1].append(0)

        self.session.vars[g_id]["selections"][self.round_number - 1].append(bit_string)
        self.session.vars[g_id]["selections_id"][self.round_number - 1].append(int(bit_string, 2) + 1)
        self.session.vars[g_id]["selections_payoff"][self.round_number - 1].append("{:.2f}".format(payoff))

        # changes best performant selection
        if payoff >= self.session.vars[g_id]["best_payoff"][self.round_number - 1]:
            self.session.vars[g_id]["best_payoff"][self.round_number - 1] = payoff
            self.session.vars[g_id]["best_selection"][self.round_number - 1] = self.session.vars[g_id]['trial_number'][self.round_number - 1] - 1

        # Number of bits that changed respect the best performant previous selection
        if len(self.session.vars[g_id]["search_distance"][self.round_number - 1]) == 0:
            self.session.vars[g_id]["search_distance"][self.round_number - 1].append(0)
        else:
            best_id = self.session.vars[g_id]["best_selection"][self.round_number - 1]
            previous = self.session.vars[g_id]["selections"][self.round_number - 1][best_id]
            actual = bit_string
            differences = sum(1 for a, b in zip(previous, actual) if a != b)
            self.session.vars[g_id]["search_distance"][self.round_number - 1].append(differences)

        self.session.vars[g_id]['trial_number'][self.round_number - 1] += 1
        self.add_payoff(payoff)

    def add_new_selections(self, values):
        g_id = self.id_in_subsession
        if len(self.session.vars[g_id]["selections"][self.round_number - 1]) > 0:
            active_search = 0 if self.session.vars[g_id]["selections"][self.round_number - 1][-1] == values['bitstring'] else 1
            self.session.vars[g_id]["active_search"][self.round_number - 1].append(active_search)
        else:
            self.session.vars[g_id]["active_search"][self.round_number - 1].append(0)

        self.session.vars[g_id]["selections"][self.round_number - 1].append(values['bitstring'])
        self.session.vars[g_id]["selections_id"][self.round_number - 1].append(int(values['bitstring'], 2) + 1)
        self.session.vars[g_id]["selections_payoff"][self.round_number - 1].append("{:.2f}".format(float(values['fitness'])))
        # self.session.vars[g_id]["p1_payoffs"][self.round_number - 1].append("{:.2f}".format(float(values['M1'])))
        # self.session.vars[g_id]["p2_payoffs"][self.round_number - 1].append("{:.2f}".format(float(values['M2'])))

        for p in self.get_players():
            self.session.vars[g_id][f"p{p.id_in_group}_payoffs"][self.round_number - 1].append("{:.2f}".format(float(values[f'M{p.id_in_group}'])))

        if float(values['fitness']) >= self.session.vars[g_id]["best_payoff"][self.round_number - 1]:
            self.session.vars[g_id]["best_payoff"][self.round_number - 1] = float(values['fitness'])
            self.session.vars[g_id]["best_selection"][self.round_number - 1] = self.session.vars[g_id]['trial_number'][self.round_number - 1] - 1

        if len(self.session.vars[g_id]["search_distance"][self.round_number - 1]) == 0:
            self.session.vars[g_id]["search_distance"][self.round_number - 1].append(0)
        else:
            best_id = self.session.vars[g_id]["best_selection"][self.round_number - 1]
            previous = self.session.vars[g_id]["selections"][self.round_number - 1][best_id]
            actual = values['bitstring']
            differences = sum(1 for a, b in zip(previous, actual) if a != b)
            self.session.vars[g_id]["search_distance"][self.round_number - 1].append(differences)

        self.session.vars[g_id]['trial_number'][self.round_number - 1] += 1
        self.add_payoff(float(values['fitness']))

    def add_payoff(self, payoff):
        self.session.vars[self.id_in_subsession]['payoff'][self.round_number - 1] += payoff

    def get_num_images(self):
        return self.session.config['number_of_pictures']


class Player(BasePlayer):
    total_time_spent = models.StringField(initial="0")
    submission_times = models.StringField(initial="0")
    click_time_list = models.StringField(initial="")

    nk_landscape_list = models.StringField()
    landscape_id_list = models.StringField()
    landscape_payoff_list = models.StringField()
    search_distance_list = models.StringField()
    active_search_list = models.StringField()

    def set_payoff_in_points(self):
        g_id = self.group.id_in_subsession
        self.payoff = c(self.session.vars[g_id]['payoff'][self.round_number - 1])

    # Find the upper and lower index bounds for which pictures the player can interact with
    def calculate_image_bounds(self):
        num_images = self.group.get_num_images()
        num_players = len(self.group.get_players())

        lower_bound = int(((num_images/num_players) * (self.id_in_group - 1)))
        upper_bound = int((num_images/num_players) * self.id_in_group)

        return lower_bound, upper_bound

    def live_selection(self, data):
        print(data)

        if 'buttonId' in data:
            return {0: dict(
                buttonId=data['buttonId'],
                playerOrigin=data['playerIdOrigin']
            )}

        if 'end_chat' in data:
            if data['end_chat'] == self.id_in_group:
                return {0: dict(
                    endChat=data['end_chat'],
                    playerOrigin=data['playerOrigin']
                )}
            return

        if 'join_chat' in data:
            if data['join_chat'] == self.id_in_group:
                return {0: dict(
                    joinChat=data['join_chat'],
                    playerOrigin=data['playerOrigin']
                )}
            return

        if 'chat' in data:
            print(data['chat'])

            trial = self.session.vars[self.group.id_in_subsession]['trial_number'][self.round_number - 1] - 1

            if self.round_number not in self.session.vars[self.group.id_in_subsession]['chat']:
                self.session.vars[self.group.id_in_subsession]['chat'][self.round_number] = {}

            if trial not in self.session.vars[self.group.id_in_subsession]['chat'][self.round_number]:
                self.session.vars[self.group.id_in_subsession]['chat'][self.round_number][trial] = ""

            self.session.vars[self.group.id_in_subsession]['chat'][self.round_number][trial] += data['chat']
            self.group.Chat = str(self.session.vars[self.group.id_in_subsession]['chat'][self.round_number])

            print(self.session.vars[self.group.id_in_subsession]['chat'])
            return

        data = json.loads(data)
        result = data["result"]
        g_id = self.group.id_in_subsession

        index = result['playerId']-1

        self.session.vars[g_id]['results'][self.round_number - 1][self.session.vars[g_id]["trial_number"][self.round_number - 1] - 2][index] = result['bitstring']

        self.session.vars[g_id]["submit_count"][self.round_number - 1][self.session.vars[g_id]["trial_number"][self.round_number - 1] - 2] += 1
        if self.session.vars[g_id]["submit_count"][self.round_number - 1][self.session.vars[g_id]["trial_number"][self.round_number - 1] - 2] < len(self.group.get_players()):
            return

        if self.session.vars[g_id]["trial_number"][self.round_number - 1] > self.session.vars["max_trials"]:
            return

        buttons_time_track(data["click_time"], self)
        time_interval_track(float(data["click_time"]), self)

        values = self.session.vars[g_id]['results'][self.round_number - 1][self.session.vars[g_id]["trial_number"][self.round_number - 1] - 2]
        bitstring = ""

        for p in self.group.get_players():
            bitstring += values[p.id_in_group - 1]

        self.group.set_alien_selection_result(bitstring)
        if self.round_number == 1:
            if self.session.vars[g_id]["trial_number"][self.round_number - 1] == self.session.vars["training_trials"] + 1:
                self.group.add_player_selections()
        elif self.session.vars[g_id]["trial_number"][self.round_number - 1] == self.session.vars["max_trials"] + 1:
            self.group.add_player_selections()

        enable_next = True

        payoffs = []

        for p in self.group.get_players():
            payoffs.append(self.session.vars[g_id][f"p{p.id_in_group}_payoffs"][self.round_number - 1][-1])

        print(bitstring)

        return {0:
            dict(
                row=self.session.vars[g_id]['trial_number'][self.round_number - 1] - 1,
                joint_payoff=self.session.vars[g_id]["selections_payoff"][self.round_number - 1][-1],
                payoffs=payoffs,
                presentation_order=self.group.presentation_order,
                selection=bitstring,
                enable_next=enable_next
            ),
        }
