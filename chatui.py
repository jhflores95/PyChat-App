# Script for Tkinter GUI chat client.

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def receive():
  while True:
    try:
      msg = client_socket.recv(BUFSIZ).decode("utf8")
      msg_list.insert(tkinter.END, msg)
    except OSError:   # Possibly the client has left chat.
      break

def send(event=None):
  msg = my_msg.get()    # Extract message to be sent
  my_msg.set("")        # Clear input field
  client_socket.send(bytes(msg, "utf8"))
  if msg == "{quit}":
    client_socket.close()
    main.quit()

def on_closing(event=None):  # Cleanup function
  my_msg.set("{quit}")
  send()

# GUI building below

main = tkinter.Tk()
main.title("PyChat App")

messages_frame = tkinter.Frame(main)
my_msg = tkinter.StringVar()    # Store the value from the input field
my_msg.set("Enter text here")
scrollbar = tkinter.Scrollbar(messages_frame)   # Enables navigation through past messages

msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set, background = "white")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_box = tkinter.Entry(main, textvariable=my_msg)
entry_box.bind("<Return>", send)
entry_box.pack()
send_button = tkinter.Button(main, text="Send", command=send)
send_button.pack()

main.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
  PORT = 33000  # default
else:
  PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution