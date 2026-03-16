import time

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):

    def is_displayed(self):
        self.player.start_time = str(time.time())
        self.player.participant.vars['start_time'] = self.player.start_time
        return self.round_number == 1 and not self.player.is_comprehension_valid()

    def vars_for_template(self):
        return dict(trials=self.session.vars["max_trials"],
                    num_pictures=self.session.vars["number_of_pictures"],
                    num_blocks=4,
                    remaining_blocks=3,
                    image_path='images/instructions_4p{}i{}m.png'.format(self.session.config["number_of_pictures"], self.session.config['modules']))

    def before_next_page(self):
        increment = time.time() - float(self.player.start_time)
        self.player.instructions_completion_time = str(float(self.player.instructions_completion_time) + increment)


class ComprehensionQuestions(Page):
    form_model = 'player'
    form_fields = ['comp_creature_buying', 'comp_symbol_changes', 'comp_symbols_buy', 'last_recorded_time']

    def is_displayed(self):
        self.player.start_time = str(time.time())
        self.player.participant.vars['start_time'] = self.player.start_time
        return self.round_number == 1 and not self.player.is_comprehension_valid()

    def before_next_page(self):
        if not self.player.is_comprehension_valid():
            self.player.comprehension_times += 1

        increment = time.time() - float(self.player.start_time)
        self.player.comprehension_completion_time = str(float(self.player.comprehension_completion_time) + increment)


class ComprehensionWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['comprehension_valid']

class ComprehensionFailed(Page):
    def is_displayed(self):
        return not self.participant.vars['comprehension_valid']

    def before_next_page(self):
        if not self.player.is_comprehension_valid():
            self._is_frozen = False
            self._index_in_pages -= 3
            self.participant._index_in_pages -= 3


page_sequence = [Instructions, ComprehensionQuestions, ComprehensionFailed, ComprehensionWaitPage]
