# Apache_accesslog_analysis
## Description
apacheのログファイルを解析する。
時間帯別のアクセス数とリモートホスト別のアクセス数を集計・表示する。

## Dependency
Python 3.6.4 :: Anaconda, Inc.

## Usage
実行オプション
-l, --log ログファイルのパスの指定　＊複数指定可能 default:/var/log/httpd/access_log\n
-f, --from 日時指定開始日の指定 フォーマットY-m-d default:1970-1-1\n
-F, --FROM 日時指定開始日の時間の指定 フォーマットH:M:S default:00:00:00\n
-t, --to 日時指定終了日の指定 フォーマットY-m-d default:9999-12-31\n
-T, --TO 日時指定終了日の時間の指定 フォーマットH:M:S default:23:59:59\n
-o, --out 出力先の指定　default:stdout\n
### Example
python apache_access.py -l testlog -f 2017-4-1 -t 2017-5-1 -o result.txt
testlogというapacheのログファイルから2017年4月1日00:00:00から2017年5月1日23:59:59までの時間帯別のアクセス数とリモートホスト別のアクセス数をカレントディレクトリのresult.txtとして書き出す。
## Author
松島　佑樹　Yuki Matsushima (m172240@hiroshima-u.ac.jp)