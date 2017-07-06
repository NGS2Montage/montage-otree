SESSION_CONFIGS = [
#    {
#        'name': 'Ruse',
#        'display_name': 'Ruse',
#        'num_demo_participants': 2,
#        'app_sequence': ['demographic', 'demographic_detailed', 'ruse'],
#        'participation_money': 0.05,
#        'optional_survey_payout': 5,
#    },
        {
        'name': 'productionPriming',
        'display_name': 'Production P2 Priming',
        'num_demo_participants': 2,
        'app_sequence': [
            'welcome', 
            'demographic', 
            'instructions_anagrams',
            'anagrams',
            'ruse',
            'instructions_pgg', 
            'public_goods', 
            'demographic_detailed',
            ],
        'participation_money': 0.05,
        'ultimatum_split': False,
        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
        'ultimatum_cutoff': 50,  # Applicable only if 'ultimatum_split' is False
        'ultimatum_group_size': 3,
        'ultimatum_histogram': True,
        'bestScore': 400,
        'threshold_num_words': 100,
        'threshold_num_points': 100,
        'marginal_points': 1,
        'timeout_anagrams_min': 3,
        'pgg_bonus': 100,
	    'pgg_timeout_min': 1,
        'xChange_ratio': 1,
        'n_games': 3,
        'n_neighbors': 2,
        'optional_survey_payout': 5,
    },
#    {
#        'name': 'productionNoPriming',
#        'display_name': 'Production P2 Only No Priming',
#        'num_demo_participants': 2,
#        'app_sequence': ['demographic', 'instructions_anagrams','ruse','public_goods'],
#        'participation_money': 0.05,
#        'ultimatum_split': False,
#        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_cutoff': 50,  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_group_size': 3,
#        'ultimatum_histogram': True,
#        'bestScore': 400,
#        'threshold_num_words': 100,
#        'threshold_num_points': 100,
#        'marginal_points': 1,
#        'timeout_anagrams_min': 3,
#        'pgg_bonus': 100,
#	    'pgg_timeout_min': 1,
#    },
#   {
#        'name': 'production',
#        'display_name': 'Production',
#        'num_demo_participants': 4,
#        'app_sequence': ['demographic', 'instructions', 'anagrams', 'public_goods', 'ultimatum'],
#        'participation_money': 0.05,
#        'ultimatum_split': False,
#        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_cutoff': 50,  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_group_size': 3,
#        'ultimatum_histogram': True
#    },
#    {
#        'name': 'games',
#        'display_name': 'Games',
#        'num_demo_participants': 4,
#        'app_sequence': ['demographic', 'anagrams', 'public_goods', 'ultimatum'],
#        'participation_money': 0.05,
#        'ultimatum_split': False,
#        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_cutoff': 30,  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_group_size': 3,
#        'ultimatum_histogram': True
#    },
#    {
#        'name': 'anagrams',
#        'display_name': 'Anagrams',
#        'use_chat': False,
#        'num_demo_participants': 4,
#        'participation_money': 0.05,
#        #'app_sequence': ['demographic', 'anagrams'],
#        'app_sequence': ['demographic','instructions_anagrams','anagrams'],
#        'ultimatum_split': False,
#        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_cutoff': 50,  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_group_size': 3,
#        'ultimatum_histogram': True,
#        'bestScore': 400,
#        'threshold_num_words': 100,
#        'threshold_num_points': 100,
#        'marginal_points': 1,
#        'timeout_anagrams_min': 3,
#        'pgg_bonus': 100,
#	'pgg_timeout_min': 1,
#    },
#    {
#        'name': 'public_goods',
#        'display_name': 'Public Goods',
#        'num_demo_participants': 2,
#        'app_sequence': ['demographic', 'instructions_pgg', 'public_goods'],
#        'participation_money': 0.05,
#        'ultimatum_split': False,
#        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_cutoff': 50,  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_group_size': 3,
#        'ultimatum_histogram': True,
#        'pgg_bonus': 100,
#	'pgg_timeout_min': 1,
#    },
#    {
#        'name': 'ultimatum',
#        'display_name': 'Ultimatum',
#        'num_demo_participants': 4,
#        'app_sequence': ['demographic', 'ultimatum'],
#        'participation_money': 0.05,
#        'ultimatum_split': False,
#        'ultimatum_player_role': 'offeror',  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_cutoff': 30,  # Applicable only if 'ultimatum_split' is False
#        'ultimatum_group_size': 3,
#        'ultimatum_histogram': True
#    },
]