# coding:utf-8
import requests
import bs4
import time
import xlwt
import random


def get_IP():
    """获取代理IP
    """
    url = "http://www.xicidaili.com/nn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive', }
    session = requests.session()
    html = session.get(url, headers=headers).text
    table = bs4.BeautifulSoup(html, 'lxml')
    IP_lists = table.find('table', attrs={'id': 'ip_list'}).find_all('tr')
    ip_list = []
    for IP_list in IP_lists[1:]:
        lists = IP_list.find_all('td')
        ip = {'ip': '', 'port': ''}
        if lists[5].text == 'HTTP':
            ip['ip'] = lists[1].text
            ip['port'] = lists[2].text
            ip_list.append(ip)
            print(ip_list)
    return ip_list


def get_urls(url, page, ip):
    """获取查询商品的每家店的地址"""
    proxy = {'http': "http://" + ip['ip'] + ":" + ip['port']}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}
    html = requests.get(url=url + "&beginPage=" + str(page), headers=headers, proxy=proxy, timeout=10).text
    soup = bs4.BeautifulSoup(html, "lxml")
    tables = soup.find('div', attrs={'id': 'sw_mod_mainblock'})
    table = tables.find('ul').find_all('div', class_='list-item-left')
    urls = []
    for item in table:
        urls.append(table.find('a').get('href'))
    print(urls)
    url_1 = random.choice(urls)
    return url_1


def get_contact(url_1, ip):
    """ 获取每家店的联系方式 """
    proxy = {'http': 'http://' + ip['ip'] + ip['port']}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}
    session = requests.session()
    try:
        html = session.get(url_1, headers=headers, proxy=proxy, timeout=10).text()
        contact_url = bs4.BeautifulSoup(html, 'lxml').find('div', class_='top-nav-bar-box').find('li', attrs={
            'data-page-name': 'contactinfo'}).find('a').get('href')
    except BaseException:
        print('-----------------')
        return
    try:
        html = session.get(contact_url, headers=headers, proxy=proxy, timeout=10).text()
        table = bs4.BeautifulSoup(html, 'lxml').find('div', class_='fd-line').find_all('dl')
        title = bs4.BeautifulSoup(html, 'lxml').find('div', class_='contact-info').find('h4').get_text()
        info = []
        for item in table[:-1]:
            info.append(item.get_text().replace('\n', '').replace(' ', ''))
        return info
    except:
        print("~~~~~~~~~~~~~~~~~~~")


def main():
    url = "http://s.1688.com/company/company_search.htm?keywords=%BE%AB%C3%DC%BB%FA%D0%B5&earseDirect=false&button_click=top&n=y&pageSize=30"
    ip = get_IP()
    url_1 = get_urls(url, 1, ip[0])
    data = get_contact(url_1, ip)


if __name__ == "__main__":
    main()