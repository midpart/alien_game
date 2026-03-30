from os import environ

SESSION_CONFIGS = [
    dict(
        name="alien_1p10i2m",
        display_name="Alien Game - 1 Participant / 10 Images / 2 Modules",
        num_demo_participants=1,
        app_sequence=['instructions_1p', 'alien_game_1p'],
        number_of_pictures=10,
        modules=2
    ),
    dict(
        name="alien_1p10i2mfsd",
        display_name="Alien Game - 1 Participant / 10 Images / 2 Modules / Fixed SD",
        num_demo_participants=1,
        app_sequence=['instructions_1p_old', 'alien_game_1p_old'],
        number_of_pictures=10,
        modules=2
    ),
    dict(
        name="alien_1p12i1m",
        display_name="Alien Game - 1 Participant / 12 Images / 1 Module",
        num_demo_participants=1,
        app_sequence=['instructions_1p_old', 'alien_game_1p_old'],
        number_of_pictures=12,
        modules=1
    ),
    dict(
        name="alien_2p102m",
        display_name="Alien Game - 2 Participants / 10 Images / 2 Modules",
        num_demo_participants=2,
        app_sequence=['instructions_2p', 'alien_game_2p'],
        number_of_pictures=10,
        modules=2
    ),
    dict(
        name="alien_2p12i2m",
        display_name="Alien Game - 2 Participants / 12 Images / 2 Modules",
        num_demo_participants=2,
        app_sequence=['instructions_2p', 'alien_game_2p'],
        number_of_pictures=12,
        modules=2
    ),
    dict(
        name="alien_3p12i3m",
        display_name="Alien Game - 3 Participants / 12 Images / 3 Modules",
        num_demo_participants=3,
        app_sequence=['instructions_3p', 'alien_game_3p'],
        number_of_pictures=12,
        modules=3
    ),
    dict(
        name="alien_4p12i4m",
        display_name="Alien Game - 4 Participants / 12 Images / 4 Modules",
        num_demo_participants=4,
        app_sequence=['instructions_4p', 'alien_game_4p'],
        number_of_pictures=12,
        modules=4
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6366622783804'
