server_ip = input("enter server ip address (leave blank for 127.0.0.1): ")
if (server_ip == ""): server_ip = "127.0.0.1"

import global_scope
import main

global_scope.SERVER_ADDRESS = (server_ip, global_scope.SERVER_ADDRESS)