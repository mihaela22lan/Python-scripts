import csv
import unicodecsv
import sys
import MySQLdb
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('C:\Temp\Log_File.log')
logger.addHandler(fh)

#Process Date Argument
if len(sys.argv)>1:
    file_name=sys.argv[1]
else:
    logger.error("no input date!")
    sys.exit(1)

#Get the csv file into a list
csv_file='C:\Temp\%s' % file_name
output_file='C:\Temp\%s_output.csv' % file_name
msisdn = []

with open(output_file, 'w') as f:
    f.write('MobileNo,AppID,Operator,Status,Created,Spent,Premium, Failed, LastBilled,LastStatusUpdate,Shortcode, CompanyId,Gateaway \n')

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for header,value in row.items():
            value=re.sub("[^0-9^.]", "",value)
            value = "'+" + value.strip(' ') + "'"
            msisdn.append(value)

# Open database connection
db = MySQLdb.connect( host='slave.colo', user='USER', passwd='PASS')
# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "select  S.*, L.Line as Shortcode, L.CompanyID,L.Gateway from Artiq.Subscribers S join Artiq.Applications A on (S.AppID = A.AppID) join Artiq.Line L on (A.LineId = L.LineId) where S.MobileNo in (%s)" % ','.join(msisdn)
logger.info(sql)
cursor.execute(sql)
rows=cursor.fetchall()

with open(output_file,'a') as f:
    for row in rows:
        line = row[0] + ',' + str(row[1]) + ',' + str(row[4])  \
               + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[8]) \
               + ',' + str(row[9]) + ',' + str(row[10]) + ',' + str(row[11]) \
               + ',' + str(row[12]) + ',' + str(row[14]) + ',' + str(row[15]) + ',' + str(row[16]) + ',' + '\n'
        f.write(line)

