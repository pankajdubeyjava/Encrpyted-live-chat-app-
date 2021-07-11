import socket
import sys
import time
import json
from cryptography.fernet import Fernet

s= socket.socket()
host= "127.0.0.1"
print("server will start on host:",host)
port=8888
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
print("server is bound successfully")
s.listen(1)
conn, addr=s.accept()
print(addr, "has connected")

def login():
    incoming_msg=conn.recv(1024)
    incoming_msg=incoming_msg.decode()
    incoming_msg=json.loads(incoming_msg)
    email=incoming_msg["email"]
    password=incoming_msg["password"]
    count=-1
    with open ("login.json", "r") as file:
                data=json.load(file)
    for user in data["email"]:
        count+=1
        if email== user:
            if data["password"][count]==password:
                print("welcom in chatAP")
                msg="Yes"
                conn.send(msg.encode())
                chatting(email)
            else:
                msg="No"
                conn.send(msg.endcode())
def creataccount():
    incoming_msg=conn.recv(1024)
    incoming_msg=incoming_msg.decode()
    incoming_msg=json.loads(incoming_msg)
    email=incoming_msg["email"]
    password=incoming_msg["password"]
    with open ("login.json", "r") as file:
        data=json.load(file)
    data["email"].append(email)
    data["password"].append(password)
    with open("login.json", "w") as file:
        json.dump(data, file) 
    login()

def chatting(email):
    while True:
        incoming_msg=conn.recv(1024)
        key=conn.recv(1024)
        f = Fernet(key)
        incoming_msg=f.decrypt(incoming_msg) 
        print(email,":>>",incoming_msg)
        key = Fernet.generate_key()
        f = Fernet(key)
        msg=input(str("You:>>"))
        en=f.encrypt(bytes(msg, 'utf-8'))
        conn.send(en)
        conn.send(key)
if conn.recv(1024).decode()=="login":
    login()
else:
    creataccount()