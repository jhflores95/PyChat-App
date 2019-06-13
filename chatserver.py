#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat applications."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = ''       # Blank for any address.
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connection():
  # Sets up handling for incoming clients.
  while True:
      # Server waits for connection and prints when connected.
      client, client_address = SERVER.accept()
      print("%s:%s has connected." % client_address)

      client.send(bytes("Welcome! "+"Please type your name and press enter.","utf8"))
      
      # Store client address in 'addresses' dictionary.
      addresses[client] = client_address
      Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Client socket is argument
  # Handles a single client connection.
  name = client.recv(BUFSIZ).decode("utf8")
  welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
  client.send(bytes(welcome, "utf8"))       # Send message to new client.
  msg = "%s has joined the chat!" % name
  broadcast(bytes(msg, "utf8"))
  clients[client] = name                    # Register new client
  
  while True:
    msg = client.recv(BUFSIZ)
    if msg != bytes ("{quit}", "utf8"):
      broadcast(msg, name+": ")
    else:
      client.send(bytes("{quit}", "utf8"))
      client.close()
      del clients[client]
      broadcast(bytes("%s has left the chat." % name, "utf8"))
      break

def broadcast(msg, prefix=""):  # Prefix allows for name id
  # Seen by all clients
  for sock in clients:
    sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
  SERVER.listen(5)  # Five connections max
  print("Waiting for connection...")
  ACCEPT_THREAD = Thread(target=accept_incoming_connection)
  ACCEPT_THREAD.start() # Start the infinite loop
  ACCEPT_THREAD.join()
  SERVER.close()