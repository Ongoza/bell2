import os
while True:
    try:
        response = self.conn.getresponse().read()
        print(response)
    except:
        os.system("python3 server.py")
