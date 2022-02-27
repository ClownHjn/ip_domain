#!/usr/bin/python
# -*- coding: UTF-8 -*-

from requests_html import HTMLSession 
import time,os,json,urllib3,re,IPy
import argparse
urllib3.disable_warnings()


def main():
    os.environ["http_proxy"] = "http://127.0.0.1:10080"
    os.environ["https_proxy"] = "http://127.0.0.1:10080"
    # ip = str(input("请输入IP或者网段:"))
    # x = ['14.215.177.39','45.43.32.234','127.0.0.1']  
    ip = '128.1.84.0/24'
    x = ip_data(ip)
    domain_data = url_data(x)
    json_data(domain_data)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("square",help="echo the string you use here",type=int)
    args = parser.parse_args()
    print(args.square**2)


def ip_data(ip):
    Network_segment = IPy.IP(ip)
    ip_list = []
    if Network_segment.iptype() == "PRIVATE":
        print("地址有误,请输入公网地址")
        exit()
    if len(Network_segment) > 1:
        for ip in Network_segment:
            ip_list.append(str(ip))
    else:
        ip_list.append(ip)
    return ip_list

def file_ip(ip):
    pass 
    # 将文件转换成ip


def url_data(ip_data):
    req = HTMLSession()
    # 构建请求头
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
    }
    # https://site.ip138.com/
    # 定义循环次数，根据传入的ip值
    ip_count = len(ip_data)
    domain_data = {}
    while ip_count > 0:
        ip_count  -= 1
        try:
            url = req.get('https://site.ip138.com/' + str(ip_data[ip_count - 1]),headers=headers,timeout=10)
            print(url)
        except Exception as e:
            print("请求超时，IP被封......")
            break
        # count = 2 
        # try:
        # 提却域名的页面元素
        url_find = url.html.find('ul#list > li > a')
        # 获取当前反查的ip
        temp_ip_data = ip_data[ip_count -1]
        temp_domain = []
        # 遍历域名
        for i in range(0,len(url_find)):   
            url_data = url_find[i].text 
            # 将域名暂时放置在列表中
            temp_domain.append(url_data)
        # print(temp_ip_data)
        # 用字典将域名和IP对应存储
        domain_data[temp_ip_data] = {"domains":temp_domain}
        # print(domain_data)
        # except IndexError as a:
        #     print("异常错误！！！ 请检查是否开启代理")
        #     continue
        # # print(url_data)
        # print(ip_count)
        time.sleep(1.5)    
    return domain_data 

def json_data(domain_data):
    filename = "IP_for_domain_result.json"
    json_file = open(filename,"w")
    json.dump(domain_data,json_file,indent=4,sort_keys=True)
    json_file.close()






if __name__ == '__main__':
    # parseArgs()
    main()