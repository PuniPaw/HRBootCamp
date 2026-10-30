import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 산점도 그리기
def setScatterGraph():
    pass

def processFunc():
    # 서울시 관광지 정보 파일 읽기
    fname = '서울특별시_관광지입장정보_2011_2016.json'
    jsonTP = json.loads(open(fname, mode='r', encoding='utf-8'))
    # print(jsonTP)
    tour_table = pd.DataFrame(jsonTP, columns=('yyyymmdd', 'resNm', 'ForNum'))
    tour_table = tour_table.set_index('yyyymm')
    # print(tour_table.head(5))
    resNm = tour_table.resNm.unique()
    # print(resNm[:5])

    # 중국인 관광지 정보 파일 읽기
    cdf = '중국인방문객.json'
    jdata = json.loads(open(cdf, mode='r', encoding='utf-8'))
    china_table = pd.DataFrame(jdata, 'yyyymm', 'visit_cnt')
    print(china_table)

if __name__ == '__main__':
    processFunc()