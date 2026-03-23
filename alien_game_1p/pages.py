import time
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from alien_game_1p.alienProductExchange import AlienProductExchange

class AlienMarket(Page):
    form_model = 'player'
    live_method = 'live_selection'

    def is_displayed(self):
        self.player.total_time_spent = "0"
        self.player.participant.vars['start_time'] = str(time.time())
        # print(self.player.participant.vars["data"])
        return self.player.participant.vars["data"]['trial_number'][self.round_number - 1] <= self.session.vars['max_trials']

    def vars_for_template(self):
        selections = self.player.participant.vars["data"]["selections"][self.round_number - 1]
        is_training = self.player.participant.vars["data"]["is_training"][self.round_number - 1]
        trial_list = list(range(0, self.session.vars['training_trials'])) if is_training else list(
            range(0, self.session.vars['max_trials']))
        total_trials = self.session.vars['training_trials'] if is_training else self.session.vars['max_trials']
        bounds = self.player.calculate_image_bounds()
        all_bounds = {}
        cutoff = int(self.session.vars["number_of_pictures"] / len(self.group.get_players()))
        for i in range(len(self.group.get_players())):
            p_bounds = self.group.get_players()[i].calculate_image_bounds()
            all_bounds[self.group.get_players()[i].id_in_group] = [int(i) for i in range(p_bounds[0], p_bounds[1])]

        alien_symbols = {}
        for i in range(self.session.vars["number_of_pictures"]):
            alien_symbols[i] = AlienProductExchange.alien_symbols[i]

        return dict(trial_number=self.player.participant.vars["data"]["trial_number"][self.round_number - 1] - 1,
                    total_trials=total_trials,
                    total_trials_minus_one=total_trials - 1,
                    trial_list=trial_list,
                    is_training=self.player.participant.vars["data"]["is_training"][self.round_number - 1],
                    number_of_pictures=self.session.vars["number_of_pictures"],
                    alien_symbols=alien_symbols,
                    selections=selections,
                    joint_payoffs=self.player.participant.vars["data"]["selections_payoff"][self.round_number - 1],
                    p1_payoffs=self.player.participant.vars["data"]["p1_payoffs"][self.round_number - 1],
                    p2_payoffs=self.player.participant.vars["data"]["p2_payoffs"][self.round_number - 1],
                    round=self.player.round_number,
                    round_counter=self.round_number - 1,
                    rounds=Constants.num_rounds - 1,
                    player_id_raw=self.player.id_in_group,
                    player_id=f"p{self.player.id_in_group}-picture",
                    nickname=f"P{self.player.id_in_group}",
                    players=self.group.get_players(),
                    all_bounds=all_bounds,
                    modules=self.session.config['modules']
                    # block_times=block_times
                    )

    def js_vars(self):
        return dict(
            player_id=self.player.id_in_group,
            modules=self.session.config['modules']
        )

    def before_next_page(self):
        self.player.total_time_spent = str(time.time() - float(self.player.participant.vars["start_time"]))


class Results(Page):
    def vars_for_template(self):
        self.player.set_payoff_in_points()
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])
        return dict(round_payoff=self.player.payoff,
                    total_payoff=total_payoff,
                    is_training=self.player.participant.vars["data"]["is_training"][self.round_number - 1])
                    

    def before_next_page(self):
        # reset payoff because of training trial
        if self.round_number == 1:
            self.participant.payoff -= self.player.payoff
            self.player.payoff = 0


class TransitionPage(Page):
    def vars_for_template(self):
        # bonus = sum([float("{:.2f}".format(float(p.payoff) * Constants.conversion_rate)) for p in self.player.in_all_rounds()])
        bonus = round(sum([float("{:.2f}".format(float(p.payoff) * Constants.conversion_rate)) for p in self.player.in_all_rounds()]), 2)
        failedCheck = False
        if not self.player.participant.vars['comprehension_valid']:
            bonus = 0
            failedCheck = True
        self.participant.vars["alien_bonus"] = bonus
        return dict(bonus=bonus, failedCheck=failedCheck)


class WaitNextRound(WaitPage):
    def is_displayed(self):
        return self.round_number < Constants.num_rounds

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [AlienMarket, Results, TransitionPage, WaitNextRound]
