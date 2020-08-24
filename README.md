# Instagram-Bot

## Motivation
This project combines implementation of different Python libraries such as pandas and selenium with OOP.

## About the Project
Assume you own a company which offers bots for instagram, and you want to ease the operators and make sure things go as planned.
The operator will open instaBotMain.py.
First, the program operator will be asked to enter the path where the Chrome driver is located.
Next, the operator will be asked to enter the client's name. This is the name of the instagram user that the operator will
add or remove bots to.
Finally the operator will have 7 options to choose from:
1. Save your work and end Bot-Client Service.
   * This option saves the updates made for the client in an Excel file (.xlsx).
   * The Excel file consists of 2 sheets - 1. Bot Followers; 2. Client's Followers.
   * The first sheet is a list of all bots that follow the client.
   * The second sheet will be updated only after option 'Check recent unfollowers' is executed.
2. Add bot to client
3. Remove bot from client
4. Like all posts of client with a specific bot of your choice 
5. Like all posts of client with all bots added
6. Print current bot followers
7. Check recent unfollowers

 * The option menu will be running as an infinite loop. When option [1] is executed, all updates are      saved and the loop breaks. 
   Then, the program terminates. 
   
 * In order to make changes for another client run the program again.
 
 * Bot's password must contain integers only.
 
 * instaBotMain.py first line: from InstaBot import IgBot - means that instaBotMain.py and igBot.py are placed together at the same folder.
