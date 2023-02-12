# Chatle
Chatle is a program that allows you to play Wordle while chatting with friends and other online users. Each user can send message to their friends but if they want to make guess, they'll need to type the key word 'guess' and their actual 5-letter word. The program will then let everyone playing Chatle know the color-coded hints that the user got but not the exact word that they guessed. The program utilizes sockets to design a client-server model. The purpose of this project is to exemplify a Network OS, where the server contains the main program file and required resources  (ie: the text file of all the 5-letter words) to run the application. The client-side simply connect to the server using the socket, collects the user's name, messages and their 5-letter word guess and sends it to the connected server. The server analyzes each received message from its client, if the client made a valid guess, it sends back a color-coded hint, or if the client sent a chat message, it broadcasts to all of its connected clients. <br />

# How to Run
Python 3.8 must be installed. The program will also utilize the colorama library.
```md
> pip install colorama
```
On the server side or the computer that runs the chatle_server.py , execute below command in the terminal. <br />
```md
> python3 chatle_server.py
```
On the client side, the chatle_client.py must be modified, the value of SERVER_HOST must be set to the IPv4 address of the server. Any client who wants to connect and run the application can run the below command from their own terminal.

```md
> python3 chatle_client.py
```
![Quote](https://github.com/kannikakabilar/Chatle/blob/main/275752206_5080581921999469_2772197795159133071_n.png)
![Quote](https://github.com/kannikakabilar/Chatle/blob/main/276032683_494356002413065_2598985376848425207_n.png)
![Quote](https://github.com/kannikakabilar/Chatle/blob/main/259079261_761454304882987_6497286830440979526_n.png)
![Quote](https://github.com/kannikakabilar/Chatle/blob/main/276042174_701217644366026_7789669837002488075_n.png)
