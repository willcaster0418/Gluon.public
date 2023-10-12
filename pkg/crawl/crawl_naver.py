import requests
import time
from bs4 import BeautifulSoup as bs
from pkg.crawl.crawl import Crawl

class CrawlNaver(Crawl):
    def __init__(self):
        super().__init__()
        return

    def get_daily_snap(self, code = "005930", offset = 0, filter = {"Date" : 0, "Close" : 2, "Volume(qty)" : 1}):
        columns = ["Date", "Close", "N/A", "Open", "High", "Low", "Volume(qty)"]
        url = f"https://finance.naver.com/item/sise_day.nhn?code={code}"
        result_dict = {}
        for key in filter.keys():
            coffset = columns.index(key)
            css_selector = f"body > table.type2 > tr:nth-of-type({3 + offset}) > td:nth-of-type({1+coffset}) > span"
            v = super().get(url, css_selector)
            if filter[key] == 0:
                result_dict[key] = v
            elif filter[key] == 1:
                result_dict[key] = int(v.replace(",", ""))
            elif filter[key] == 2:
                result_dict[key] = float(v.replace(",", ""))

        return result_dict

    def get_minute_snap(self, code = "005930", time = None, page = 1, offset = 0, filter = {"Time" : 0, "Price" : 2, "Qty" : 1}):
        columns = ["Time", "Price", "Qty"]
        if time == None:
            import datetime
            time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        url = f"https://finance.naver.com/item/sise_time.naver?code={code}&thistime={time}&page={page}"
        result_dict = {}
        for key in filter.keys():
            coffset = columns.index(key)
            css_selector = f"body > table.type2 > tr:nth-of-type({3 + offset}) > td:nth-of-type({1+coffset})"
            v = super().get(url, css_selector)
            if filter[key] == 0:
                result_dict[key] = v
            elif filter[key] == 1:
                result_dict[key] = int(v.replace(",", ""))
            elif filter[key] == 2:
                result_dict[key] = float(v.replace(",", ""))

        return result_dict

    def get_articles(self, keyword = None):
        sid_list = [sid for sid in range(259, 264)]
        result = []
        for sid in sid_list:
            url_finance = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2={sid}"
            css_selector = "#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-of-type(2) > a"
            title_list = [(ele.text, ele['href']) for ele in super().get(url_finance, css_selector, need_list = True)]
            #print(sid, title_list)
            article_list = [{"title" : title[0], "url" : title[1], "article" : self.get_article(title[1])} for title in title_list]
            result += article_list
        return result

    def get_article(self, url = ""):
        css_selector = "#dic_area"
        return super().get(url, css_selector)

    def get_usa_bond_yield(self, maturity = "1Y", dtype = "value"):
        headers = {"Content-Type" : "application/json", "Connect" : "Close"}
        valid_maturities = ["1M", "2M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
        if dtype == "list":
            return valid_maturities
        if maturity not in valid_maturities:
            raise ValueError(f"Invalid maturity. Valid maturities are {valid_maturities}")
        url = f"https://m.stock.naver.com/marketindex/bond/US{maturity}T=RR"
        html = requests.get(url, headers = headers)
        html_soup = bs(html.text, "html.parser")
        css_selector = "#__next > div.DetailInfo_article__2XNzs > div > div.DetailInfo_infoPrice__ODLC6 > strong"
        ele = html_soup.select(css_selector)
        return float(ele[0].text)

    def kr_bond_yield(self, maturity = "1Y", dtype = "value"):
        headers = {"Content-Type" : "application/json", "Connect" : "Close"}
        valid_maturities = ["1Y", "2Y", "3Y", "4Y", "5Y", "10Y", "20Y", "30Y", "50Y"]
        if dtype == "list":
            return valid_maturities
        if maturity not in valid_maturities:
            raise ValueError(f"Invalid maturity. Valid maturities are {valid_maturities}")
        url = f"https://m.stock.naver.com/marketindex/bond/KR{maturity}T=RR"
        html = requests.get(url, headers = headers)
        html_soup = bs(html.text, "html.parser")
        css_selector = "#__next > div.DetailInfo_article__2XNzs > div > div.DetailInfo_infoPrice__ODLC6 > strong"
        ele = html_soup.select(css_selector)
        return float(ele[0].text)

    def get_usa_bond_yield_dict(self):
        for m in self.get_usa_bond_yield(dtype = "list"):
            yield m, self.get_usa_bond_yield(maturity = m)

    def kr_bond_yield_dict(self):
        for m in self.kr_bond_yield(dtype = "list"):
            yield m, self.kr_bond_yield(maturity = m)

    def snap_krx(self, url = "https://finance.naver.com/sise/sise_market_sum.naver?",
                 info = {}, filter = {"현재가" : "close"}, sosok=0, page = 1):
        market_data = {}
        html = requests.get(url + f"sosok={sosok}&page={page}", headers = self.get_header())
        html_soup = bs(html.text, "html.parser")
        datas = html_soup.select("table[class='type_2'] > thead > tr > th")
        data_keys = [data.text for data in datas]
        datas = html_soup.select("table[class='type_2'] > tbody > tr")
        for data in datas:
            if "href" in str(data):
                tmpsoup = bs(str(data), "html.parser")
                data_dict = {}
                idx = 0
                for tmpdata in tmpsoup.find_all("td"):
                    try:
                        if tmpdata.has_attr("class"):
                            if tmpdata['class'][0] == "no":
                                data_dict[data_keys[idx]] = int(tmpdata.text)
                            elif tmpdata['class'][0] == "number":
                                data_dict[data_keys[idx]] = float(tmpdata.text.replace(",", "").replace("\n", "").replace("%",""))
                        if not data_keys[idx] in data_dict.keys():
                            data_dict[data_keys[idx]] = tmpdata.text
                            if data_keys[idx] == "종목명":
                                data_dict['code'] = tmpdata.select("a")[0]['href'].replace("/item/main.naver?code=", "")
                    except Exception as e:
                        if data_keys[idx] == "종목명":
                            data_dict['code'] = None
                        data_dict[data_keys[idx]] = None
                        pass
                    idx += 1
                if data_dict['code'] != None:
                    data_dict['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    if data_dict['code'] in market_data.keys():
                        market_data[data_dict['code']].update(data_dict)
                    else:
                        market_data[data_dict['code']] = data_dict
        market_data = {k : {filter[f] : v for f, v in v.items() if f in filter.keys()} for k, v in market_data.items()}
        for data in market_data.values():
            data.update(info)
        return market_data

    def get_last_page(self, url = "https://finance.naver.com/sise/sise_market_sum.naver?&", sosok=0):
        headers = {"Content-Type" : "application/json", "Connect" : "Close"}
        html = requests.get(url + f"sosok={sosok}", headers = headers)
        html_soup = bs(html.text, "html.parser")
        data = html_soup.select("td > a")
        return int(data[-1]['href'][-2:])

if __name__ == "__main__":
    c = CrawlNaver()
    print(c.snap_krx(page=1))
    print(c.snap_krx(page=2))
    print(c.snap_krx(page=3))