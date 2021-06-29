# Lab 3: Pathfinding Part II

## Intro
This week, we will be taking a different approach to commanding our characters. Instead of having them make decisions through conditionals, we will be giving them direct instructions. You will be organizing a team of up to 3 characters, trying to find the quickest way to get all the diamonds from the playing area to the goal.

For this lab we will be practicing our data structures. You will be using dictionaries and lists to organize actions for your characters to take.


## Set Up
* Click the green 'Code' button on the top right of this section.
* Find 'Download ZIP' option and click it
* Unzip the file and move it over to your 'workspace' folder (or wherever you keep your files)

* Find the folder and open the entire folder in VSCode
    * You can find it in your Files and right click on it. Use the "Open with VSCode" option
    * You can also open VSCode, go to 'File' > 'Open' and then find the lab folder

* With VSCode open, go to the top of your window and find `Terminal`
* Click `Terminal`
* Click `New Terminal`

* In the new window that opens at the bottom of VSCode, type in
```
python run_small.py
```

* Hit enter
* You should see a game window open up, with a small grid and game objects.
* You are done with set up!

## Game Explanation
This is a puzzle game where you use Code to directly give actions to your characters. Your objective is to collect all the diamonds and reach the flag using the shortest amount of steps possible.

* If one of your characters falls in the river or goes out of bounds, then its game over.
* A character collects a diamond by occupying the same square.
* Your characters may throw any diamonds they have collected.
* You must have one character reach the endpoint, holding ALL of the diamonds.

Your objective is to pre-plan your route, using data structures to organize commmands to your character team. Inside of `lab.py` you will find 3 functions, that will apply individually to the three game scenarios we have.

## Lab Steps
* All the code you will need to edit is in `lab.py`
* `run_small.py`, `run_med.py`, and `run_big.py` are used to run the game. If you take a look inside, you can see how we set up the game to be played.
* Everything inside the `engine/` folder are the inner workings of the game. Feel free to take a look, but you won't need to change anything (unless you want to change your sprite speed)
* If at any point in the lab, you would like to change your sprite speed, open up `engine/game.py` and edit the variable `CHARACTER_SPEED`.

### Small Map
Let's get started with the small map scenario. If you notice, we have a river in the middle, a bridge at the bottom, a diamond at the top left, and the flag at the top right.

* Let's first see what happens when we don't give our character any commands
* Open up your terminal (if it isn't open already) and type in `python run_small.py` and hit enter
* Notice how our character now stays in one place. We call this action "IDLE".
* Let's look ahead and make an observation. If we want to get the diamond AND get to the flag, we need to start the game by moving up.
* Go into `lab.py` and find the section:
```python
# ------------------ Lab Small ---------------------

lab_actions_small = {}


def lab_run_small(character_id, time_step):
    """
    This function is given to the game in run_small.py
    """
    pass
```
* Notice how the comments say that this function runs in run_small.py
* `lab_run_small` is a function we call in the game engine, that will be used to give an action to our character. 
    * Notice how the variables it takes in as arguments are different now. We have `character_id` and `time_step`. We are given these so we can know which character we are commanding, and at what given time step.
    * Notice also that we have a dictionary to use, called `lab_actions_small`. We want to use this data structure to help organize the commands we want to give.
    * `time_step` refers to a constantly increasing variable we use to keep track of each step in time in the game. We measure this by how long it takes our sprite to move from one grid to another.
* Let's get started by getting our character to move to the diamond
* Replace the section with:
```python
# ------------------ Lab Small ---------------------

lab_actions_small = {
    'char_1': [up, up]
}


def lab_run_small(character_id, time_step):
    """
    This function is given to the game in run_small.py
    """
    actions_list = lab_actions_small[character_id]
    return actions_list[time_step]
```
* IMPORTANT: Since we will be commanding multiple characters, we want to differentiate which sequence of commands go to which character. This is why we are using a dictionary. The key is the character's name and the value is the list of actions we want them to take.
    * We only have one character in game right now, but we still need to format our dictionary in the same way.
    * The game engine code will automatically detect how many entries you have in that dictionary, and create a character with the id equals to the dictionary key you supplied. This is done for you, but don't assume it happens magically. Also we have a max of 3 characters.
* Notice how simple our function code is now. All we need to do is look into our data structure, find which character the function is called on (via character_id) and at what time step.
    * We do this through accessing the data structure. The first line accesses the DICTIONARY by looking up the character_id. The second line accesses the resulting LIST and finds the element at the xth index, where x is the value of time_step
* Make sure to save your file and then run the game again with `python run_small.py`

* Notice how our sprite moves up by two spaces!
* However, notice how we experienced an error. What do you think went wrong?
    * Whenever our software encounters an error and needs to close, you will see the error information displayed. It should always start with: `Traceback (most recent call last):` and then contain a lot information about files and lines.
    * This is called a Stack Trace. It contains useful information about what went wrong. It will even tell you exactly which line in your code was incorrect! You can sometimes debug whole issues by just looking at this information.

* Let's investigate by adding some print statements.
* ADD THIS LINE at the beginning of the `lab_run_small` function:
```python
    print("Character ID: " + character_id + ", Time step: " + str(time_step))
```

* Save your file and run the game again with `python run_small.py`
* Let's take a look at the the log statements (inside of your terminal).
* You should see something similar to:
```shell
char_1 at: a0
Character ID: char_1, Time step: 0
char_1 at: a1
Character ID: char_1, Time step: 1
Got the treasure at a2
char_1 at: a2
Character ID: char_1, Time step: 2
Traceback (most recent call last):
  File "run_small.py", line 42, in <module>
    pyglet.app.run()

...
<Multiple lines pointing out files in your computer>
...

IndexError: list index out of range
```
* Let's analyze this together. 
    * Notice how our time step starts at 0 (remember in lists, we start at the number 0)
    * Since the character_id is `char_1` and the time_step is `0` then we know that we are triggering the FIRST action for that character
    * Our character is now at a1 (he/she moved up by one space)
    * Next is `char_1` at time step `1`. That means we are giving him/her the second command in our list (which is also up)
    * `char_1` is now at a2, which means he/she moved up again.
    * Next we have `char_1` at time step `2`. This means we are trying to find the third command.
    * That's an issue, since we only put two items in our command list. 
    * Notice at the bottom of our stack trace, we get the message `IndexError: list index out of range`
    * This means that we tried to access an element of a list that doesn't exist! IE we tried to find the element at index 2, but there is no index 2, only index 0 and 1
    * Python will throw an error and our program will stop in a situation like this

* How do we fix this?
    * We can take something we learned from last week and apply it here. The conditional.
    * Before accessing an item from the list, we can make sure that the list is long enough to have that item
    * For example: If we are trying to find the 3rd item in that list, we can check if that list has AT LEAST 3 items. If it has less, then we know it will throw an error, so we don't try in the first place!
    * Remember that we can get the length of a list by using `len(list_variable)`

* Replace `lab_run_small` with
```python
def lab_run_small(character_id, time_step):
    """
    This function is given to the game in run_small.py
    """
    actions_list = lab_actions_small[character_id]
    if time_step < len(actions_list):
        return actions_list[time_step]
```

* Now we are checking if time_step is less than the length of actions_list, before trying to use it to access the list.
```
list - [up, up]
index - 0   1

len(list) - 2
```
* The size of the list is 2. Notice how the number of indexes is just below the size of the list. That's because we start at the number 0. You can usually be safe in assuming that if the index value is less than the length of the list, then you can use it to access the list.

* Save your file and run the game with `python run_small.py`
* Now your character should move up two spaces, and stay there. (If we don't give your character a command, then it will just stay idle.)
* Close the window and let's finally beat the game

* Now that your code is safe (won't throw errors) we can just concentrate on updating our data structure.

* Change `lab_actions_small` to
```python
lab_actions_small = {
    'char_1': [up, up, down, down, right, right, up, up]
}
```
* Save your file and run the game with `python run_small.py`
* Your character should make it to the end, and you win!
* Your output should look like:
```shell
You got all the treasure! You win!
Total steps taken: 8
Game shutting down
```

However, this was the easy way to get your character to win. But this wasn't really speedrunning the goal here. Let's find a way to get our total steps down.

* A new feature we have is to a) throw an item and b) command a team of characters
    * PSA: Throwing an item takes a single time step, so take that into account!
* By coordinating multiple characters, we can cut our time down by half
* Change `lab_actions_small` to
```python
lab_actions_small = {
    'char_1': [up, up],
    'char_2': [right, right, up, up]
}
```
* We create new characters by just adding a new dictionary entry! The game engine code will detect this and spawn a new character (up to 3)
* These commands should put both of our characters in the important positions (the diamond and the finish)
* Run `python run_small.py` to see the two characters move!

* However, we need to get the diamond over to char_2. Notice in `lab.py` we have a new set of commands
    * `throw_up`
    * `throw_down`
    * `throw_left`
    * `throw_right`

* We can get char_1 to throw the diamond over to the goal right when char_2 gets to it!
* Change `lab_actions_small` to
```python
lab_actions_small = {
    'char_1': [up, up, throw_right],
    'char_2': [right, right, up, up]
}
```

* Run `python run_small.py`
* We should now beat the game in 4 steps!

### Medium Map
Now let's try it out on a bigger map.

* Let's take a look at the new map by running `python run_med.py`
* Notice how many diamonds there are. It looks like we will need a full team of 3 to get a good time here
* Here's the cool thing, we don't need to change our code for this new map! The powerful part of data structures, is that it allows you to separate your logic from your data.
    * As long as our code has the right logic, we can reuse the same code inside our decision function and just change the data we give to it.
    * We want our code to apply as generally as possible. Aka handle as many cases as it can. Changing data structures is much easier and flexible than writing new code.
    * Also we want to make sure that we can process that data safely, which is why the conditional in the first part of this lab was so important.
* Change `lab_run_med` to
```python
def lab_run_med(character_id, time_step):
    """
    This function is given to the game in run_med.py
    """
    char_actions = lab_actions_med[character_id]
    if time_step < len(char_actions):
        return char_actions[time_step]
```

* Change `lab_actions_med` to
```python
lab_actions_med = {
    "char_1": [right, up, up, throw_right, up, left, up, right, throw_right],
    "char_2": [right, right, right, up, up, up, up, right, throw_right],
    "char_3": [right, right, right, right, up, up, right, right, up, up]
}
```

* These actions look correct, however the timing isn't right.
    * We want the characters to grab the diamonds and throw them to the right. However notice how char_2 moves too quickly and doesn't pick up the diamond that char_1 threw.
* Let's add some idle actions to our characters. 

* Change `lab_actions_med` to
```python
lab_actions_med = {
    "char_1": [right, up, up, throw_right, up, left, up, right, throw_right],
    "char_2": [right, right, right, up, up, up, up, idle, idle, right, throw_right],
    "char_3": [right, right, right, right, up, up, right, right, up, up]
}
```

* Run `python run_med.py` again to see the result
* Close! But char_3 moves too quickly, and reaches the finish flag before the diamond arrives. Remember, the character must have all the diamonds in order to beat the game (he/she can pick up the diamond AT the finish flag)
* Let's add another idle action to get the timing right:
```python
lab_actions_med = {
    "char_1": [right, up, up, throw_right, up, left, up, right, throw_right],
    "char_2": [right, right, right, up, up, up, up, idle, idle, right, throw_right],
    "char_3": [right, right, right, right, up, up, right, right, up, idle, up]
}
```

* Run `python run_med.py`
* Looks good! But if you notice the terminal output, it says we still lost. What happened?
* If you were keeping track, char_2 actually picks up TWO diamonds. But he only threw one to the goal.
* The fix here is to throw it again. But also make sure that char_3 waits until BOTH diamonds are at the goal before moving.

* Add a final `throw_right` command to char_2 and another `idle` command to char_3 BEFORE he/she moves up.

* Run `python run_med.py` and see if you won the game!
* This solution should get a score of 12 steps. See if you can find something better!


### Big Map
Alright, let's throw you out there and see how you do.

I will leave you to figure this out on your own. You should be able to use the learnings from the Small and Med Maps to solve this larger case.

You can run the big map by using the command `python run_big.py`

Message me and tell me how many steps your sprite team took to beat the game! I'll announce at the end whoever got the fastest score.
