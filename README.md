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
Test fight!: Plains

||Good|CV: 1705|||Ebil|CV:1571|||
:---|:---|:---|:---|:---|:---|:---|:---|:---
|**Users**|/u/Moose_Hole||||/u/Moose__Hole||||
||||||/u/moosehole||||
|**Commanders**|Bucket||||Reaper||||
||Wignit||||||||
|**Units**|Amount|Region|Type|CV|Amount|Region|Type|CV|
||400|The Riverlands|Light Infantry|400|1000|The Riverlands|Light Infantry|1000|
||100|The Riverlands|Heavy Infantry|200|20|The Riverlands|Ranged Infantry|38|
||250|The Riverlands|Ranged Infantry|475|10|The Westerlands|Heavy Cavalry|33|
||150|The Riverlands|Light Cavalry|330|5||Zombies|500|
||100|The Riverlands|Heavy Cavalry|300|||||


To begin battle:  
/u/Moose_Hole respond [[Confirm]]  
/u/Moose__Hole respond [[Confirm]]  
/u/moosehole respond [[Confirm]]  
--OR--  
moderator respond [[Confirm override]]  

To delete battle:  
moderator respond [[Delete]]  
