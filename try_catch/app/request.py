from datetime import datetime
import requests
import MySQLdb
import time
import schedule


def do_request():
    try:
        mydb = MySQLdb.connect("localhost", "root", "thanh2210", "nhanvien" )
    except:
        print("error to connect database !")
        exit()
    else:
        mycursor = mydb.cursor()
        try:
            mycursor.execute("SELECT url_name FROM web")
        except:
            print("something wrong when select column in the table !")
            exit()
        else:
            result = mycursor.fetchall()
        dem = 0
        for result1 in result:
            for result2 in result1:
                x = requests.get(result2)
                y = result2
                try:
                    val = (result2,)
                    sql = ("SELECT web_name FROM web WHERE url_name = %s")
                    mycursor.execute(sql, val)
                except:
                    print("some thing wrong when select fields or execute the statement !")
                    exit()
                else:
                    result3 = mycursor.fetchone()

                duong_dan = str(y)
                thoigian_check = str(datetime.now())
                trang_thai = str(x.status_code)

                try:
                    tup = (duong_dan, thoigian_check, trang_thai, result3)
                    sql = "INSERT INTO web_status(url_name,time_check,status,web_name) VALUES(%s,%s,%s,%s)"
                    mycursor.execute(sql, tup)
                except:
                    print("some thing wrong when select fields or execute the statement !")
                    exit()
                else:
                    mydb.commit()
                dem += mycursor.rowcount
            print(dem, "record is inserted")
        print("\nthe next send after delay time\n")
    finally:
        mydb.close()

def main():
    try:
        f = open("data.txt", "r")
        data = f.read()
    except:
        print("error to handling file !")
        exit()
    else:
        _time = int(data)
        schedule.every(_time).seconds.do(do_request) #đặt lịch theo giây
        #schedule.every(tg).minutes.do(do_request)  #đặt lịch theo phút
        #schedule.every(tg).day.at("06:00").do(do_request)  #đặt lịch theo ngày
        while True:
            schedule.run_pending()
            time.sleep(1)
    finally:
        f.close()

main()