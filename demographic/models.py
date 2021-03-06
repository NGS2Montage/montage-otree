from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Parang'

doc = """
This app displays the demographic survey
"""


class Constants(BaseConstants):
    name_in_url = 'demographic'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for player in self.get_players():
            player.participant.vars['consent'] = True
            player.participant.vars['playing'] = True
            player.participant.vars['locked'] = False
            player.participant.vars['clicked'] = True
            player.participant.vars['money_earned'] = self.session.config['participation_fee']
            player.participant.vars['anagrams_wait_required'] = False
            player.participant.vars['pgg_arrival_wait'] = False
            player.participant.vars['pgg_results_wait'] = False

        self.session.vars['locked'] = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.PositiveIntegerField(
        verbose_name="What is your age?",
        choices=[
            [1, "0-17 years old"],
            [2, "18-30 years old"],
            [3, "31-40 years old"],
            [4, "41-60 years old"],
            [5, "61-80 years old"],
            [6, "greater than 80 years old"],
        ],
        widget=widgets.RadioSelect(),
    )

    income = models.CharField(
        verbose_name="What is your annual household income (answer in USD)?",
        choices=["Less than $25,000", "$25,000 - $49,999", "$50,000 - $74,999", "$75,000 - $99,999",
                 "$100,000 - $124,999", "$125,000 - $149,999", "Greater than $150,000", "Do not wish to answer"],
        widget=widgets.RadioSelect(),
    )

    sex = models.CharField(
        verbose_name="What is your sex?",
        choices=["Male", "Female", "Other"],
        widget=widgets.RadioSelect()
    )

    marital_status = models.CharField(
        verbose_name="What is your marital status?",
        choices=["Never married", "Married", "Widowed", "Separated", "Divorced", "Other", "Do not wish to answer"],
        widget=widgets.RadioSelect()
    )

    country_born = models.CharField(verbose_name="In which country were you born?")

    country_reside = models.CharField(
        verbose_name="""What best describes your current location?""",
        choices=[
            "Africa",
            "Asia/Pacific",
            "Europe",
            "Latin America",
            "Middle East",
            "North America",
        ],
        widget=widgets.RadioSelect(),
    )

    year_moved = models.CharField(verbose_name="If your country of birth is different than your country of residence, "
                                               "what year did you come to your country of current residence?",
                                  blank=True)

    highest_degree = models.CharField(
        verbose_name="""What is the highest level of education that you have
        completed (received degree or other certification)?""",
        choices=["Did Not Complete High School", "High School", "Some College", "Bachelor's Degree", "Master's Degree",
                 "Advanced Graduate work or Ph.D.", "Not Sure"],
        widget=widgets.RadioSelect()
    )

    speciality = models.CharField(
        verbose_name="What is your area of specialty (college major, work skills, etc.) if applicable?",
	choices=["Engineering", "History", "Mathematics", "Literature", "Foreign Language", "Social Sciences", "Arts", "Psychology", "Natural Sciences (Biology, Chemistry Physics)", "Agriculture", "Business", "Education", "Health Sciences", "Medicine", "Law", "Other", "Choose not to answer"],
        widget=widgets.RadioSelect()
    )

    employment_status = models.CharField(
        verbose_name="What is your employment status?",
        choices=["Employed for wages", "Self-employed", "Out of work and looking for work",
                 "Out of work but not currently looking for work", "A homemaker", "A student", "Military", "Retired",
                 "Unable to work", "Other", "Choose not to answer"],
        widget=widgets.RadioSelect()
    )

    occupation = models.CharField(verbose_name="Occupation, if applicable?", blank=True)

    religious_preference = models.CharField(
        verbose_name="What is your religious preference?",
        choices=["None", "Roman Catholic", "Muslim", "Seventh-Day Adventist", "Mormon",
                 "an Orthodox church such as the Greek or Russian Orthodox Church", "Christian Scientist",
                 "Protestant", "Jewish", "Other"],
        widget=widgets.RadioSelect()
    )

    other_religion = models.CharField(
        verbose_name="If you selected Other in religious preference above, please specify your religion",
        blank=True
    )

    device_type = models.CharField(
        verbose_name="""What type of device are you using to complete 
            this task (tablet, desktop, laptop, phone, etc)?""",
        choices=[
            "desktop computer (e.g., monitor separate from CPU)",
            "tablet computer (e.g., Microsoft Surface, Apple iPad, etc.)",
            "phone (e.g., Apple iPhone, Samsung Galaxy, etc.)",
            "laptop computer (e.g., any portable computer not a tablet or phone)",
            "other",
        ],
        widget=widgets.RadioSelect()
    )

    membership_duration = models.PositiveIntegerField(
        verbose_name="""How long have you been a member of Amazon Mechanical
        Turk?""",
        choices=[
            [1, "less than 1 month"],
            [2, "1 month - 6 months"],
            [3, "6 months - 1 year"],
            [4, "greater than 1 year"],
        ],
        widget=widgets.RadioSelect(),
    )

    access_turk = models.CharField(
        verbose_name="How do you usually access Amazon Mechanical Turk?",
        choices=["Cell phone", "Computer", "Tablet", "Other"],
        widget=widgets.RadioSelect()
    )

    access_turk_other = models.CharField(
        verbose_name="If you selected others above, please specify:", blank=True
    )

    timezone = models.CharField(
        verbose_name="What is your current timezone?"
    )

    timezone_access = models.CharField(
        verbose_name="From what timezone do you usually access Amazon Mechanical Turk?"
    )

    time_of_day = models.CharField(
        verbose_name="What time of day do you usually use Amazon Mechanical Turk?",
        choices=["4am-8am; early morning", "8am-12pm; late morning", "12pm - 4pm; afternoon",
                 "4pm - 8pm; early evening", "8pm - 12am; late evening", "12am - 4am; late night"],
        widget=widgets.RadioSelect()
    )

    hours_spent = models.PositiveIntegerField(
        verbose_name="How long do you usually spend during a session using Amazon Mechanical Turk? (in hours)",
    )

    start_frequency = models.CharField(
        verbose_name="How frequently do you start a new session on Amazon Mechanical Turk?",
        choices=["Multiple times a day", "Once a day", "Every 1-3 days", "Weekly", "Monthly", "Yearly"],
        widget=widgets.RadioSelect()
    )

    location = models.CharField(
        verbose_name="What type of location best classifies your current location?",
        choices=["Home", "Work", "Other"],
        widget=widgets.RadioSelect()
    )

    location_other = models.CharField(
        verbose_name="If you selected other above, please specify your current location", blank=True
    )

    multitask = models.CharField(
        verbose_name="Do you multitask while using Amazon Mechanical Turk?",
        choices=["Yes", "No"],
        widget=widgets.RadioSelect()
    )

    multitask_yes = models.CharField(
        verbose_name="If you selected yes above, please specify what kind of other activity is involved while "
                     "multitasking?",
        blank=True
    )

    hits = models.CharField(
        verbose_name="What kind of HITs do you normally accept on Amazon Mechanical Turk?",
    )

    number_of_studies = models.PositiveIntegerField(
        verbose_name="How many research studies have you participated in using Amazon Mechanical Turk?",
    )

    participation_number = models.PositiveIntegerField(
        verbose_name="How many times have you participated in this particular game before?",
    )

    consent = models.BooleanField()
