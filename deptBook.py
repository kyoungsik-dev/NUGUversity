def getSejongdeptTime():
    deptTime=[
        ['군자관식당', '오전 11시', '오후 7시30분'],
        ['학생회관식당', '오전 10시30분', '오후 7시'],
        ['은행', '오전 9시', '오후 4시'],
        ['서점', '오전 9시', '오후 6시'],
        ['우체국', '오전 9시', '오후 4시'],
        ['헬스장', '오전 7시', '오후 10시'],
        ['복사실', '오전 9시', '오후 6시'],
        ['안경점', '오전 10시', '오후 6시'],
        ['사진관', '오전 10시', '오후 6시'],
        ['보건실', '오전 9시', '오후 6시']
        ]
    # print(tels)
    return deptTime
if __name__ == '__main__':
    from pprint import pprint as p
    p(getSejongdeptTime())
