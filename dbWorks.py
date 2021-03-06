# -*- coding: utf-8 -*-
import pymysql
import getMeal
import telBook
import deptBook
import getNotice as noticeGetter
import calendar
from pprint import pprint as p
from datetime import datetime
from datetime import timedelta
def getDB():
    db = pymysql.connect(
            host='schio.iptime.org',
            port=3306,
            user='root',
            passwd='cldh1004',
            db='NUGUversity',
            charset='utf8'
        )
    return db

def getDay(day):

    if day=='TODAY':
        today=datetime.today()
        year=str(today.year)
        date=str(today.month)+'월'+ str(today.day)+'일'
    elif day=='TOMORROW':
        tomorrow=datetime.today() + timedelta(days=1)
        year=str(tomorrow.year)
        date=str(tomorrow.month)+'월' + str(tomorrow.day)+'일'
    elif day=='A_TOMORROW':
        twoDaysLater=datetime.today() + timedelta(days=2)
        year=str(twoDaysLater.year)
        date=str(twoDaysLater.month)+'월'+ str(twoDaysLater.day)+'일'
    elif day=='YESTERDAY':
        yesterday=datetime.today() - timedelta(days=1)
        year=str(yesterday.year)
        date=str(yesterday.month)+'월'+ str(yesterday.day)+'일'
    elif day=='B_YESTERDAY':
        dayBeforeYesterday=datetime.today() - timedelta(days=2)
        year=str(dayBeforeYesterday.year)
        date=str(dayBeforeYesterday.month)+'월'+ str(dayBeforeYesterday.day)+'일'
    return year,date

def saveGunja():
    db=getDB()
    cursor = db.cursor()
    gunjaDatas=getMeal.getGunja()
    # mealGunja Columns -> idx year date day insDinner foodList
    for gunjaData in gunjaDatas:
        sql = "INSERT IGNORE INTO mealGunja(year, date, day, isDinner, foodList) VALUES (%s, %s, %s, %s, %s);"    
        cursor.execute(sql,(gunjaData[4], gunjaData[3], gunjaData[2], gunjaData[0], gunjaData[1])) # 2018 11월22일 금요일 중식 불고기
    db.commit()
    db.close()


def saveStudentsBuilding():
    db=getDB()
    cursor = db.cursor()
    foodList,price=getMeal.getStudentsBuilding()

    # init mealStudentsBuilding part 
    initCursor = db.cursor()
    truncateSql = "Truncate mealStudentsBuilding;" # init mealStudentsBuilding table
    initCursor.execute(truncateSql)

    # mealStudentsBuilding Columns -> idx foodList price currentTime
    for i in range(len(foodList)):
        sql = "INSERT IGNORE INTO mealStudentsBuilding(foodList, price) VALUES (%s, %s);"    
        cursor.execute(sql,(foodList[i],price[i])) #foodName, price
    
    db.commit()
    db.close()


def getStudentsBuildingPrice(foodName):
    db=getDB()
    cursor = db.cursor()
    sql = "SELECT price FROM `mealStudentsBuilding` WHERE `foodList` LIKE %s;"
    
    cursor.execute(sql,(foodName))
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type (('3,500원',),)
        return rows[0][0]

def getRandomStudentBuildingFood():
    db=getDB()
    cursor = db.cursor()
    sql = "SELECT foodList FROM mealStudentsBuilding ORDER BY RAND() LIMIT 1;"
    
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        return rows[0][0]

def saveNotice():
    db=getDB()
    cursor = db.cursor()

    # return type [titles, writers, writeTimes, numOfTitles]
    titles, writers, writeTimes, numOfTitles, urls = noticeGetter.getNotice()

    for i in range(len(titles)):
        sql = "INSERT IGNORE INTO notice(title, writer, writrTime, numOfTitle, link) VALUES (%s, %s, %s, %s, %s);"    
        cursor.execute(sql,(titles[i], writers[i], writeTimes[i], numOfTitles[i], urls[i]))
    db.commit()
    db.close()

def getNotice():
    db=getDB()
    cursor = db.cursor()
    saveNotice()
    sql='SELECT `title` FROM `notice` ORDER BY `numOfTitle` DESC LIMIT 3'
    cursor.execute(sql,())
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type (('오전 9시', '오후 6시'),)
        return rows[0][0], rows[1][0], rows[2][0] # openTime, closeTime
def getNoticeIncludeLink(idx):
    db=getDB()
    cursor = db.cursor()

    sql='SELECT `title`,link, writer FROM `notice` ORDER BY numOfTitle LIMIT 1 OFFSET %s;'

    cursor.execute(sql,(idx-1))
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type (('오전 9시', '오후 6시'),)
        return rows[0] # openTime, closeTime

def saveDeptBook():
    db=getDB()
    cursor = db.cursor()
    deptTimeData=deptBook.getSejongdeptTime()

    for info in deptTimeData:
        sql = "INSERT IGNORE INTO deptTime(dept, openTime, closeTime) VALUES (%s, %s, %s);"    
        cursor.execute(sql,(info[0],info[1],info[2]))
    
    db.commit()
    db.close()
def saveTelBook():
    db=getDB()
    cursor = db.cursor()
    telBookData=telBook.getSejongTelBook()

    for info in telBookData:
        sql = "INSERT IGNORE INTO telBook(department, number) VALUES (%s, %s);"    
        cursor.execute(sql,(info[0],info[1])) #ex 컴퓨터공학과, 3321
    
    db.commit()
    db.close()
def saveCalendar():
    db=getDB()
    cursor = db.cursor()
    calendarData=calendar.getCalendar()

    for event in calendarData:
        sql = "INSERT IGNORE INTO calendar(semester, event, startDate, endDate) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql,(event[0], event[1], event[2], event[3]))

    db.commit()
    db.close()
        
def getCalendar(event):
    today=datetime.today()
    nowMonth=today.month
    if nowMonth>6 and nowMonth<=12:
        semester='2학기'
    else:
        semester='1학기'

    db=getDB()
    cursor = db.cursor()

    sql = 'SELECT `startDate`, `endDate`, semester FROM `calendar` WHERE `event` LIKE %s and semester LIKE %s'
    cursor.execute(sql,(event, semester))
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type (('10월 22일', '10월 26일', '2학기'), ('4월 20일', '4월 26일', '1학기'))
        # return type (('3월 2일', '', '1학기'), ('9월 3일', '', '2학기'))
        return rows[0]#[0],rows[0][1] # openTime, closeTime

def getCalendarIncludeSemester(event, semester):
    today=datetime.today()
    
    db=getDB()
    cursor = db.cursor()

    sql = 'SELECT `startDate`, `endDate`, semester FROM `calendar` WHERE `event` LIKE %s and semester LIKE %s'
    cursor.execute(sql,(event, semester))
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type (('10월 22일', '10월 26일', '2학기'), ('4월 20일', '4월 26일', '1학기'))
        # return type (('3월 2일', '', '1학기'), ('9월 3일', '', '2학기'))
        return rows[0]#[0],rows[0][1] # openTime, closeTime

def getDeptTime(deptName):
    db=getDB()
    cursor = db.cursor()

    if deptName=='학술정보원':
        return '평일에는 오전 9시부터 오후 10시까지이며, 토요일과 방학은 오후 5시까지입니다. 열람실은 24시간 '

    sql = 'SELECT `openTime`, `closeTime` FROM `deptTime` WHERE `dept` LIKE %s'
    cursor.execute(sql,(deptName))
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type (('오전 9시', '오후 6시'),)
        return rows[0][0],rows[0][1] # openTime, closeTime

def getTelBook(deptName):
    db=getDB()
    cursor = db.cursor()

    sql = 'SELECT `number` FROM `telBook` WHERE `department` LIKE %s'
    cursor.execute(sql,(deptName))
    rows = cursor.fetchall()
    db.commit()
    db.close()
    if len(rows)==0:
        return 0
    else:
        # return type ((3321,),)
        return rows[0][0]

def getGunja(day):
    todayInfo=getDay(day)

    db=getDB()
    cursor = db.cursor()
    sql = "SELECT isDinner, foodList FROM mealGunja WHERE year LIKE %s AND date LIKE %s;"
    cursor.execute(sql,(todayInfo[0],todayInfo[1]))
    rows = cursor.fetchall()
    

    if len(rows)==0:
        saveGunja()
        cursor.execute(sql,(todayInfo[0],todayInfo[1]))
        rows = cursor.fetchall()
        if len(rows)==0:
            db.close()
            return dayKorean(day) + '에는 식당을 운영하지 않습니다'
    
    lunch = ", ".join(rows[1][1].split(' ')[:3])
    dinner = ", ".join(rows[0][1].split(' ')[:3])
    db.close()
    return dayKorean(day) + '의 점심 메뉴는 ' + lunch + '이고, 저녁 메뉴는 ' + dinner + '입니다'
    

def dayKorean(day):
    days = ['B_YESTERDAY', 'YESTERDAY', 'TODAY', 'TOMORROW', 'A_TOMORROW']
    koreans = ['그저께', '어제', '오늘', '내일', '모레']
    return koreans[days.index(day)]


if __name__ == '__main__':
    # p(getCalendar('개강'))
    # p(getCalendar('중간고사'))
    # p(getCalendarIncludeSemester('중간고사','1학기'))
    # p(getNoticeIncludeLink(1))
    p(getNotice())