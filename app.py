# import necessary libraries
from flask import (
    Flask,
    render_template,
    jsonify,
    request)
import math


app = Flask(__name__)

# Create a list to hold our player data
player_data = {}

@app.route("/")
def home():
    # outputs current players and their statss
    return jsonify(player_data)

# tfile should contain the path to the txt file to read from
# use "TestText.txt" for the test txt file
@app.route("/execute_file/<string:tfile>")
def execute(tfile):
    output = ""
    ofile = open(tfile,"r")
    steps=ofile.readlines()
    for line in steps:
        try:
            path = line.split(":")[0]
            inputs = line.split(":")[1].strip() #removes trailing spaces

            # checks where to send the input
            if(path == "movePlayer"):
                move(inputs)
            elif(path == "turnPlayer"):
                turn(inputs)
            elif(path == "mineItem"):
                mine(inputs)
            # these are the commands with expected output
            elif(path == "lookupInventory"):
                output = output + checkInv(inputs)+"\n"
            elif(path == "lookupItemOwners"):
                output = output + findOwners(inputs)+"\n"
            elif(path == "lookupDistance"):
                output = output + findDistance(inputs)+"\n"
        except:
            pass
    
    ofile.close()

        #will write over file
    writeout = open("output.txt","w")
        #appends to file
    #writeout = open("output.txt","a")
    writeout.write(output)
    writeout.close()
    return output


@app.route("/movePlayer/<string:input>")
def move(input):
    # make distance an int or throw error if it cant
    try:
        player = input.split(",")[0]
        distance = int(input.split(",")[1])
    except:
        return "Error: invalid distance"

        #keeps distance moved within paramaters
    distance = min(1000,max(-1000,distance))

    # Moves assuming north is positive x and east is positive y
    if player not in player_data:
        player_data[player] = {"name":player,"location":[0,0],"direction":"north","inventory":[]}

    # move based on direction player is facing
    if(player_data[player]["direction"] == "north"):
        player_data[player]["location"] = [player_data[player]["location"][0] + distance,player_data[player]["location"][1]]
    elif(player_data[player]["direction"] == "east"):
        player_data[player]["location"] = [player_data[player]["location"][0] ,player_data[player]["location"][1]+ distance]
    elif(player_data[player]["direction"] == "south"):
        player_data[player]["location"] = [player_data[player]["location"][0] - distance,player_data[player]["location"][1]]
    else: #west
        player_data[player]["location"] = [player_data[player]["location"][0] ,player_data[player]["location"][1]- distance]

    # if called via path, shows current player stats
    return home()

@app.route("/turnPlayer/<string:input>")
def input(input):
    # checks for two inputs
    try:
        player = input.split(",")[0]
        direction =input.split(",")[1]
    except:
        return "Error: Invalid number of inputs"

    #checks for invalid directions
    if direction.lower() not in ["left","right"]:
        return "Error: Invalid Direction"

    if player not in player_data:
        player_data[player] = {"name":player,"location":[0,0],"direction":"north","inventory":[]}

    # sets direction
    if(player_data[player]["direction"] == "north"):
        player_data[player]["direction"] = "west" if direction.lower()=="left" else "east"
    elif(player_data[player]["direction"] == "east"):
        player_data[player]["direction"] = "north" if direction.lower()=="left" else "south"
    elif(player_data[player]["direction"] == "south"):
        player_data[player]["direction"] = "east" if direction.lower()=="left" else "west"
    else: #west
        player_data[player]["direction"] = "south" if direction.lower()=="left" else "north"

    # if called via path, shows current player stats
    return home()

@app.route("/mineItem/<string:input>")
def mine(input):
    try:
        player = input.split(",")[0]
        item =input.split(",")[1]
    except:
        return "Error: Invalid number of inputs"

    if player not in player_data:
        player_data[player] = {"name":player,"location":[0,0],"direction":"north","inventory":[]}

    player_data[player]["inventory"].append(item)

    # if called via path, shows current player stats
    return home()

@app.route("/lookupInventory/<string:player>")
def checkInv(player):
    
    # does not create player in this instance
    if player not in player_data:
        return "Error: Player does not exist"

    inventory  = {}
    playerInv = player_data[player]["inventory"]

    for item in playerInv:
        if item in inventory:
            inventory[item] = inventory[item]+1
        else:
            inventory[item] = 1

    invOutput = ""
    for key in inventory:       #returns count with item
        invOutput = invOutput + key +":"+str(inventory[key])+","
    invOutput = invOutput[:-1]

    return invOutput

@app.route("/lookupItemOwners/<string:item>")
def findOwners(item):
    
    players  = []
    
    for key in player_data:
        if item in player_data[key]["inventory"]:
            players.append(key)
            
    if (len(players)<1):
        return "No Players have this item"

    outputs = ""
    for player in players:
        outputs = outputs + player +","
    return outputs[:-1]

@app.route("/lookupDistance/<string:input>")
def findDistance(input):
    
    #Looks for two players
    if(len(input.split(","))==2):
        player = input.split(",")[0]
        player2 = input.split(",")[1]
        if((player not in player_data)or(player2 not in player_data)):
            return "Error: One or more invalid players given"
        return getDistance(player_data[player]["location"][0],player_data[player]["location"][1],player_data[player2]["location"][0],player_data[player2]["location"][1])

    #Loods for 1 player and 2 valid cordinates
    elif(len(input.split(","))==3):
        try:
            player = input.split(",")[0]
            x = int(input.split(",")[1])
            y = int(input.split(",")[2])
        except:
            return "Error: Invalid coordinates"
        if(player not in player_data):
            return "Error: Invalid player given"
        return getDistance(player_data[player]["location"][0],player_data[player]["location"][1],x,y)

    return "Error: Incorrect inputs"


#Math Happens
def getDistance(x1,y1,x2,y2):
    #non manhattan Distance
    #return str(math.sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))))
    #Manhattan Distance
    return str(abs(x1-x2)+abs(y1-y2))

if __name__ == "__main__":
    app.run(debug=True)
