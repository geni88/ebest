import time
import win32com.client
client = win32com.client.Dispatch("XA_Session.XASession")  # COM 타입의 XASession 객체를 불러온다.
client.ConnectServer("demo.ebestsec.co.kr", 20001)  

class XASession:
    #로그인 상태를 확인하기 위한 클래스변수
    login_state = 0

    def OnLogin(self, code, msg):
        """
        로그인 시도 후 호출되는 이벤트.
        code가 0000이면 로그인 성공
        """
        if code == "0000":
            print(code, msg)
            XASession.login_state = 1
        else:
            print(code, msg)

    def OnDisconnect(self):
        """
        서버와 연결이 끊어지면 발생하는 이벤트
        """
        print("Session disconntected")
        XASession.login_state = 0
        
def _execute_query(self, res, in_block_name, out_block_name, *out_fields, **set_fields):
    """
    TR코드를 실행한다.
    이 때, 10분에 200회를 초과하는 TR을 수행시키지 않도록
    TR을 수행할 때 마다 리스트에 TR 수행 시각을 저장하고
    저장된 수행 시각과 현재 시각을 비교해 10분이 넘은 값은
    리스트에서 제거하는 방식으로 수행 시간을 조정한다.
    이 리스트의 길이는 200을 초과하지 않는다.

    [Parameters]
    res            : TR 리소스 이름 (str)
    in_block_name  : 인블록 이름 (str)
    out_block_name : 아웃 블록 이름 (str)
    *out_fields    : 출력필드 리스트 (list)
    **set_fields   : 인블록에 설정할 필드 딕셔너리 (dict)

    [Returns]
    result : 결과 (list)
    """

    time.sleep(1)
    print("current query cnt:", len(self.query_cnt))
    print(res, in_block_name, out_block_name)

    while len(self.query_cnt) >= EBest.QUERY_LIMIT_10MIN:  # 현재 수행된 퀴리의 개수가 200개 이상인 경우
        time.sleep(1)                                      # 프로세스를 1초간 정지
        print("waiting for execute query... current query cnt:", len(self.query_cnt))
        self.query_cnt = list( filter( lambda x: (datetime.today() - x).total_seconds() < EBest.LIMIT_SECONDS, self.query_cnt ) ) # 호출된지 10분 미만인 TR만 추출

    xa_query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)  # XAQuery 객체 생성
    xa_query.LoadFromResFile(XAQuery.RES_PATH + res+".res")                       # 리소스 파일 로드

    #in_block_name 셋팅
    for key, value in set_fields.items():
        xa_query.SetFieldData(in_block_name, key, 0, value)
    errorCode = xa_query.Request(0) # TR 요청

    #요청 후 대기
    waiting_cnt = 0
    while xa_query.tr_run_state == 0:  # OnReceiveData 이벤트가 발생되면 tr_run_state는 1로 설정됨 (즉, 0인 경우는 아직 TR 결과가 나오지 않았음을 의미함)
        waiting_cnt +=1
        if waiting_cnt % 1000000 == 0 :
            print("Waiting....", self.xa_session_client.GetLastError())
        pythoncom.PumpWaitingMessages()

    result = []  # 결과 블럭을 담을 리스트
    count = xa_query.GetBlockCount(out_block_name)  # 결과의 개수 계산

    # TR 요청 결과를 result에 저장
    for i in range(count):
        item = {}
        for field in out_fields:  # out_fields Argument에서 정의된 필드값만 추출
            value = xa_query.GetFieldData(out_block_name, field, i)
            item[field] = value
        result.append(item)

    """
    print("IsNext?", xa_query.IsNext)
    while xa_query.IsNext == True:
        time.sleep(1)
        errorCode = xa_query.Request(1)
        print("errorCode", errorCode)
        if errorCode < 0:
            break
        count = xa_query.GetBlockCount(out_block_name)
        print("count", count)
        if count == 0:
            break
        for i in range(count):
            item = {}
            for field in out_fields:
                value = xa_query.GetFieldData(out_block_name, field, i)
                item[field] = value
            print(item)
            result.append(item)
    """

    XAQuery.tr_run_state = 0  # TR 요청 및 결과반환까지 종료
    self.query_cnt.append(datetime.today()) # TR 처리시간 저장

    #영문필드를 한글필드명으로 변환
    for item in result:
        for field in list(item.keys()):
            if getattr(Field, res, None):  # Field 객체에 res 필드를 추출
                res_field = getattr(Field, res, None)
                if out_block_name in res_field:
                    field_hname = res_field[out_block_name]
                    if field in field_hname:
                        item[field_hname[field]] = item[field]  # 한글 필드에 영문 필드의 값 복사
                        item.pop(field)  # 영문 필드명 삭제
    return result

_execute_query("t1305","t1305InBlock","t1305OutBlock1",["date",
"open",
"high",
"low",
"close",
"sign",
"change",
"diff",
"volume",
"diff_vol",
"chdegree",
"sojinrate",
"changerate",
"fpvolume",
"covolume",
"value",
"ppvolume",
"o_sign",
"o_change",
"o_diff",
"h_sign",
"h_change",
"h_diff",
"l_sign",
"l_change",
"l_diff",
"marketcap"],{"shcode":"304100",
"dwmcode":"1",
"date":"20230127",
"idx":"",
"cnt":"10"})