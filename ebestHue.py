
import win32com.client
import pythoncom
 
class XASessionHandler:
     login_state = 0

     def Onlogin(code, msg):
         if code == "0000":
             print(code, msg)
             XASessionHandler.login_state = 1
         else:
            print(code, msg)

     def OnDisconnect():
        print("Session disconnected")
        XASessionHandler.login_state = 0

class EBest:
    def __init__(self):
        self.user = "geni88"
        self.password = "ge0713!"
        self.cert_password = ''
        self.host = "demo.ebestsec.co.kr" 
        self.port = 20001

        self.xasession_handler = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionHandler)

    def login(self):
        self.xasession_handler.ConnectServer(self.host, self.port)
        self.xasession_handler.Login(self.password, self.password, self.cert_password, 0, 0)

        while XASessionHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()

    def logout(self):
        XASessionHandler.login_state = 0
        self.xasession_handler.DisconnectServer()

ebest = EBest()
ret = ebest.login()
if ret == 0 :
    print('fail to login')
    quit(0)

print('login ok') 