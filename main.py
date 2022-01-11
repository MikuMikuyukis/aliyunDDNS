#!/usr/bin/env python
# coding=utf-8

import json
import logging
import time
import threading

import requests
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from health import run_health_server

settings = {}

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)


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
    logging.info(str(response, encoding='utf-8'))
    logging.info("新增完成")


def update_domain_name_value(record_id, ip):
    client = AcsClient(settings["accessKeyId"], settings["accessSecret"],
                       settings["regionId"])
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(record_id)
    request.set_RR(settings["secondary_domain"])
    request.set_Type("A")
    request.set_Value(ip)

    response = client.do_action_with_exception(request)
    logging.info(str(response, encoding='utf-8'))
    logging.info("更新完成")


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
            new_ip = get_ip_addr()
            inquire = get_domain_name_list()
            current_ip = inquire[1]
            record_id = inquire[0]
            logging.info("new_ip: %s current_ip: %s record_id: %s", new_ip, current_ip, record_id)
            if record_id == "":
                add_domain_name_value(ip=new_ip)
            elif current_ip != new_ip:
                update_domain_name_value(record_id=record_id, ip=new_ip)
        except Exception as e:
            logging.exception(u"{}".format(e))
        time.sleep(settings["sleep_time"])


if __name__ == '__main__':
    # health
    threading.Thread(target=run_health_server, name="health").start()
    # ddns
    run()
