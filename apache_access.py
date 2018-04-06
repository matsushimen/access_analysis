# coding: utf-8
import sys,re
import datetime
import time
import argparse
import calendar
def sorted_list(l):
    s = set(l)
    dict ={}
    for member in s:
        dict[member] = l.count(member)
    for i,j in sorted(dict.items()):
        print(str(i)+":"+str(j))
    return 0
def date_to_epoch(d):
    return int(calendar.timegm(d.utctimetuple()))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Receive log files, a start date, and an end date")
    parser.add_argument("-l",
                        "--log",
                        nargs="*",
                        type=str,
                        required=True,
                        help=u"ログファイルのパスを指定してください。",
                        dest="input_logs"
                        )
    parser.add_argument("-f",
                        "--from",
                        nargs="?",
                        default="1970-1-1",
                        type=str,
                        help=u"対象期間の開始日をY-m-dの形式で指定してください。 | 初期値: %(default)s",
                        dest="start_date"
                       )
    parser.add_argument("-t",
                        "--to",
                        nargs="?",
                        default="4000-12-31",
                        type=str,
                        help=u"対象期間の終了日をY-m-dの形式で指定してください。 | 初期値: %(default)s",
                        dest="end_date"
                       )
    stdate = parser.parse_args().start_date+"-00:00:00"
    endate = parser.parse_args().end_date+"-00:00:00"

    date_from = date_to_epoch(datetime.datetime.strptime(stdate, "%Y-%m-%d-%H:%M:%S"))
    date_to = date_to_epoch(datetime.datetime.strptime(endate, "%Y-%m-%d-%H:%M:%S"))

    line_num = 0
    host_list = []
    date_list = []
    acc = {}
    for hour in range(24):
        acc[hour] = 0

    argvs = parser.parse_args().input_logs
    for filename in argvs:
        f = open(filename)
        for line in f.readlines():
            line = line.strip()
            stat_list = line.split("\"")

            date = stat_list[0].split()[3][1:]
            tdatetime = datetime.datetime.strptime(date,'%d/%b/%Y:%H:%M:%S')
            if((date_from>date_to_epoch(tdatetime))|(date_to<date_to_epoch(tdatetime))):
                continue
            
            acc[tdatetime.hour] += 1
            hostname = stat_list[0].split()[0]
            host_list.append(hostname)
            
            client_id = stat_list[0].split()[1]
            usr = stat_list[0].split()[2]
            zone = stat_list[0].split()[4][:-1]
            first_line = stat_list[1].strip()
            response_stat = stat_list[2].split()[0]
            response_bite = stat_list[2].split()[1]
            referer = stat_list[3].strip()
            UA = stat_list[5].strip()
        
        f.close()
    #
    sorted_list(host_list)
    for i,j in acc.items():
        print(str(i)+":"+str(j))
