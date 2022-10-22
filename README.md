# owl

rough scripts to help me get my head around potion mixing in Potionomics

it uses https://steamcommunity.com/sharedfiles/filedetails/?id=2876744197 list of ingredients
save it as a CSV, add a column 'Availability' with a number of ingredients in your inventory
in the code (for now) modify the recipe and cauldron limits
in the core (for now) modify the threshold for passing a mix for a recipe. default is 0 for perfect magimin balance only
run `python owl.py`
it outputs all valid recipes as a csv file
load that in your spreadsheet editor of choice, convert into a table and sort and filter by anything you like

tracks the total cost (based on Quinn's prices), total magimin count, all the possitive and negative traits
