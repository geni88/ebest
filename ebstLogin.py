

import win32com.client
import pythoncom
class XASessionEventHandler:  
    login_state = 0

    def OnLogin(self, code, msg):  
        print('on login start')  
        if code == "0000":  
            print("login succ")  
            XASessionEventHandler.login_state = 1  
        else:  
            print("login fail")  
    def wait_for_event(code) :
        while XAQueryEventHandler.query_state == 0:
            pythoncom.PumpWaitingMessages()
        if XAQueryEventHandler.query_code != code :
            print('diff code : wish(',code,')', XAQueryEventHandler.query_code)
            return 0
        XAQueryEventHandler.query_state = 0
        XAQueryEventHandler.query_code = ''
        return 1
class EBestStock():  
    def __init__(self):
        self.operation_begin = '085000'
        self.operation_end = '153000'

    def login(self, server, id, pwd, cer_pwd, acc, acc_pwd) :
        self.instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)
        self.id = id
        self.passwd = pwd
        self.cert_passwd = cer_pwd
        self.account_number = acc
        self.account_pwd = acc_pwd
        self.instXASession.ConnectServer(server, 20001)
        self.instXASession.Login(self.id, self.passwd, self.cert_passwd, 0, 0)
        while XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()

        self.login = XASessionEventHandler.login_state
        return self.login        
if __name__ == "__main__":
    print('\\nebest testing')

server = "demo.ebestsec.co.kr" #"hts.ebestsec.co.kr"  # or "demo.ebestsec.co.kr" 모의투자
id = "geni88"
passwd = "ge0713!"
cert_passwd = "" #공인인증서 암호
account_number = 0 #"계좌번호"
account_pwd = 0 #"계좌비밀번호"

ebest_st = EBestStock()
ret = ebest_st.login(server, id, passwd, cert_passwd, account_number, account_pwd)
if ret == 0 :
    print('fail to login')
    quit(0)

print('login ok')  