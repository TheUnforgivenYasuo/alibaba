#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/16 20:03
# @Author : J.D.Allen
# @Site : 
# @File : ali_get_store_info.py
# @Software: PyCharm
# @Phone: 17664166105
# @Email: is_a_store@163.com


import requests, csv, time, logging
from lxml import etree
from urllib.parse import quote



class make_time_str(object):
    now_datetime_str = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    now_datetime_code = str(int(round(time.time() * 1000)))

class KEYWORD_OBJ(object):
    PROXY_IP = 'proxy_ip'
    PROXY_PORT = 'proxy_port'
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    STORENAME = 'store_name'
    STOREADDRESS = 'store_address'
    STOREURL = 'store_url'


logging.basicConfig(
    level=logging.INFO,
    filename='ali_getinfo_%s.log' % make_time_str.now_datetime_code,
    format='%(asctime)s-%(funcName)s-%(lineno)d-%(levelname)s:>>>%(message)s'
)

logger = logging.getLogger(__name__)

# logger.info("Start print log")
# logger.debug("Do something")
# logger.warning("Something maybe fail.")
# logger.info("Finish")


def get_proxy_ip():

    """
    获取代理IP
    """
    logger.info("get_proxy_ip start")
    get_proxy_url = "http://www.xicidaili.com/nn/"

    get_proxy_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
    }

    get_proxy_session = requests.session()
    get_proxy_obj = get_proxy_session.get(get_proxy_url, headers=get_proxy_headers)
    get_proxy_html = get_proxy_obj.text
    get_proxy_html_x = etree.HTML(get_proxy_html)
    proxy_x = get_proxy_html_x.xpath('//tr[@class="odd"]')
    proxy_http_list = []
    proxy_https_list = []
    for one_proxy_x in proxy_x:
        proxy_ip = one_proxy_x.xpath('normalize-space(.//td[2])')
        proxy_port = one_proxy_x.xpath('normalize-space(.//td[3])')
        proxy_code = one_proxy_x.xpath('normalize-space(.//td[6])')
        if str(proxy_code).upper() == KEYWORD_OBJ.HTTP:
            proxy_http_list.append({KEYWORD_OBJ.PROXY_IP: str(proxy_ip), KEYWORD_OBJ.PROXY_PORT: str(proxy_port)})
        elif str(proxy_code).upper() == KEYWORD_OBJ.HTTPS:
            proxy_https_list.append({KEYWORD_OBJ.PROXY_IP: str(proxy_ip), KEYWORD_OBJ.PROXY_PORT: str(proxy_port)})
    logger.info("get_proxy_ip end")

    return {KEYWORD_OBJ.HTTP: proxy_http_list, KEYWORD_OBJ.HTTPS: proxy_https_list}



def csv_dumpers(csv_row, csv_name):
    file = open(csv_name, 'a', newline='')  # 打开文件
    content = csv.writer(file, dialect='excel')  # 设定文件写入模式
    content.writerow(csv_row)  # 写入具体内容


def get_ali_keyword(keyword, page_num, cookies_text):
    """获取查询商品的每家店的地址"""
    proxy_ip_obj = get_proxy_ip()
    ip_list = proxy_ip_obj[KEYWORD_OBJ.HTTP]
    ali_keyword_url = "http://s.1688.com/company/company_search.htm?keywords={keyword}&earseDirect=false&button_click=top&n=y&pageSize=30&beginPage={page_num}"
    ali_keyword_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    store_info_list = []
    cookies = cookies_spilt(cookies=cookies_text)
    for ip_dict in ip_list:
        try:
            proxy = {'http': "http://{IP}:{PORT}".format(IP=ip_dict[KEYWORD_OBJ.PROXY_IP], PORT=ip_dict[KEYWORD_OBJ.PROXY_PORT])}
            get_ali_keyword_obj = requests.get(
                url=ali_keyword_url.format(keyword=quote(str(keyword).encode('gbk')), page_num=str(page_num)),
                headers=ali_keyword_headers,
                proxies=proxy,
                cookies=cookies,
                timeout=10
            )
            get_ali_keyword_html = get_ali_keyword_obj.text
            ali_keyword_html_x = etree.HTML(get_ali_keyword_html)
            ali_store_info_list_x = ali_keyword_html_x.xpath('//ul[@class="sm-company-list fd-clr"]/li')

            for one_ali_store_info in ali_store_info_list_x:
                store_name = one_ali_store_info.xpath('.//a[@class="list-item-title-text"]/@title')[0]
                store_url = str(one_ali_store_info.xpath('.//a[@class="list-item-title-text"]/@href')[0]) + '/page/contactinfo.htm'
                store_address = one_ali_store_info.xpath('.//a[@class="sm-offerResult-areaaddress"]/@title')[0]
                store_info_list.append({
                    KEYWORD_OBJ.STORENAME: store_name,
                    KEYWORD_OBJ.STOREADDRESS: store_address,
                    KEYWORD_OBJ.STOREURL: store_url
                })
        except Exception as e:
            logger.info("get_keyword error:>>> %s" % str(e))
            continue
    return store_info_list


def get_store_phone(store_info_list, cookies_text, file_name):


    cookies = cookies_spilt(cookies=cookies_text)
    store_info_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    for one_store_info in store_info_list:
        store_phone_url = one_store_info[KEYWORD_OBJ.STOREURL]
        one_store_info_v = one_store_info.values()
        proxy_ip_obj = get_proxy_ip()
        ip_list = proxy_ip_obj[KEYWORD_OBJ.HTTPS]
        for ip_dict in ip_list:
            try:
                proxy = {'https': "https://{IP}:{PORT}".format(
                    IP=ip_dict[KEYWORD_OBJ.PROXY_IP],
                    PORT=ip_dict[KEYWORD_OBJ.PROXY_PORT]
                )}
                get_ali_store_obj = requests.get(
                    url=store_phone_url,
                    headers=store_info_headers,
                    proxies=proxy,
                    cookies=cookies,
                    timeout=10
                )
                get_ali_store_html = get_ali_store_obj.text
                ali_store_html_x = etree.HTML(get_ali_store_html)
                ali_store_info_list_x = ali_store_html_x.xpath('//div[@class="contcat-desc"]/dl')
                store_info_list = []
                store_info_list.extend(list(one_store_info_v))
                for one_ali_store_info in ali_store_info_list_x:
                    store_key_name = str(one_ali_store_info.xpath('normalize-space(.//dt)')).replace(' ', '')
                    store_value_name = one_ali_store_info.xpath('normalize-space(.//dd)')
                    store_info_list.extend([str(store_key_name), str(store_value_name)])
                store_info_list = [str(x).replace('\xa0', '') for x in store_info_list]
                csv_dumpers(csv_row=store_info_list, csv_name=file_name)
                break
            except Exception as e:
                logger.info("get_phone error:>>> %s" % str(e))
                continue
    logger.info("%s success" % file_name)


def cookies_spilt(cookies):
    cookies_list = str(cookies).split(';')
    cookies_dict = {}
    for onecook in cookies_list:
        onecook_list = onecook.split('=')
        cookies_dict.update({onecook_list[0]: onecook_list[1]})
    return cookies_dict


def main():
    fp = open('get_ali.conf', 'r', encoding='utf-8')
    content = fp.read()
    fp.close()
    conf_obj = content.split('|')
    keyword = conf_obj[0]
    page_num = conf_obj[1]
    file_name = keyword + '-' + make_time_str.now_datetime_code + '.csv'
    cookies_text = conf_obj[2]
    if int(page_num) > 1:
        for one_page in range(0, int(page_num)):
            ali_keyword_store = get_ali_keyword(keyword=keyword, page_num=str(one_page+1), cookies_text=cookies_text)
            if len(ali_keyword_store) > 0:
                get_store_phone(store_info_list=ali_keyword_store, cookies_text=cookies_text, file_name=file_name)
            else:
                logger.info("ali_keyword_store is none file_name error:>>> %s" % file_name)
    else:
        ali_keyword_store = get_ali_keyword(keyword=keyword, page_num=1, cookies_text=cookies_text)
        if len(ali_keyword_store) > 0:
            get_store_phone(store_info_list=ali_keyword_store, cookies_text=cookies_text, file_name=file_name)
        else:
            logger.info("ali_keyword_store is none file_name error:>>> %s" % file_name)



if __name__ == '__main__':
    main()
