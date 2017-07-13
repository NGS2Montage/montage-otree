from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django_countries import countries

doc = """
This app displays the demographic survey
"""

class Constants(BaseConstants):
    name_in_url = 'demographic-detailed'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
#    def before_session_starts(self):
        
#        for player in self.get_players():
#            player.participant.vars['consent'] = True
#            player.participant.vars['playing'] = True
#            player.participant.vars['locked'] = False
#            player.participant.vars['clicked'] = True
#            player.participant.vars['money_earned'] = self.session.config['participation_fee']
#        self.session.vars['locked'] = False
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    

    #Question 1
    income_skip = models.BooleanField()
    income = models.CharField(
        blank = True,
        verbose_name="""What is your annual household income (answer in USD;
        conversion tool: <a
        href='https://www.google.com/finance/converter'>https://www.google.com/finance/converter</a>)?
        """,
        choices=[
            "Less than $25,000 annually", 
            "$25,000 - $49,999 annually",
            "$50,000 - $89,999 annually", 
            "$90,000 - $149,999 annually", 
            "Greater than $150,000 annually", 
        #    "Skip this question"
        ],
        #widget=widgets.RadioSelect(),
    )

    #Question 2 
    house_skip = models.BooleanField()
    house = models.CharField(
        blank = True,
        verbose_name="""Including you, how many people live in the same house or
        apartment as you?""",
        choices=[
            "1", 
            "2",
            "3",
            "4",
            "5",
            "6",
            "More than 6 total people",
        #    "Skip this question"
        ],
        #widget=widgets.RadioSelect()
    )

    #Question 3
    marital_status_skip = models.BooleanField()
    marital_status = models.CharField(
        blank = True,
        verbose_name="What is your marital status?",
        choices=[
            "Never married", 
            "Married", 
            "Widowed", 
            "Separated", 
            "Divorced", 
            "Other", 
        #    "Skip this question"
        ],
        #widget=widgets.RadioSelect()
    )

    #Question 4
    friends_skip = models.BooleanField()
    friends = models.CharField(
        blank = True,
        verbose_name="""Not including family members or co-workers, how many
        friends do you have that you see in person at least once a week?""",
        choices=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7-10",
            "more than 10",
        #    "Skip this question",
        ],
        #widget=widgets.RadioSelect()
    )

    #Question 5
    country_born_skip = models.BooleanField()
    country_born = models.CharField(
        blank = True,
        verbose_name="In which country were you born?",
        choices = countries,
    )

    #Question 6
    country_reside_skip = models.BooleanField()
    country_reside = models.CharField(
        blank = True,
        verbose_name="""In which country do you currently reside?""",
        choices = countries,
    )

    #Question 7
    year_moved_skip = models.BooleanField()
    year_moved = models.CharField(
        blank = True,
        verbose_name="""If your country of birth is different than your country of residence,
                        what year did you come to your country of current
                        residence?""",
        choices = list(map(str,range(1940,2018))),
        # widget=widgets.DateInput,
    )

    #Question 8
    city_reside_skip = models.BooleanField()
    city_reside = models.CharField(
        blank = True,
        verbose_name="""What is your city of residence/home?""",
        choices=[],
    )

    # Question 9
    density_skip = models.BooleanField()
    density = models.CharField(
        blank = True,
        verbose_name="""What is the density of your neighborhood?""",
        choices=[
            "Rural (mostly farmland)",
            "Suburban (large house lots)",
            "Urban (small or no lots)",
        #    "Skip this question",
        ],
        #widget=widgets.RadioSelect()
    )

    # Question 10
    ethnicity_skip = models.BooleanField()
    ethnicity = models.CharField(
        blank = True,
        verbose_name="""What is your ethnicity?""",
        choices=[
            "American Indian or Alaska Native",
            "Asian",
            "Black or African American",
            "Hispanic or Latino",
            "Native Hawaiian or Other Pacific Islander",
            "White or Caucasian",
            "Latin American",
            "Mixed",
            "Unknown",
            "Other",
        #    "Skip this question",
        ],
        #widget=widgets.RadioSelect(),
    )

   
    # Question 11
    employment_status_skip = models.BooleanField()
    employment_status = models.CharField(
        blank = True,
        verbose_name="What is your employment status?",
        choices=[
            "Part-time paid employment outside the home.", 
            "Full-time paid employment outside the home.", 
            "Part- or full-time paid employment in the home.",
            "Homemaker or other unpaid work in the home.", 
            "Going to school full-time.", 
            "Going to school part-time.", 
            "Self-employed.", 
            "Out of work and looking for work.",
            "Out of work but not currently looking for work.",
            "Student",
            "Military",
            "Retired",
            "Unable to work",
            "Other", 
       #     "Skip this question."
        ],
       # widget=widgets.RadioSelect()
    )
 
    # Question 12
    free_time_skip = models.BooleanField()


    free_time_sports = models.BooleanField(
        verbose_name="""Play on sports team/club, such as for soccer, football, hockey, basketball, baseball.""",
        widget=widgets.CheckboxInput()
    )
    free_time_singing = models.BooleanField(
        verbose_name="""Part of a performing arts group such as singing, dancing.""",
        widget=widgets.CheckboxInput()
    )
    free_time_instrument = models.BooleanField(
        verbose_name="""Play a musical instrument in a band or take lessons.""",
        widget=widgets.CheckboxInput()
    )
    free_time_volunteer = models.BooleanField(
        verbose_name="""Do volunteer work such as work in a homeless shelter or package food for the hungry.""",
        widget=widgets.CheckboxInput()
    )
    free_time_hobbies = models.BooleanField(
        verbose_name="""I have hobbies such as book reading or collecting, drawing, stamp collecting, photography, hiking, bike riding.""",
        widget=widgets.CheckboxInput()
    )
    free_time_other = models.BooleanField(
        verbose_name="""Other""",
        widget=widgets.CheckboxInput()
    )

    free_time = models.CharField(
        blank = True,
        verbose_name = """How do you spend your free time? Please check all that apply.""",
        choices=[
            """Play on sports team/club, such as for soccer, football, hockey, basketball, baseball.""",
            """Part of a performing arts group such as singing, dancing.""",
            """Play a musical instrument in a band or take lessons.""",
            """Do volunteer work such as work in a homeless shelter or package food for the hungry.""",
            """I have hobbies such as book reading or collecting, drawing, stamp collecting, photography, hiking, bike riding.""",
            """Other""",
            #    "Skip this question",
        ],
        #checkbox
        widget=widgets.CheckboxInput()
        # input_type="checkbox"
    )
    
    # Question 13
    specialty_skip = models.BooleanField()
    specialty = models.CharField(
        blank = True,
        verbose_name="What is your area of specialty (college major, work skills, etc.) if applicable?",
	    choices=[
            "Engineering", 
            "History", 
            "Mathematics", 
            "Literature", 
            "Foreign Language", 
            "Social Sciences", 
            "Arts", 
            "Psychology", 
            "Natural Sciences (Biology, Chemistry Physics)", 
            "Agriculture", 
            "Business", 
            "Education", 
            "Health Sciences", 
            "Medicine", 
            "Law", 
            "Other liberal arts",
            "Other",
        #    "Skip this question"
        ],
        #widget=widgets.RadioSelect()
    )
    
    # Question 14
    occupation_skip = models.BooleanField()
    occupation = models.CharField(verbose_name="Occupation, if applicable?", blank=True)

    # Question 15a
    age_residence_skip = models.BooleanField()
    age_residence_6 = models.PositiveIntegerField(
        blank = True,
        initial = 0,
        verbose_name="Less than or equal to 6 years?",
    )
    age_residence_12= models.PositiveIntegerField(
        blank = True,
        initial = 0,
        verbose_name="7 to 12 years?",
    )
    age_residence_18= models.PositiveIntegerField(
        blank = True,
        initial = 0,
        verbose_name="13 to 18 years?",
    )
    age_residence_65= models.PositiveIntegerField(
        blank = True,
        initial = 0,
        verbose_name="19 to 65 years?",
    )
    age_residence_Over65=models.PositiveIntegerField(
        blank = True,
        initial = 0,
        verbose_name="Over 65 years?",
    )

    # Question 16
    activity_young_skip = models.BooleanField()
    activity_young_school = models.PositiveIntegerField(
        blank = True,
        verbose_name="Attend day care, school, or college?",
    )
    activity_young_afterSchool = models.PositiveIntegerField(
        blank = True,
        verbose_name="Participate in after-school group activities?",
    )
    activity_young_weekend = models.PositiveIntegerField(
        blank = True,
        verbose_name="Participate in weekend group activities?",
    )
    activity_young_sports = models.PositiveIntegerField(
        blank = True,
        verbose_name="Play on organized sports teams(s)?",
    )
    activity_young_flu = models.PositiveIntegerField(
        blank = True,
        verbose_name="Have taken this year's flu vaccine?",
    )

    # Question 17
    activity_old_skip = models.BooleanField()
    activity_old_work = models.PositiveIntegerField(
        blank = True,
        verbose_name="Work outside the home for wages?",
    )
    activity_old_school = models.PositiveIntegerField(
        blank = True,
        verbose_name="Attend school or college?",
    )
    activity_old_ptrans = models.PositiveIntegerField(
        blank = True,
        verbose_name="Use public transportation?",
    )
    activity_old_group = models.PositiveIntegerField(
        blank = True,
        verbose_name="Participate in evening or weekend group activities?",
    )
    activity_old_sports = models.PositiveIntegerField(
        blank = True,
        verbose_name="Play on organized sports team(s)?",
    )
    activity_old_flu = models.PositiveIntegerField(
        blank = True,
        verbose_name="Have taken this year's flu vaccine?",
    )

    participate = models.BooleanField(
        verbose_name="I would like to take the optional survey."
    )

    nSkips = models.PositiveIntegerField(
        initial = 17
    )
