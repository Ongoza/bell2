import os

server = 0
cam_manager = 0

while True:
    try:
        response = self.conn.getresponse().read()
        print(response)
    except:
        os.system("python3 server.py")
        os.system("python3 cam_manager.py")
