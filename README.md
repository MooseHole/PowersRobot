# PowersRobot
Powers Robot for Reddit

This bot is currently run from Heroku under https://powersrobot.herokuapp.com/


Parameters:  
[[Battle BattleName]]  
[[Faction FactionName /u/UserName]]  
[[Commander FactionName CommanderName]]  
[[Units FactionName Amount Region|Region Type|CV Name]]  
/u/BotName

Example:  
[[Battle Test fight!]]  
[[Terrain Plains]]  
[[Faction Good /u/Moose_Hole]]  
[[Faction Ebil /u/Moose__Hole]]  
[[Faction Ebil /u/moosehole]]  
[[Commander Bucket Good]]  
[[Commander Wignit Good]]  
[[Commander Reaper Ebil]]  
[[Units Good 1000 The Riverlands]]  
[[Units Ebil 1000 The Riverlands Light Infantry]]  
[[Units Ebil 20 The Riverlands Ranged Infantry]]  
[[Units Ebil 10 The Westerlands Heavy Cavalry]]  
[[Units Ebil 5 100 Zombies]]  
/u/PowersRobot

Output:  
Test fight! is ready to begin in Plains!  
* Good:  
    * Users:  
        * /u/Moose_Hole  
    * Commanders:  
        * Bucket  
        * Wignit  
    * Units:  Total Combat Value 1705  
        * 1000 The Riverlands (CV 1705)  
            * 400 The Riverlands Light Infantry (CV 400)  
            * 100 The Riverlands Heavy Infantry (CV 200)  
            * 250 The Riverlands Ranged Infantry (CV 475)  
            * 150 The Riverlands Light Cavalry (CV 330)  
            * 100 The Riverlands Heavy Cavalry (CV 300)  
* Ebil  
    * Users:  
        * /u/Moose__Hole  
        * /u/moosehole  
    * Commanders:  
        * Reaper  
    * Units: Total Combat Value 1571  
        * 1000 The Riverlands Light Infantry (CV 1000)  
        * 20 The Riverlands Ranged Infantry (CV 38)  
        * 10 The Westerlands Heavy Cavalry (CV 33)  
        * 5 Zombies (CV 500)  

To begin battle:  
/u/Moose_Hole respond [[Confirm]]  
/u/Moose__Hole respond [[Confirm]]  
/u/moosehole respond [[Confirm]]  
--OR--  
moderator respond [[Confirm override]]  

To delete battle:  
moderator respond [[Delete]]  
