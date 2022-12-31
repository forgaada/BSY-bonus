# BSY 2022/2023 Bonus Assignment
This repository serves for purposes of Stage 5 implementation in BSY bonus assignment.

Example video `full_example.mp4` - showing communication between controller and two bots.

## How it works?

![example.gif](example.gif)

Bots (`bot.py`) and Controller (`controller.py`) communicate over comment section in Gist with url: https://gist.github.com/forgaada/11fc787784a6a18ee1b89f6ceb4f4803 .

Communication is done by creating comments in Gist and embedding hidden commands to a markdown
comment section (e.g.: `<!-- ls -->`). First comment is always containing command for bots
and following comments are outputs from consoles.

Bots are checking new comments from Controller every 1 to 10 seconds (randomized interval due to race
condition issue). After resolving command (using `subprocess` library) output is appended to given comment.

![img.png](comment_screenshot.png)

User creates new comments (commands for bots) from controller by typing `post` to console. Output for pending commands 
is resolved all at once after typing `read` (it's not automatically). List of all new
commands outputs from all bots is then returned. Output contains bot ID, command from controller and
raw bot console output (e.g.: `<!-- Bot ID: 7d8ecd98-b569-499a-bf38-e5d9ccd501ef | Command: ls | Output: b'bot.py\ncomment_screenshot.png\nconsoles_screenshot.png\ncontroller.py\nexample.gif\nREADME.md\n' -->`).

Supported commands may differ based on terminal / console where is bot running. For Linux / Bash
should be supported all default terminal commands like: `ls`, `id`, `w` ..or running binary using `./<filename>.exe`.

![img.png](consoles_screenshot.png)










