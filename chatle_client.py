# This is the client side of the Chatle program
# Users only have to run this file to play Wordle
# with their friends while chatting
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Server's IP address-if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # Used this to separate the client name & message

# initialize TCP socket and connect to the server
s = socket.socket()
print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...") 
s.connect((SERVER_HOST, SERVER_PORT))
print("Connected to Chatle server.")

# Initialize and set the user's info
name = input("Enter your username: ")
print("Welcome to the chat room " + name +"!")
won = False
guess_num = 0

# Init colors and choose a random color for the user
init()
rand_colint = random.randint(1, 256)
client_color = f"\033[38;5;{rand_colint}m"

def listen_for_messages():
    """
    This function keep listening for a message from the socket server
    Whenever a message is received, analyze it and print an according response
    """
    global won
    global guess_num
    while True:
        message = s.recv(1024).decode()
        msg_lst = message.split() # Used to analyze the message

        # Set won as true to prevent user from continue playing after guessing correctly
        if f"{Fore.LIGHTGREEN_EX}{name}{' has guessed the word correctly!'}" in message:
            won = True

        # If the player has made a valid guess, increase their guess count
        if len(msg_lst) > 2 and msg_lst[1] == name and msg_lst[2] == 'guessed:':
            guess_num += 1

        # If the player did not make a valid guess, print a message
        if len(msg_lst) > 1 and msg_lst[0] == name and msg_lst[1] == 'Notinwordlist':
            print("\nNot in word list")
            continue
        if len(msg_lst) > 1 and msg_lst[0] != name and msg_lst[1] == 'Notinwordlist':
            continue
        
        # If the player is just chatting with the other users
        print("\n" + message)


# Make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# Set thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

# Let everyone in the chat know that a user just joined
date_joined = datetime.now().strftime('%H:%M:%S')
pre_send = f"({date_joined}) {name}{' has just joined the chat!'}"
s.send(pre_send.encode())

while True:
    # Input message we want to send to the server
    to_send =  input()
    # a way to exit the program cleanly
    if to_send.lower() == 'q':
        break
    inp_words = to_send.lower().split() # Used to analyze the message
    
    if len(inp_words) < 1:
        print("Please type something to send")
        continue

    if len(inp_words) == 1 and inp_words[0] == 'guess':
        print("Please type a 5-letter word to make a guess")
        continue

    if inp_words[0] == 'guess' and len(inp_words[1]) != 5:
        print("Please guess a 5-letter word")
        continue

    if inp_words[0] == 'guess' and won:
        print("You've already guessed correctly")
        continue

    if inp_words[0] == 'guess' and guess_num == 6:
        print("You've run out of guesses")
        continue

    # If the user makes a proper guess, send it to the server to 
    # to check it and receive color coded hints
    if inp_words[0] == 'guess':
        guess = (inp_words[1]).lower()
        date_guess = datetime.now().strftime('%H:%M:%S') # add the datetime
        guess_send = f"{client_color}({date_guess}) {name} {'guessed'}{separator_token}{guess} {Fore.RESET}"
        s.send(guess_send.encode())
        continue
    
    # If the user just wants to chat with other players, send it to server to broadcast it
    date_now = datetime.now().strftime('%H:%M:%S') 
    to_send = f"{client_color}({date_now}) {name}{separator_token}{to_send}{Fore.RESET}"
    s.send(to_send.encode())

# Close the socket
s.close()
