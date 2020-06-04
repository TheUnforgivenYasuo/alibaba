#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/18 21:27
# @Author : J.D.Allen
# @Site : 
# @File : ali_get.py
# @Software: PyCharm
# @Phone: 17664166105
# @Email: is_a_store@163.com


import requests
import bs4
import time
import xlwt
import random


def get_urls(url, page):
    """获取查询商品的每家店的地址"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}
    html = requests.get(url=url + "&beginPage=" + str(page), headers=headers, timeout=10).text
    soup = bs4.BeautifulSoup(html, "lxml")
    tables = soup.find('div', attrs={'id': 'sw_mod_mainblock'})
    table = tables.find('ul').find_all('div', class_='list-item-left')
    # print(table)
    urls = []
    for items in table:
        item = items.find('a').get('href')
        # print(item)
        urls.append(item)
    # print(urls)
    # url_1 = random.choice(urls)
    # print(url_1)
    return urls


def get_contact(url_1):
    """ 获取每家店的联系方式 """
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    session = requests.session()
    try:
        html = session.get(url_1, headers=headers, timeout=10).text
        contact_url = bs4.BeautifulSoup(html, 'lxml').find('div', class_='top-nav-bar-box').find('li', attrs={
            'data-page-name': 'contactinfo'}).find('a').get('href')
        # print(contact_url)
    except BaseException:
        print('-----------------')
        return
    try:
        html = session.get(contact_url, headers=headers,timeout=10).text
        table = bs4.BeautifulSoup(html, 'lxml').find('div', class_='fd-line').find_all('dl')
        title = bs4.BeautifulSoup(html, 'lxml').find('div', class_='contact-info').find('h4').get_text()
        info = []
        for item in table[:-1]:
            info.append(item.get_text().replace('\n', '').replace('\xa0', ''))
        # print(info)
        return (title, info)
    except:
        print("~~~~~~~~~~~~~~~~~~~")

def main():
    url = "http://s.1688.com/company/company_search.htm?keywords=%BE%AB%C3%DC%BB%FA%D0%B5&earseDirect=false&button_click=top&n=y&pageSize=30"
    for j in range(100):
        urls = get_urls(url,j)
        for i in range(0, len(urls) - 1):
            url_1 = urls[i]
            data = get_contact(url_1)


if __name__ == "__main__":
    main()