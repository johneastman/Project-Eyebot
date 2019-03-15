import socket
import json
import time

import direct_keys  # direct_keys.py


HOST = "184.171.155.200"
PORT = 65432
ENCODING = "utf-8"

def spawn_enemy(enemy_dict):
    
    code = enemy_dict["code"]
    number = enemy_dict["number"]
    
    for _ in range(number):
        direct_keys.key_sequence(f"~player.placeatme {code}\n~".upper())
        time.sleep(0.1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024).decode(ENCODING)
            
            for enemy in json.loads(data):
                spawn_enemy(enemy)

            conn.sendall("Data successfully retrieved".encode(ENCODING))
            break
