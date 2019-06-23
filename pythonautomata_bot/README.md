# AutomataBot...grow!
* Python 3.6
* pip install requests
* run glass_cage.py
---
Meet AutomataBot:
https://noopschallenge.com/challenges/automatabot
---
Copied and pasted from my other repo. Successfully solves noops challenge seeds.

Built on Tkinter. Should be good to go for Python 3.6

Automatically sends solution to Noops API for resolution of confirmation bias...

For alternate requests as per API.md:

<code>automatabot = AutomataBot(challenge="path_name")</code>

For a specific challenge

<code>challenge="/automatabot/challenges/-challengePath-</code>

For a specific game type, non-challenge

<code>challenge="/automatabot/rules/-name-/random"</code>


## TODO
* Settings to alter speed, refresh automata, (see API for more challenges!)
* ... ? Popup for success? Write on iterations of challenges to hdd?
* Hack it so it runs forever? Oh wait it kind of does that.


## Also...
Name: inverse, Birth: [0, 1, 2, 3, 4, 5, 6, 7, 8], Survival: [3, 4, 6, 7, 8], Life Span: 7, Cols: 33, Rows: 33

This set of rules is possibly one of the coolest things I've seen in a while. 
Just alter glass_cage.py to:

<code>automatabot = AutomataBot(challenge="/automatabot/rules/inverse/random")</code> 