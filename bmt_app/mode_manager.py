"""Here's where the guidance begins
We have productivity modes here with different approaches

    - pomodoro mode
    - OTAT mode (one thing at a time)

It teaches you how to traverse through your todo list if you have
it
"""

from tkinter.simpledialog import SimpleDialog
from gui_maker import Ask, Window, appLayoutModifier, Message, Button, modernButton


# the approach is simple

# print(f"""\

# 1. Set a clear goal (end goal)

# 2. Break it into 3 parts (called milestones)
#     Ask yourself, how can i achieve this goal?

# 3. Take one to the exclusion of all others. Break it down if necessary into 3 “sub-milestones”
#     Take one of those milestones and treat it as though it were your end goal (but for a set duration).
#     Forget about all the other milestones in this step.
#     If the selected milestone is too complex, break that down into 3 “sub-milestones” and so on for each sub-milestone as needed.
#     Try not to go to deep into detail to avoid overwhelm.

# 4. Finish that selected milestone completely without going back to it whatsoever.
#     “Tick” it for confidence
#     After ticking, you remind yourself where you are headed ultimately. Remind yourself as frequently as possible.

# 5. Repeat 3 and 4 for each of the milestones.



# """)


class OTATApproach(appLayoutModifier):
    def __init__(self):

        self.start()

    def start(self):
        self.bmt_win = Window()

        self.intro = Message('INFO', 'Welcome to OTAT approach',
                             f"""\
Welcome to the OTAAT (one thing at a time) approach!""")

        self.intro2 = Message('INFO', "WHAT YOU'LL ACHIEVE WITH THIS APPROACH", f"""\

In this approach, you will achieve the following:

        - You'll finish Projects FASTER

        - You'll have CLARITY OF MIND

        - You'll have LESS OVERALL STRESS

        - You'll feel MORE CONFIDENT at
            any stage of your project
            (even if you don't finish)

""")
        self.intro3 = Message('INFO', "WHAT OTAT APPROACH IS ALL ABOUT", f"""\

This approach consists of 5 simple steps:

        1. Set a clear Goal

        2. Break the goal down into 3 parts (milestones)

        3. Take one of those milestones to the exclusion
            of all others

        4. Finish that milestone completely.

        5. Repeat 2, 3 and 4 for each milestone (if necessary)

""")
        self.ready = Message('YESNO', 'Ready?',
                             "Are you Ready to start with this approach?")

        # 1. set a clear goal
        self.destination = Ask(
            'STRING', 'Set a clear goal', f"""\
Let's start by knowing what your desired end goal is.

What is the thing you want to create?
e.g. make a webpage

What is your end goal?""")

        # 2. break it down into 3 parts
        self.milestones = str(Ask('STRING', 'Breaking down the goal (Milestone 1)',
                                  f"""\
Now you can break the goal the goal down
into a maximum of 3 "milestones" to reach.
separate them with commas.

e.g. "make the header, make the body, make the footer"

How are you going to achieve this goal?

"""))

        self.milestones = self.milestones.split(',')

        # 3. which one to focus on first
        self.take_one = Ask('STRING', 'Taking one milestone only',
                            f"""\
It is important that you focus on only
one milestone at a particular time
from these milestones that you listed:

    - {self.milestone[0]}
    - {self.milestone[1]}
    - {self.milestone[2]}

Which one would you like to start with?
""")


# Now we have created your roadmap based on what you created
# your todo list will be structured in a way that will follow your map
# these are the things you will do.


# but then is there anyway to allow for them to break down big tasks, or do we
#
        # save the map
        OTATmap = {f'{self.destination}': self.milestones}

        print(f"""\
END Goal: {self.destination}

Milestones:
    - {self.milestone}

""")

        self.bmt_win.mainloop()


OTATApproach()

# r=Window()
# p=SimpleDialog(r,'asoo', ['Yes', 'No'], title='title', default=2)
# print(p)
# r.mainloop()
