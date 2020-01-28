# MineCityAPI
2D Mining game API

to operate, run app.py from your console
navigate via browser to the given port Ex: http://127.0.0.1:5000/

to run your txt file through the app, after the port input the execute file path
    Ex: http://127.0.0.1:5000/execute_file/TestText.txt
    Note in this example TestText.txt is in the same directory as app.py


@/ 
    Home Route
    Methods: Get
    Returns Json format of all current players and their values
    Other Routes will call this route to return current state of game
    
    ```json
    [
       {
            "A": {
                "direction": "north", 
                "inventory": [
                "coin"
                ], 
                "location": [
                2, 
                0
                ], 
                "name": "A"
            }, 
            "B": {
                "direction": "north", 
                "inventory": [
                "diamond"
                ], 
                "location": [
                -3, 
                0
                ], 
                "name": "B"
            }, 
            "C": {
                "direction": "north", 
                "inventory": [
                "diamond"
                ], 
                "location": [
                5, 
                0
                ], 
                "name": "C"
            }
        }
    ]

@/execute_file/<string:tfile>
    Route to execute file for game instructions
    Methods: Post
    Reads given txt file with game commands and executes other paths based on command recieved

@/movePlayer/<string:input>
    Route to move player
    Methods: Post
    Given string input, parses out Player and Distance and move Player accordingly with reguards to Player's Direction
    Distance is limited in range -1000,1000

@/turnPlayer/<string:input>
    Route to turn player
    Methods: Post
    Given string input, parses out Player and direction to turn with reguards to direction Player is currently facing
    Player is locked to 90 degree settings based on compass: North, East, South, West
    Player can only turn left or right

@/mineItem/<string:input>
    Route to mine item and add to player inventory
    Methods: Post
    Given String input, parses out Player and item to be mined and adds the given item to the Player's inventory

@/lookupInventory/<string:player>
    Route to get a Player's current inventory
    Methods: Get
    Given string input, searches out matching Player and returns count of unique items in that Player's inventory

@/lookupItemOwners/<string:item>
    Route to get Players that have aquired given item
    Methods: Get
    Given string input, searches out all Players that have the given item in their inventory

@/lookupDistance/<string:input>
    Route to find distance between given player and either another given player or a set of coordinates
    Methods: Get
    Given string input, parses for either two Players or one Player and a pair of cordinates and then returns the Manhatten Distance between them.