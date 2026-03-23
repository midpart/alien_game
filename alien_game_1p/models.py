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

from alien_game_1p.alienProductExchange import AlienProductExchange
from common import buttons_time_track, time_interval_track

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'alien_game_1p'
    players_per_group = None
    num_rounds = 4
    conversion_rate = 0.002


class Subsession(BaseSubsession):
    def creating_session(self):
        self.initialize()

    def initialize(self):
        for p in self.get_players():

            if "data" not in p.participant.vars.keys():
                p.participant.vars["data"] = {
                    "is_training": {},
                    "selections": {},
                    "selections_id": {},
                    "selections_payoff": {},
                    "p1_payoffs": {},
                    "p2_payoffs": {},
                    "num_clicks": {},
                    "module1_change": {},
                    "module2_change": {},
                    "search_distance": {},
                    "active_search": {},
                    "alien_market": {},
                    "trial_number": {},
                    "payoff": {},
                    "best_selection": {},
                    "best_payoff": {},
                    "alien_randomized_order": {},
                    "results": {},

                }

            # initialize your fields or perform any setup here
            indexes_to_shuffle = list(range(1, Constants.num_rounds + 1))
            # create array of indexes, the first is fixed and the others are randomized
            randomized_order = random.sample(indexes_to_shuffle, len(indexes_to_shuffle))
            p.participant.vars["data"]['alien_randomized_order'][self.round_number - 1] = randomized_order

            if self.round_number == 1 and not 'round_1_initiated_alien' in p.participant.vars["data"].keys():
                p.participant.vars["data"]["is_training"][self.round_number - 1] = True
                p.participant.vars["data"]["selections"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["selections_id"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["selections_payoff"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["p1_payoffs"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["p2_payoffs"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["num_clicks"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["module1_change"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["module2_change"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["search_distance"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["active_search"][self.round_number - 1] = list(range(1, Constants.num_rounds + 1))
                p.participant.vars["data"]["results"][self.round_number - 1] = [[[""] for j in range(2)] for i in range(0, self.session.vars["training_trials"]-1)]
                # self.session.vars[g_id]['comprehension_trials'][self.round_number - 1] = 1
                p.participant.vars["data"]['round_1_initiated_alien'] = True
                self.initialize_common(p)
            else:
                p.participant.vars["data"]["is_training"][self.round_number - 1] = False
                p.participant.vars["data"]["results"][self.round_number - 1] = [[[""] for j in range(2)] for i in range(0, self.session.vars["max_trials"]-1)]
                self.initialize_common(p)

            # print(p.participant.vars["data"])

    def initialize_common(self, player):
        randomized_order = player.participant.vars["data"]['alien_randomized_order'][self.round_number - 1]
        player.participant.vars["data"]["alien_market"][self.round_number - 1] = AlienProductExchange(self.session.config['modules'], 1, self.session.config['number_of_pictures'])
        player.presentation_order = randomized_order[self.round_number - 1]
        player.participant.vars["data"]['trial_number'][self.round_number - 1] = 1
        player.participant.vars["data"]["selections"][self.round_number - 1] = []
        player.participant.vars["data"]["selections_id"][self.round_number - 1] = []
        player.participant.vars["data"]["search_distance"][self.round_number - 1] = []
        player.participant.vars["data"]["active_search"][self.round_number - 1] = []
        player.participant.vars["data"]["selections_payoff"][self.round_number - 1] = []
        player.participant.vars["data"]["p1_payoffs"][self.round_number - 1] = []
        player.participant.vars["data"]["p2_payoffs"][self.round_number - 1] = []
        player.participant.vars["data"]["num_clicks"][self.round_number - 1] = []
        player.participant.vars["data"]["module1_change"][self.round_number - 1] = []
        player.participant.vars["data"]["module2_change"][self.round_number - 1] = []
        player.participant.vars["data"]['payoff'][self.round_number - 1] = 0.0
        player.participant.vars["data"]["best_selection"][self.round_number - 1] = 0
        player.participant.vars["data"]["best_payoff"][self.round_number - 1] = 0
        player.trial_0_activation()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    total_time_spent = models.StringField(initial="0")
    submission_times = models.StringField(initial="0")
    click_time_list = models.StringField(initial="")

    nk_landscape_list = models.StringField()
    landscape_id_list = models.StringField()
    landscape_payoff_list = models.StringField()
    search_distance_list = models.StringField()
    active_search_list = models.StringField()
    num_clicks_list = models.StringField()
    module1_change_list = models.StringField()
    module2_change_list = models.StringField()

    presentation_order = models.IntegerField()

    def add_player_selections(self, player):
        player.nk_landscape_list = str(player.participant.vars["data"]["selections"][player.round_number - 1])
        player.landscape_id_list = str(player.participant.vars["data"]["selections_id"][player.round_number - 1])
        player.landscape_payoff_list = str(player.participant.vars["data"]["selections_payoff"][player.round_number - 1])
        player.search_distance_list = str(player.participant.vars["data"]["search_distance"][player.round_number - 1])
        player.active_search_list = str(player.participant.vars["data"]["active_search"][player.round_number - 1])
        player.num_clicks_list = str(player.participant.vars["data"]["num_clicks"][player.round_number - 1])
        player.module1_change_list = str(player.participant.vars["data"]["module1_change"][player.round_number - 1])
        player.module2_change_list = str(player.participant.vars["data"]["module2_change"][player.round_number - 1])

    def set_alien_selection_result(self, bitstring):
        values = self.participant.vars["data"]["alien_market"][self.round_number - 1].get_new_lookup_values(bitstring)
        self.add_new_selections(values)

    def trial_0_activation(self):
        alien = self.participant.vars["data"]["alien_market"][self.round_number - 1]
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
            self.session.vars[g_id]["best_selection"][self.round_number - 1] = self.session.vars[g_id]['trial_number'][
                                                                                   self.round_number - 1] - 1

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
        if len(self.participant.vars["data"]["selections"][self.round_number - 1]) > 0:
            active_search = 0 if self.participant.vars["data"]["selections"][self.round_number - 1][-1] == values['bitstring'] else 1
            self.participant.vars["data"]["active_search"][self.round_number - 1].append(active_search)
        else:
            self.participant.vars["data"]["active_search"][self.round_number - 1].append(0)

        self.participant.vars["data"]["selections"][self.round_number - 1].append(values['bitstring'])
        self.participant.vars["data"]["selections_id"][self.round_number - 1].append(int(values['bitstring'], 2) + 1)
        self.participant.vars["data"]["selections_payoff"][self.round_number - 1].append("{:.2f}".format(float(values['fitness'])))
        self.participant.vars["data"]["p1_payoffs"][self.round_number - 1].append("{:.2f}".format(float(values['M1'])))

        if self.session.config['modules'] == 2:
            self.participant.vars["data"]["p2_payoffs"][self.round_number - 1].append("{:.2f}".format(float(values['M2'])))

        if float(values['fitness']) >= self.participant.vars["data"]["best_payoff"][self.round_number - 1]:
            self.participant.vars["data"]["best_payoff"][self.round_number - 1] = float(values['fitness'])
            self.participant.vars["data"]["best_selection"][self.round_number - 1] = self.participant.vars["data"]['trial_number'][self.round_number - 1] - 1

        if self.participant.vars["data"]["search_distance"][self.round_number - 1] == 0:
            self.participant.vars["data"]["search_distance"][self.round_number - 1].append(0)
        else:
            best_id = self.participant.vars["data"]["best_selection"][self.round_number - 1]
            previous = self.participant.vars["data"]["selections"][self.round_number - 1][best_id]
            actual = values['bitstring']
            differences = sum(1 for a, b in zip(previous, actual) if a != b)
            self.participant.vars["data"]["search_distance"][self.round_number - 1].append(differences)

        self.participant.vars["data"]['trial_number'][self.round_number - 1] += 1
        self.add_payoff(float(values['fitness']))

    def add_payoff(self, payoff):
        self.participant.vars["data"]['payoff'][self.round_number - 1] += payoff

    def get_num_images(self):
        return len(self.participant.vars["data"]["alien_market"][self.round_number - 1].alien_symbols)

    def set_payoff_in_points(self):
        self.payoff = c(self.participant.vars["data"]['payoff'][self.round_number - 1])

    # Find the upper and lower index bounds for which pictures the player can interact with
    def calculate_image_bounds(self):
        num_images = self.get_num_images()
        num_players = len(self.group.get_players())

        lower_bound = int(((num_images/num_players) * (self.id_in_group - 1)))
        upper_bound = int((num_images/num_players) * self.id_in_group)

        return lower_bound, upper_bound

    def has_change(self, string1, string2):
        changes = 0
        for i in range(len(string1)):
            if string1[i] != string2[i]:
                changes += 1
        
        changes_bool = False
        if changes > 0:
            changes_bool = True
        
        return changes_bool

    def live_selection(self, data):
        data = json.loads(data)
        result_long = data["result"]
        results = result_long.split("_")
        result = results[0]
        num_clicks = ""
        module1_change = ""
        module2_change = ""
        if len(results) >= 2:
            num_clicks = results[1]
        if len(results) >= 3:
            module1_change = results[2]
        if len(results) >= 4:
            module2_change = results[3]

        self.participant.vars["data"]["num_clicks"][self.round_number - 1].append(num_clicks)
        self.participant.vars["data"]["module1_change"][self.round_number - 1].append(module1_change)
        self.participant.vars["data"]["module2_change"][self.round_number - 1].append(module2_change)

        self.participant.vars["data"]['results'][self.round_number - 1][self.participant.vars["data"]["trial_number"][self.round_number - 1] - 2][0] = result[:5]
        self.participant.vars["data"]['results'][self.round_number - 1][self.participant.vars["data"]["trial_number"][self.round_number - 1] - 2][1] = result[5:]

        if self.participant.vars["data"]["trial_number"][self.round_number - 1] > self.session.vars["max_trials"]:
            return

        buttons_time_track(data["click_time"], self)
        time_interval_track(float(data["click_time"]), self)

        values = self.participant.vars["data"]['results'][self.round_number - 1][self.participant.vars["data"]["trial_number"][self.round_number - 1] - 2]
        bitstring = str(values[0] + values[1])

        self.set_alien_selection_result(bitstring)
        if self.round_number == 1:
            if self.participant.vars["data"]["trial_number"][self.round_number - 1] == self.session.vars["training_trials"] + 1:
                self.add_player_selections(self)
        elif self.participant.vars["data"]["trial_number"][self.round_number - 1] == self.session.vars["max_trials"] + 1:
            self.add_player_selections(self)

        enable_next = True

        return_data = dict(
                row=self.participant.vars["data"]['trial_number'][self.round_number - 1] - 1,
                joint_payoff=self.participant.vars["data"]["selections_payoff"][self.round_number - 1][-1],
                p1_payoff=self.participant.vars["data"]["p1_payoffs"][self.round_number - 1][-1],
                presentation_order=self.presentation_order,
                selection=bitstring,
                enable_next=enable_next
            )

        if self.session.config['modules'] == 2:
            return_data['p2_payoff'] = self.participant.vars["data"]["p2_payoffs"][self.round_number - 1][-1],

        return {self.id_in_group:
            return_data,
        }
