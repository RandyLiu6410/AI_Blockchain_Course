import sys, os, re, io, csv
from os import walk
from bs4 import BeautifulSoup

def main(data_dir_path):
    files = []
    for (dirpath, dirnames, filenames) in walk(data_dir_path):
        files.extend(filenames)
        break
    
    _data_dir_path = data_dir_path if data_dir_path[-1] == '/' else data_dir_path + '/'

    # Create directory
    path = "result"

    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    with open('result/result_1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['oid', 'n', 'Transaction'])

        for fileName in files:
            oid, n, Transaction = pullData1(_data_dir_path + '/' + fileName)
            writer.writerow([oid, n, Transaction])
        
        print('write to result_1.csv done')

    with open('result/result_2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['oid', '產品名稱', '產出組織', '產出日期', '有效日期', '產出數量', '剩餘數量'])

        for fileName in files:
            oid, name, org, date, expire, count, last = pullData2(_data_dir_path + '/' + fileName)
            writer.writerow([oid, name, org, date, expire, count, last])
        
        print('write to result_2.csv done')

    with open('result/result_3.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['oid', 'gps'])

        for fileName in files:
            oid, gps = pullData3(_data_dir_path + '/' + fileName)
            _gps = ''
            for g in gps:
                _gps += '(' + g[0] + ',' + g[1] + '),'

            writer.writerow([oid, _gps[:-1]])
        
        print('write to result_3.csv done')

    # print(pullData2(_data_dir_path + 'data_106800.txt'))

def pullData1(file):
    soup = BeautifulSoup(open(file), "html.parser")

    # get oid
    url = soup.find('meta', {'property' : 'og:url'})['content']
    _start = url.find('oid=') + 4
    _end = url.find('&m=')
    oid = url[_start:] if _end == -1 else url[_start:_end]

    # get transactions
    transactions = ''
    count = 0
    for transaction in soup.find_all('a', {'class' : 'btn btn-dark btn-lg btn-width'}):
        count += 1
        transactions += transaction.text.strip() + ','

    return oid, count, transactions[:-1]

def pullData2(file):
    soup = BeautifulSoup(open(file), "html.parser")

    # get oid
    url = soup.find('meta', {'property' : 'og:url'})['content']
    _start = url.find('oid=') + 4
    _end = url.find('&m=')
    oid = url[_start:] if _end == -1 else url[_start:_end]

    # get product name
    name = soup.find('h1').text.strip()
    info = re.sub(r"[\n\t\s]*", "", soup.find('div', {'class' : 'username'}).text)
    
    org_index = info.find('產出組織：')
    date_index = info.find('產出日期：')
    expire_index = info.find('有效日期：')
    count_index = info.find('產出數量：')
    last_index = info.find('剩餘數量：')

    org = info[org_index + 5 : date_index]
    date = info[date_index + 5 : count_index] if expire_index == -1 else info[date_index + 5 : expire_index]
    date = date[:10] + " " + date[10:]
    expire = date[0:11] if expire_index == -1 else info[expire_index + 5 : expire_index + 15]
    count =  info[count_index + 5 : last_index]
    last = info[last_index + 5 : ]

    return oid, name, org, date, expire, count, last

def pullData3(file):
    soup = BeautifulSoup(open(file), "html.parser")

    # get oid
    url = soup.find('meta', {'property' : 'og:url'})['content']
    _start = url.find('oid=') + 4
    _end = url.find('&m=')
    oid = url[_start:] if _end == -1 else url[_start:_end]

    # get gps

    gps = []

    for script in soup.find_all('script', type='text/javascript'):
        for content in script.contents:
            _strip = re.sub(r"[\n\t\s]*", "", content.strip())
            indexes = [m.start() for m in re.finditer('\]=\[{lat:', _strip)]
            for index in indexes:
                _end = _strip[index:].find('}];')
                _cut = _strip[index : index + _end + 1]

                _lat_start_indexes = [m.start() + 4 for m in re.finditer('lat:', _cut)]
                _lat_end_indexes = [m.start() for m in re.finditer(',lng:', _cut)]
                _lng_start_indexes = [m.start() + 4 for m in re.finditer('lng:', _cut)]
                _lng_end_indexes = [m.start() for m in re.finditer('}', _cut)]

                for s_lat, e_lat, s_lng, e_lng in zip(_lat_start_indexes, _lat_end_indexes, _lng_start_indexes, _lng_end_indexes):
                    gps.append([_cut[s_lat : e_lat], _cut[s_lng : e_lng]])

                # print(_lat_end_indexes)

    return oid, gps

if __name__ == "__main__":
    main(sys.argv[1])