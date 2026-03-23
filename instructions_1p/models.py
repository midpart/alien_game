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


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'instructions_1p'
    players_per_group = None
    num_rounds = 1
    comprehension_trials = 6  # How many times can the player try retry the comprehension


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["max_trials"] = 11  # 10 trials + 1 preset
        self.session.vars["training_trials"] = 4  # 3 trials + 1 preset
        self.session.vars["number_of_pictures"] = self.session.config["number_of_pictures"]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comp_creature_buying = models.StringField(
        label="1)	What creature is buying the pictures?",
        initial=""
    )

    comp_symbol_changes = models.IntegerField(
        label="2)	How many symbols can you, without your teammate, change from one trial to the next?",
        choices=[[1, 'a) 0-5'], [2, 'b) 1'], [3, 'c) 1-5']]
    )

    comp_symbols_buy = models.IntegerField(
        label="3) How many pictures is the creature willing to buy?",
        choices=[[1, 'a) The alien buys all pictures and pays a random price'],
                 [2, 'b) The alien buys one picture. It is the one with the highest price'],
                 [3, 'c) The alien buys all pictures and pays the accumulated price']]
    )

    comprehension_times = models.IntegerField(initial=1)
    instructions_completion_time = models.StringField(initial="0")
    comprehension_completion_time = models.StringField(initial="0")
    start_time = models.StringField(initial="0")
    last_recorded_time = models.StringField(initial="0")

    def is_comprehension_valid(self):
        comp_creature_buying = self.comp_creature_buying or ''
        # if comp_creature_buying.upper().find(
        #         'ALIEN') == -1 or self.comp_symbol_changes != 1 or self.comp_symbols_buy != 3:
        if comp_creature_buying.upper().find(
                'ALIEN') == -1 or self.comp_symbol_changes != 2 or self.comp_symbols_buy != 3:
            self.reset_comprehension_fields()
            self.participant.vars['comprehension_valid'] = False
            return False

        self.participant.vars['comprehension_valid'] = True
        return True

    def reset_comprehension_fields(self):
        self.comp_creature_buying = ""
        self.comp_symbol_changes = 0
        self.comp_symbols_buy = 0

    def comp_symbol_changes_choices(self):
        value = int(self.session.config["number_of_pictures"] / self.session.config["modules"])
        choices=[[1, f'a) 0-{value}'], [2, 'b) 1'], [3, f'c) 1-{value}']]
        return choices
