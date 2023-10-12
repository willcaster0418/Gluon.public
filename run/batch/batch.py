#--*-- coding: utf-8 --*--
import pandas as pd
import urllib.request
import ssl
import zipfile
import os
# change file encoding to utf-8
def change_encoding(file_name, from_encoding="cp949", to_encoding="utf-8"):
    with open(file_name, mode="r", encoding=from_encoding) as f:
        data = f.read()
    with open(file_name, mode="w", encoding=to_encoding) as f:
        f.write(data)

def batch_krx_com_future(base_dir, encoding="cp949"):
    
    # download file
    print("Downloading...")

    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/fo_com_code.mst.zip", base_dir + "fo_com_code.mst.zip")
    os.chdir(base_dir)

    fo_com_code_zip = zipfile.ZipFile('fo_com_code.mst.zip')
    fo_com_code_zip.extractall()
    fo_com_code_zip.close()
    file_name = base_dir + "fo_com_code.mst"
    change_encoding(file_name, from_encoding="cp949", to_encoding=encoding)

    # df1 : '상품구분','상품종류','단축코드','표준코드','한글종목명'
    tmp_fil1 = base_dir + "fo_com_code_part1.tmp"
    tmp_fil2 = base_dir + "fo_com_code_part2.tmp"

    wf1 = open(tmp_fil1, mode="w", encoding=encoding)
    wf2 = open(tmp_fil2, mode="w", encoding=encoding)
    with open(file_name, mode="r", encoding=encoding) as f:
        for row in f:
            rf1 = row[0:55]
            rf1_1 = rf1[0:1]
            rf1_2 = rf1[1:2]
            rf1_3 = rf1[2:11].strip()
            rf1_4 = rf1[11:23].strip()
            rf1_5 = rf1[23:55].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + ',' + rf1_4 + ',' + rf1_5 + '\n')
            rf2 = row[55:].lstrip()
            wf2.write(rf2)
    wf1.close()
    wf2.close()
    part1_columns = ['상품구분','상품종류','단축코드','표준코드','한글종목명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding=encoding)

    # df2 : '월물구분코드','기초자산 단축코드','기초자산 명'
    tmp_fil3 = base_dir + "fo_com_code_part3.tmp"
    wf3 = open(tmp_fil3, mode="w", encoding=encoding)
    with open(tmp_fil2, mode="r", encoding=encoding) as f:
        for row in f:
            rf2 = row[:]
            rf2_1 = rf2[8:9]
            rf2_2 = rf2[9:12]
            rf2_3 = rf2[12:].strip()
            wf3.write(rf2_1 + ',' + rf2_2 + ',' + rf2_3 + '\n')
    wf3.close()
    part2_columns = ['월물구분코드','기초자산 단축코드','기초자산 명']
    df2 = pd.read_csv(tmp_fil3, header=None, names=part2_columns, encoding=encoding)

    # DF : df1 + df2
    df = pd.concat([df1,df2],axis=1)
    # os.remove(tmp_fil1)
    # os.remove(tmp_fil2)
    # os.remove(tmp_fil3)
    # os.remove(fo_com_code_zip)
    return df

def batch_krx_idx_future(base_dir, encoding='cp949'):
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/fo_idx_code_mts.mst.zip", base_dir + "fo_idx_code_mts.mst.zip")
    os.chdir(base_dir)

    fo_idx_code_zip = zipfile.ZipFile('fo_idx_code_mts.mst.zip')
    fo_idx_code_zip.extractall()
    fo_idx_code_zip.close()
    file_name = base_dir + "fo_idx_code_mts.mst"
    change_encoding(file_name, to_encoding=encoding)
    
    columns = ['상품종류','단축코드','표준코드',' 한글종목명',' ATM구분',
               ' 행사가',' 월물구분코드',' 기초자산 단축코드',' 기초자산 명']
    df=pd.read_table(file_name, sep='|',encoding=encoding,header=None)
    df.columns = columns

    return df

def batch_krx_stk_future(base_dir, encoding = 'cp949'):
    
    # download file
    print("Downloading...")

    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/fo_stk_code_mts.mst.zip", base_dir + "fo_stk_code_mts.mst.zip")
    os.chdir(base_dir)

    fo_stk_code_zip = zipfile.ZipFile('fo_stk_code_mts.mst.zip')
    fo_stk_code_zip.extractall()
    fo_stk_code_zip.close()
    file_name = base_dir + "fo_stk_code_mts.mst"
    change_encoding(file_name, to_encoding=encoding)

    fo_stk_code_zip = zipfile.ZipFile('fo_stk_code_mts.mst.zip')
    fo_stk_code_zip.extractall()
    fo_stk_code_zip.close()
    file_name = base_dir + "fo_stk_code_mts.mst"
    change_encoding(file_name, to_encoding=encoding)

    columns = ['상품종류','단축코드','표준코드',' 한글종목명',' ATM구분',
               ' 행사가',' 월물구분코드',' 기초자산 단축코드',' 기초자산 명']
    df=pd.read_table(file_name, sep='|',encoding=encoding,header=None)
    df.columns = columns
    #df.to_excel('fo_stk_code_mts.xlsx',index=False)  # 현재 위치에 엑셀파일로 저장

    return df

def batch_krx_spot_kosdaq(base_dir, verbose = False, encoding = "cp949"):
    cwd = os.getcwd()
    if (verbose): print(f"current directory is {cwd}")
    ssl._create_default_https_context = ssl._create_unverified_context
    
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kosdaq_code.mst.zip",
                               base_dir + "kosdaq_code.zip")

    os.chdir(base_dir)
    if (verbose): print(f"change directory to {base_dir}")
    kosdaq_zip = zipfile.ZipFile('kosdaq_code.zip')
    kosdaq_zip.extractall()
    
    kosdaq_zip.close()

    if os.path.exists("kosdaq_code.zip"):
        os.remove("kosdaq_code.zip")

    file_name = base_dir + "kosdaq_code.mst"
    change_encoding(file_name, to_encoding=encoding)
    tmp_fil1 = base_dir + "kosdaq_code_part1.tmp"
    tmp_fil2 = base_dir + "kosdaq_code_part2.tmp"

    wf1 = open(tmp_fil1, mode="w", encoding=encoding)
    wf2 = open(tmp_fil2, mode="w", encoding=encoding)

    with open(file_name, mode="r", encoding=encoding) as f:
        for row in f:
            rf1 = row[0:len(row) - 222]
            rf1_1 = rf1[0:9].rstrip()
            rf1_2 = rf1[9:21].rstrip()
            rf1_3 = rf1[21:].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
            rf2 = row[-222:]
            wf2.write(rf2)

    wf1.close()
    wf2.close()

    part1_columns = ['단축코드','표준코드','한글종목명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding=encoding)

    field_specs = [2, 1,
                   4, 4, 4, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 9,
                   5, 5, 1, 1, 1,
                   2, 1, 1, 1, 2,
                   2, 2, 3, 1, 3,
                   12, 12, 8, 15, 21,
                   2, 7, 1, 1, 1,
                   1, 9, 9, 9, 5,
                   9, 8, 9, 3, 1,
                   1, 1
                   ]

    part2_columns = ['그룹코드','시가총액 규모 구분 코드 유가',
                     '지수업종 대분류 코드','지수 업종 중분류 코드','지수업종 소분류 코드','벤처기업 여부 (Y/N)',
                     '저유동성종목 여부','KRX 종목 여부','ETP 상품구분코드','KRX100 종목 여부 (Y/N)',
                     'KRX 자동차 여부','KRX 반도체 여부','KRX 바이오 여부','KRX 은행 여부','기업인수목적회사여부',
                     'KRX 에너지 화학 여부','KRX 철강 여부','단기과열종목구분코드','KRX 미디어 통신 여부',
                     'KRX 건설 여부','(코스닥)투자주의환기종목여부','KRX 증권 구분','KRX 선박 구분',
                     'KRX섹터지수 보험여부','KRX섹터지수 운송여부','KOSDAQ150지수여부 (Y,N)','주식 기준가',
                     '정규 시장 매매 수량 단위','시간외 시장 매매 수량 단위','거래정지 여부','정리매매 여부',
                     '관리 종목 여부','시장 경고 구분 코드','시장 경고위험 예고 여부','불성실 공시 여부',
                     '우회 상장 여부','락구분 코드','액면가 변경 구분 코드','증자 구분 코드','증거금 비율',
                     '신용주문 가능 여부','신용기간','전일 거래량','주식 액면가','주식 상장 일자','상장 주수(천)',
                     '자본금','결산 월','공모 가격','우선주 구분 코드','공매도과열종목여부','이상급등종목여부',
                     'KRX300 종목 여부 (Y/N)','매출액','영업이익','경상이익','단기순이익','ROE(자기자본이익률)',
                     '기준년월','전일기준 시가총액 (억)','그룹사 코드','회사신용한도초과여부','담보대출가능여부','대주가능여부']

    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)
    os.remove(file_name)

    return df

def batch_krx_spot_kospi(base_dir, verbose = False, encoding="cp949"):
    cwd = os.getcwd()
    if (verbose): print(f"current directory is {cwd}")
    ssl._create_default_https_context = ssl._create_unverified_context

    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip",
                               base_dir + "kospi_code.zip")

    os.chdir(base_dir)
    if (verbose): print(f"change directory to {base_dir}")
    kospi_zip = zipfile.ZipFile('kospi_code.zip')
    kospi_zip.extractall()

    kospi_zip.close()

    if os.path.exists("kospi_code.zip"):
        os.remove("kospi_code.zip")

    file_name = base_dir + "kospi_code.mst"
    change_encoding(file_name, to_encoding=encoding)

    tmp_fil1 = base_dir + "kospi_code_part1.tmp"
    tmp_fil2 = base_dir + "kospi_code_part2.tmp"

    wf1 = open(tmp_fil1, mode="w", encoding=encoding)
    wf2 = open(tmp_fil2, mode="w", encoding=encoding)

    with open(file_name, mode="r", encoding=encoding) as f:
        for row in f:
            rf1 = row[0:len(row) - 228]
            rf1_1 = rf1[0:9].rstrip()
            rf1_2 = rf1[9:21].rstrip()
            rf1_3 = rf1[21:].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
            rf2 = row[-228:]
            wf2.write(rf2)
    wf2.close()

    part1_columns = ['단축코드', '표준코드', '한글명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding=encoding)

    field_specs = [2, 1, 4, 4, 4,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 9, 5, 5, 1,
                   1, 1, 2, 1, 1,
                   1, 2, 2, 2, 3,
                   1, 3, 12, 12, 8,
                   15, 21, 2, 7, 1,
                   1, 1, 1, 1, 9,
                   9, 9, 5, 9, 8,
                   9, 3, 1, 1, 1]

    part2_columns = ['그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
                     '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
                     'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
                     'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
                     'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
                     'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
                     'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
                     '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
                     '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
                     '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
                     '상장주수', '자본금', '결산월', '공모가', '우선주',
                     '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
                     '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
                     '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능여부', '대주가능여부']

    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(file_name)
    return df

from pkg.dbwrapper.mariadb import MariaDBWrapper
if __name__ == "__main__":
    base_dir = "/tmp/"
    df = batch_krx_spot_kospi(base_dir, verbose=True, encoding="utf-8")
    # sdf = df.loc[(~df['한글명'].isnull()) & (df['한글명'].str.contains('삼성전자'))].copy()
    sdf = df.loc[(~df['한글명'].isnull())].copy()

    sdf['시장유형'] = 'kospi'
    sdf['상품유형'] = 'stock'
    sdf['표시통화식별자'] = 'KRW'
    sdf['시장별종목순서'] = [i for i in range(0, sdf.shape[0])]

    db = MariaDBWrapper('localhost', 'oms', None, 'OMS')

    item_df = sdf[['단축코드', '한글명', '기준가', '시장유형', '상품유형', '표시통화식별자', '시장별종목순서']]\
        .rename(columns={'단축코드':'id', '한글명':'name', \
                         '기준가':'price', '시장유형':'market_id', \
                         '상품유형':'type', '표시통화식별자':'currency_id', \
                         '시장별종목순서' : 'seq'})
    db.insert('ITEM', item_df, key = 'id')

    market_df = pd.DataFrame([{'id' : 'kospi', 'name' : '코스피', 'info' : '한국거래소의 유가증권시장'}])
    db.insert('MARKET', market_df, key = 'id')

    snap_df = pd.DataFrame([{'market_id' : 'kospi', 'count' : item_df.shape[0], 'type' : 'SHM', 'info' : 1}])
    db.insert('MARKET_SNAP', snap_df, key = 'market_id')