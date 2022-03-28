# This is the server side of the Chatle program
# The Chatle server file requires to access the 5-letter
# word list file which the client side doesn't need 
# This file also validates the users guess
# and sends the color coded hints accordingly
import socket
import random
from threading import Thread
from colorama import Fore, init, Back

# This should be set as the server's IP address when 
# client is executing from a different machine but the port
# can be any be any number from 1024-49151 => can be used w/o 
# superuser priveleges, 0-1023 are used for well-known systems
# and 49152-65535 are used for private ports or customized services
SERVER_HOST = "0.0.0.0" 
SERVER_PORT = 5002 
separator_token = "<SEP>" # used to separate the client name & message

# The ranks listed are for players in the chat on when they correctly 
# guess the word among the group
rank_idx = 0
rank_lst = ['1st', '2nd', '3rd', '4th']

# Only the server can access the text file containing the list of all
# 5-letter words
word_lst = []
f = open('words5.txt', 'r')
for line in f:
    word_lst.append((line.strip()).lower())
f.close()

# Randomly select a word to be guessed 
word_win = random.choice(word_lst)

# symbols to be displayed when each player makes a guess
green = f"{Fore.LIGHTGREEN_EX}[o]{Fore.RESET}"
yellow = f"{Fore.LIGHTYELLOW_EX}[~]{Fore.RESET}"
red = f"{Fore.RED}[x]{Fore.RESET}"

# Initialize list/set of all connected client's sockets
client_sockets = set()
# Create a TCP socket
s = socket.socket()
# Make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# Listen for upcoming connections
s.listen(5)

print(f"Chatle Server Running. Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    # Used to keep track of available rank for next player who guesses the word correctly
    global rank_idx
 
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client is no longer connected so remove it from the set
            print(f"A User has been disconnected")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
 
            # Used to analyze the message
            ref = msg.split()

            # When the player is making a guess and the word is not in list
            if len(ref) > 3 and ref[2] == 'guessed:' and not(ref[3] in word_lst):
                not_word_msg = ref[1] + ' Notinwordlist'
                for client_socket in client_sockets:
                    client_socket.send(not_word_msg.encode())
                continue

            # When the player has guessed the word correctly
            if len(ref) > 3 and ref[2] == 'guessed:' and ref[3] == word_win:
                name = ref[1]
                place = rank_lst[rank_idx]
                rank_idx += 1
                win_msg = f"{Fore.LIGHTGREEN_EX}{name}{' has guessed the word correctly!'} {name}{' ranks: '}{place}{Fore.RESET} \n"
                for client_socket in client_sockets:
                    client_socket.send(win_msg.encode())     
                continue
            
            # When the player makes a valid guess but not the correct word
            if len(ref) > 3 and ref[2] == 'guessed:':
                guessed = ref[3]
                name = ref[1]
                code_msg = ref[0] + " " + ref[1] + " " + "guessed: "
                for i in range(len(guessed)):

                    # Include green symbol if the letter is in the coreect spot
                    if guessed[i] == word_win[i]:
                        code_msg += green

                    # Include yellow symbol if the letter is in word but wrong spot
                    elif guessed[i] in word_win:
                        if guessed.count(guessed[i]) <= word_win.count(guessed[i]):
                            code_msg += yellow
                        # If player guessed the letter in word more than present in winning word 
                        else:
                            guessed = guessed[:i] + '~' + guessed[i+1:]
                            code_msg += red

                    # Include red symbol if the letter is in word
                    else:
                        code_msg += red

                # Let everyone in the chat know the type of guess that the player has made
                for client_socket in client_sockets:
                    client_socket.send(code_msg.encode())
                continue 
    
        # If the player did not make a guess and its just a message to the group chat
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    # Keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"A user: {client_address} has been connected.")
    # Add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # Start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # Make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # Start the thread
    t.start()

# Close client sockets
for cs in client_sockets:
    cs.close()
# Close server socket
s.close()
