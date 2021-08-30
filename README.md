# PyChess
created by Andreza Serra

A simple command line chess game using Python. 

This program was based on the xsanon code available here: https://github.com/xsanon/chess. The bugs contained in it have been fixed and the code and design structure has been changed to promote greater maintainability and readability.


The tests were done manually and the files with the test case entries are in the 'files' folder. 


## Before playing...
* Make sure you have Python 3.8 installed, you can learn how to install it [here](https://realpython.com/installing-python/)
* We recommend that you use the PyCharm terminal to run the game, as there you can increase the font size and enlarge the terminal window. Otherwise, the game will look too small on your screen, as it doesn't have a graphical interface.
* Learn how to install PyCharm [here](https://web.stanford.edu/class/archive/cs/cs106ap/cs106ap.1196/coursehandouts/installingpycharm.html) and how to configure the py interpreter in the IDE [here](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add_new_project_interpreter)  
* You can increase PyCharm terminal font in `File > Settings > Editor > Color Scheme > Console Font`. We recommend **JetBrains Mono** font and **size 33** to make the game look like this:


<img src="/home/acbse/Imagens/chess.png" width="1000"/>

## Starting the Game
1. Clone this repository
2. Open the PyChess project in PyCharm (you can learn how to do this [here](https://www.jetbrains.com/help/pycharm/open-projects.html))
3. With the previously configured interpreter selected, run the `game.py` file (you can learn how to do this [here](https://www.jetbrains.com/help/pycharm/running-without-any-previous-configuring.html))

## How to Play
The game follows the initial rules of occidental chess, with basic and exceptional moves that include:
- valid movement of each piece (Pawn, Rook, Bishop, Knight, Queen and King)
- check and checkmate
- pawn promotion
- castling
- en passant 

Each turn, you will be prompted with `From: ` and `To: ` where you will enter the current board position of a piece to where you want to move it.

The input string must follow the pattern `[number][letter]`, where the number represents the row and the letter the column 

Check a entry example:
`From: 2a
To: 3a`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Notes
Chess board only prints properly on Unix-type terminals due to system-specific colored printing. 
For Windows, use Ubuntu on WSL.
