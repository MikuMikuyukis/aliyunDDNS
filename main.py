#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import json
import requests
import time
import os

settings = {}


def read_json_settings():
    # 读取配置文件
    global settings
    for i in range(3):
        try:
            with open("./settings.json", "r") as file_data:
                data = file_data.read()
                settings = eval(data)
                return
        except Exception as e:
            print(e)


def network_test():
    # 网络测试
    while True:
        ping_test = os.system("ping {} -c1".format(settings["networkTestAddr"]))
        if ping_test == 0:
            return True

        else:
            return False


def update_domain_name_value(RecordId, ip):
    # 更新域名解析记录
    while True:
        try:
            client = AcsClient(settings["accessKeyId"], settings["accessSecret"], 'cn-hangzhou')
            request = UpdateDomainRecordRequest()
            request.set_accept_format('json')
            request.set_RecordId(RecordId)
            request.set_RR(settings["secondary_domain"])
            request.set_Type("A")
            request.set_Value(ip)
            response = client.do_action_with_exception(request)
            print(str(response, encoding='utf-8'))
            print("************updateOK************")
            return
        except Exception as e:
            print(e)
            time.sleep(5)


def get_domain_name_list():
    # 获取域名列表、RecordID
    while True:
        try:
            client = AcsClient(settings["accessKeyId"], settings["accessSecret"], 'cn-hangzhou')
            request = DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(settings["domain_name"])
            response = client.do_action_with_exception(request)
            data_json = json.loads(str(response, encoding='utf-8'))
            for i in data_json["DomainRecords"]["Record"]:
                if i["RR"] == settings["secondary_domain"]:
                    return_data = [i["RecordId"], i["Value"]]
                    return return_data
            print("请确认配置是否正确")
            exit()
        except Exception as  e:
            print(e)


def get_ip_addr():
    # 获取公网ip地址
    try:
        ip = requests.get("http://ip.42.pl/raw")
        return ip.text
    except Exception as e:
        print(e)


def run():
    # 执行
    read_json_settings()
    while True:
        if network_test():
            update_ip = get_ip_addr()
            inquire = get_domain_name_list()
            current_ip = inquire[1]
            RecordId = inquire[0]
            if current_ip != update_ip:
                current_ip = update_ip
                update_domain_name_value(RecordId=RecordId, ip=update_ip)
            time.sleep(settings["sleep_time"])


if __name__ == '__main__':
    run()
