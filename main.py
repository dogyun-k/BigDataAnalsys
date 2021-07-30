import csv
from functools import total_ordering
import requests, json
import re

# Origin 파일 속성값
# 설명 | 날짜 | 시간 | 장소 | 등록일 | 등록일
#   0      1     2      3      4        5
date = 1
time = 2
addr = 3

def split_data_into_date(split_year):
    """초기 데이터셋 (illegal_park_info.csv) 년도별로 파일 나눠서 저장."""

    with open('./illegal_park_info.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        csv_file = open(split_year+'.csv', 'w', newline='', encoding='utf-8-sig')
        writer = csv.writer(csv_file)

        for row in reader:
            # print(row)
            year = row[1][:4]
            if year == split_year:
                writer.writerow(row)

def get_geocode(address):
    """네이버 API로 주소 -> 좌표 리턴"""


    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?"
    client_id = "1g2av434tn"
    client_secret = "N4S7F8ie2frva4wOBNnsFmHfvlxZrhUeDQTHN0TX"
    query = "query=" + address
    header = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }

    r = requests.get(url + query, headers=header)
    result = r.json()
    # print(result)

    if r.status_code == 200:
        if result['meta']['totalCount'] != 0:
            long, lat = result['addresses'][0]['x'], result['addresses'][0]['y']
            return long, lat
        else:
            return None
    else:
        # print("Error :", r.status_code)
        return False

def remove_overlap(file_name):
    """origin 데이터셋에 중복되는 주소들 제거 후 주소만 txt로 저장"""

    origin_file = open(file_name+'.csv', 'r', encoding='utf-8-sig')
    result_file = open(file_name+'.txt', 'w', encoding='UTF-8')
    reader = csv.reader(origin_file)
    
    addresses = {}
    
    for row in reader:
        print(row)
        if not row[addr] in addresses:
            addresses[row[addr]] = 1
        else:
            addresses[row[addr]] += 1
    
    origin_file.close()

    addresses = dict(sorted(addresses.items(), key=lambda x: x[1], reverse=True))

    # print(addresses)



    for key, value in addresses.items():
        if value >= 10:
            key = normalization(key)

            result_file.write(f"{key}\t{value}\n")

def normalization(address):
    """검색 안되는 주소 전처리"""

    # 앞뒤 공백 지우기
    address = address.strip()

    # 첫 단어가 "북구"라면 제거
    if address[:2] == "북구":
        address = address[3:]
    
    address = "대구 북구 " + address

    # 검색에 방해되는 단어 지우기
    ban_words = ["뒤편", "부근", "건너", "사거리", "사거", "횡단보도", "횡단번호", "모퉁이", "소화전", "육교밑", "버스정류장", "버스정류", "어린이보호구역", "인도"]
    for word in ban_words:
        address = re.sub(word, '', address)

    # 끝 단어 이상한거 제거
    last_bad_word = ['부', '소', '장', '앞']
    if address[-1] in last_bad_word:
        address = address[:-1]


    # 괄호와 포함된 단어 지우기
    address = re.sub(r'\([^)]*\)', '', address)
    address = address.strip()


    #return "대구 북구 " + address

    address = gil_to_doro(address)

    return address

def gil_to_doro(addr):
    ### 동과 도로명 주소가 같이 있다면 제거함
    
    temp = addr.split(' ')
    
    if len(temp) < 4:
        return addr

    if temp[2][-1] == "동" or temp[2][-1] == "가":
        if temp[3][-1] == "로" or temp[3][-1] == "길":
            del temp[3]

    # print(temp)
    return " ".join(temp)
       
def check_ok(file_name):
    ### 검색 안 되는 주소 리스트 뽑기 ###

    f = open(file_name+'.txt', 'r', encoding='utf-8-sig')
    result = open(file_name+'_checked.csv', 'w', newline='', encoding='utf-8-sig')

    writer = csv.writer(result)

    ok_lists = []
    no_lists = []

    cnt = 0

    for row in f.readlines():
        row = row.strip()
        addr, number = row.split('\t')
        
        response = get_geocode(addr)

        if response != False:
            if response != None:
                ok_lists.append(['ok', addr, response[0], response[1], number])
            else:
                no_lists.append(['no', addr, number])
        else:
            no_lists.append(addr)

        print(f"\t{cnt}..... {(cnt / 3884)*100} %\t\t", end='\r')
        cnt += 1

    writer.writerows(no_lists)

    f.close()
    result.close()
    
def complete(file_name):
    """csv 파일 읽어서 주소 전처리 + 좌표값 입력"""
    geo_file = open(file_name+'_geo.csv', 'r', encoding='utf-8-sig')
    origin_file = open(file_name+'_origin.csv', 'r', encoding='utf-8-sig')
    reulst_file = open(file_name+'.csv', 'w', newline='', encoding='utf-8-sig')
    
    origin_reader = csv.reader(origin_file)
    geo_reader = csv.reader(geo_file)
    writer = csv.writer(reulst_file)


    # 파일 불러와서 딕셔너리 저장해놓고 쓰는게 더 빠름. 딕셔너리 서치 O(1)
    geo_dict = {}
    for row in geo_reader:
        geo_dict[row[0]] = [row[1], row[2]]


    lists = []
    cnt = 0
    total = 49447

    for row in origin_reader:
        # print(row)
        row[addr] = normalization(row[addr])

        if row[addr] in geo_dict:
            geo_point = geo_dict[row[addr]]
            lists.append(row[1:4] + geo_point)
            print(row[1:4] + geo_point)

        print(f"{(cnt / total) * 100} %\t{cnt}\t", end='\r')
        cnt += 1

        if cnt % 1000 == 0:
            writer.writerows(lists)
            lists = []
    
    geo_file.close()
    origin_file.close()
    reulst_file.close()

def make_geo_list_csv(file_name):

    input_file = open(file_name+'.txt', 'r', encoding='utf-8')
    output_file = open(file_name+'_geo.csv', 'w', newline='', encoding='utf-8-sig')

    writer = csv.writer(output_file)

    lists = []
    cnt = 0
    for row in input_file.readlines():
        address = row.split('\t')[0]
        geo_point = get_geocode(address)

        if geo_point != None:
            lists.append([address] + list(geo_point))
        else:
            print(address)

        counting(cnt, 679)
        cnt += 1 

    writer.writerows(lists)

    input_file.close()
    output_file.close()


if "__main__":



    # remove_overlap('2021')
    # check_ok('2021')
    # make_geo_list_csv('2021')
    # complete('2021')

    pass
