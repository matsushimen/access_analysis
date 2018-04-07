# coding: utf-8
import sys,re,os
import datetime
import time
import argparse
import calendar

def date_to_epoch(d):
    try:
        r = int(calendar.timegm(d.utctimetuple()))
    except ValueError:
        print("Error : 不正な日付です。")
    return r

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Receive log files, a start date, and an end date")
    parser.add_argument("-l",
                        "--log",
                        nargs="*",
                        default=["/var/log/httpd/access_log"],
                        type=str,
                        help=u"ログファイルのパスを指定してください。 | default: %(default)",
                        dest="input_logs"
                        )
    parser.add_argument("-f",
                        "--from",
                        nargs="?",
                        default="1970-1-1",
                        type=str,
                        help=u"対象期間の開始日をY-m-dの形式で指定してください。 | default: %(default)s",
                        dest="start_date"
                       )
    parser.add_argument("-F",
                        "--FROM",
                        nargs="?",
                        default="00:00:00",
                        type=str,
                        help=u"対象期間の開始時間をH:M:Sの形式で指定してください。 | default: %(default)s",
                        dest="start_time"
                       )
    parser.add_argument("-t",
                        "--to",
                        nargs="?",
                        default="9999-12-31",
                        type=str,
                        help=u"対象期間の終了日をY-m-dの形式で指定してください。 | default: %(default)s",
                        dest="end_date"
                       )
    parser.add_argument("-T",
                        "--TO",
                        nargs="?",
                        default="23:59:59",
                        type=str,
                        help=u"対象期間の終了時間をH:M:Sの形式で指定してください。 | default: %(default)s",
                        dest="end_time"
                       )
    parser.add_argument("-o",
                        "--output",
                        nargs="?",
                        default=None,
                        type=str,
                        required = None,
                        help=u"結果の出力先を指定してください。 | default:標準出力",
                        dest="out"
                       )
    stdate = parser.parse_args().start_date+"-"+parser.parse_args().start_time
    endate = parser.parse_args().end_date+"-"+parser.parse_args().end_time
    try:
        date_from = date_to_epoch(datetime.datetime.strptime(stdate, "%Y-%m-%d-%H:%M:%S"))
        date_to = date_to_epoch(datetime.datetime.strptime(endate, "%Y-%m-%d-%H:%M:%S"))
    except ValueError:
        print("Error : 日付が不正です。")
        exit(1)
    
    host_dict = {}
    acc = {}
    for hour in range(24):
        acc[hour] = 0
    argvs = parser.parse_args().input_logs


    for filename in argvs:
        try:
            f = open(filename)
        except IOError:
            print ('"%s" cannnot be opened.' % filename)
            continue

        else:
            for line in f.readlines():
                line = line.strip()
                stat_list = line.split("\"")

                date = stat_list[0].split()[3][1:]
                tdatetime = datetime.datetime.strptime(date,'%d/%b/%Y:%H:%M:%S')
                if((date_from>date_to_epoch(tdatetime))|(date_to<date_to_epoch(tdatetime))):
                    continue
                
                acc[tdatetime.hour] += 1
                hostname = stat_list[0].split()[0]
                if(hostname in host_dict.keys()):
                    host_dict[hostname] += 1
                else:
                    host_dict[hostname] = 1
                
                client_id = stat_list[0].split()[1]
                usr = stat_list[0].split()[2]
                zone = stat_list[0].split()[4][:-1]
                first_line = stat_list[1].strip()
                response_stat = stat_list[2].split()[0]
                response_bite = stat_list[2].split()[1]
                referer = stat_list[3].strip()
                UA = stat_list[5].strip()
        
            f.close()
    ##結果表示##
    if(parser.parse_args().out!=None):
        try:
            o = open(parser.parse_args().out, 'w')
        except IOError:
            print ('"%s" cannnot be opened.' % parser.parse_args().out)
            exit(1)
            
        sys.stdout = o
    

    print('{:>5}'.format("Hour")+":"+'{:>5}'.format("Access")),
    for i,j in acc.items():
        print('{:>5}'.format(str(i)+"-"+str(i+1))+":"+'{:>5}'.format(str(j)))
    
    print('{:>16}'.format("Hostname")+":"+'{:>5}'.format("Access"))
    for i,j in sorted(host_dict.items(),key=lambda x: -x[1]):
        print('{:>16}'.format(str(i))+":"+'{:>5}'.format(str(j)))
    if(parser.parse_args().out!=None):
        o.close()