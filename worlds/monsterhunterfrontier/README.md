# Monster Hunter Frontier Archipelago

The Monster Hunter Frontier Randomizer requires [Postgres 14](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259101) to operate.
Ideally it'd be a locally hosted database using the password of "admin." However you may change it to whatever user and password you'd like
from the config.json inside of the `erupe` folder.

## What does randomization do?

In Monster Hunter Frontier, the first 6 quests in each HR is randomized. Completing a quest will grant a check. 
You cannot progress beyond HR 1 without first obtaining an Urgent Ticket for that rank.

## What is the goal?

You must obtain the Star Guildie Badge in order to win. Future victory conditions may include reaching a certain rank.

## What will be in other player's worlds?

Other players can find:

* Urgent Tickets
* Any Random Item
* Any Random Piece of Armor
* Any Random Weapon
* Zenny
* N-Points
* GCP

## What version of the game does this work for?

This only works for the ZZ version of the game.

## World Installation

1. Take the APWorld and place it inside of your Archipelago's `libs/worlds` folder.
2. Download the APFrontier connector and yaml from the [Releases](https://github.com/matthe815/APFrontier/releases/latest).
3. Customize your YAML and place it within the Players folder.

## Game Setup

1. Make sure your database is properly setup with `admin` as the default password -> otherwise change the config.json later.
2. Place your quests into the quests folder.
3. Using the APFrontier.zip you downloaded earlier. Extract it somewhere.
4. Within the folder is a setup.exe. Run that before anything else.
5. Assuming default settings, open your command line and run `psql -d "dbname='erupe' user='postgres' password='admin' host='192.168.1.1'" -f setup.sql`.
6. You are now ready to run the local server.

## Randomize!

1. Generate your game.
2. Go to the `compiler` folder.
3. Take the `AP_xxxxxxxxxxxx_Px_X.apmhf` from your archive and place it within the folder.
4. Take your `dat/mhfdat.bin` and `dat/mhfinf.bin` from your copy of Monster Hunter Frontier and place it within the folder.
5. Drag and drop the apmhf file onto randomizer-win.exe
6. Once it is done, you will find your new `mhfdat.bin` and `mhfinf.bin` within the `compiled` folder.
7. Replace your `mhfdat.bin` and `mhfinf.bin`

## How to start the server

To start the server, drag and drop an apmhf file onto the `apfrontier.exe` in the main directory.
Everything will be automatically setup and ready.
