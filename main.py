#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
import json
import requests
import time
import os
import platform

settings = {}


def read_json_settings():
    global settings
    with open("./settings.json", "r") as file_data:
        data = file_data.read()
        settings = eval(data)


def add_domain_name_value(ip):
    client = AcsClient(settings["accessKeyId"], settings["accessSecret"],
                       settings["regionId"])
    request = AddDomainRecordRequest()
    request.set_DomainName(settings["domain_name"])
    request.set_RR(settings["secondary_domain"])
    request.set_Type("A")
    request.set_Value(ip)

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
    print("************新增完成************")


def update_domain_name_value(RecordId, ip):
    client = AcsClient(settings["accessKeyId"], settings["accessSecret"],
                       settings["regionId"])
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordId)
    request.set_RR(settings["secondary_domain"])
    request.set_Type("A")
    request.set_Value(ip)

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
    print("************更新完成************")


def get_domain_name_list():
    client = AcsClient(settings["accessKeyId"], settings["accessSecret"],
                       settings["regionId"])
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(settings["domain_name"])
    response = client.do_action_with_exception(request)
    data_json = json.loads(str(response, encoding='utf-8'))
    for i in data_json["DomainRecords"]["Record"]:
        if i["RR"] == settings["secondary_domain"]:
            return_data = [i["RecordId"], i["Value"]]
            return return_data
    return_data = ["", ""]
    return return_data


def get_ip_addr():
    session = requests.Session()
    session.trust_env = False
    ip = session.get("http://ip.42.pl/raw")
    return ip.text


def run():
    read_json_settings()
    while True:
        try:
            update_ip = get_ip_addr()
            inquire = get_domain_name_list()
            current_ip = inquire[1]
            RecordId = inquire[0]
            if RecordId == "":
                add_domain_name_value(ip=update_ip)
            elif current_ip != update_ip:
                update_domain_name_value(RecordId=RecordId, ip=update_ip)
        except Exception as e:
            print(e)
        time.sleep(settings["sleep_time"])


if __name__ == '__main__':
    run()
