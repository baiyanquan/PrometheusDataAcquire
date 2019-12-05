#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: metrics2csv.py

import csv
import requests
import sys
import getopt
import time
import logging

PROMETHEUS_URL =  'http://10.60.38.181:13002'
PROMETHEUS_URL2 = 'http://10.60.38.181:13001'
CONTAINERLIST = ['docker-compose_carts-db_1','docker-compose_carts_1','docker-compose_catalogue-db_1',
 'docker-compose_catalogue_1','docker-compose_edge-router_1','docker-compose_front-end_1','docker-compose_kibana_1',
 'docker-compose_orders-db_1','docker-compose_orders_1','docker-compose_payment_1','docker-compose_queue-master_1',
 'docker-compose_rabbitmq_1', 'docker-compose_shipping_1','docker-compose_user-db_1','docker-compose_user_1']
INSTANCELIST = ['carts:80','catalogue:80','edge-router:80','orders:80','payment:80','shipping:80','user:80']
QUERY_API = '/api/v1/query'
RANGE_QUERY_API = '/api/v1/query_range'
RESOLUTION = '10'  # default: 10s
OUTPUTFILE = 'result.csv'  # default: result.csv
START = '1541661496'  # rfc3339 | unix_timestamp
END = '1541661496'  # rfc3339 | unix_timestamp
START_STR = '2018-11-24 15:00:00'
END_STR = '2018-11-24 20:00:00'
PERIOD = "" #1440  # unit: miniute, default 60, Resolution=10s

TiandiMetricNames = [
    'container_fs_io_current',
    'container_fs_usage_bytes',
    'container_fs_reads_bytes_total',
    'container_fs_writes_bytes_total',
    'memory_usage',
    'network_receive_bytes',
    'network_transmit_bytes',
    'cpu_usage_percent',
    'memory_cache_usage_bytes'
    ]
#2针对url2
TiandiMetricNames2 = [
    'request_duration_seconds_count',
    'request_duration_seconds_bucket'
]
TiandiQueryList = [
    'container_fs_io_current{name="%s"}',
    'container_fs_usage_bytes{name="%s"}',
    'sum by (name) (rate(container_fs_reads_bytes_total{name="%s"}[1m]))',
    'sum by (name) (rate(container_fs_writes_bytes_total{name="%s"}[1m]))',
    'container_memory_usage_bytes{name = "%s"}',
    'sum by (name) (rate(container_network_receive_bytes_total{name="%s",container_label_org_label_schema_group=""}[1m]))',
    'sum by (name) (rate(container_network_transmit_bytes_total{name="%s",container_label_org_label_schema_group=""}[1m]))',
    'sum by (name) (rate(container_cpu_usage_seconds_total{image!="",name="%s",container_label_org_label_schema_group=""}[1m]))',
    #1m指1分钟
    'container_memory_cache{name="%s",container_label_org_label_schema_group=""}',
    ]
TiandiQueryList2 = [
    'sum by (instance) (rate(request_duration_seconds_count{instance="%s"}[1m]))',
    'sum by (instance) (rate(request_duration_seconds_bucket{instance="%s"}[1m]))'
]



def handle_args(argv):
    global PROMETHEUS_URL
    global OUTPUTFILE
    global CONTAINERLIST
    global RESOLUTION
    global START
    global END
    global PERIOD
    global INSTANCELIST

    try:
        opts, args = getopt.getopt(argv, "h:o:c:s:",
                                   ["host=", "outfile=", "container=", "step=", "help", "start=", "end=", "period=","instancelist="])
    except getopt.GetoptError as error:
        logging.error(error)
        print_help_info()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--help":
            print_help_info()
            sys.exit()
        elif opt in ("-h", "--host"):
            PROMETHEUS_URL = arg
        elif opt in ("-o", "--outfile"):
            OUTPUTFILE = arg
        elif opt in ("-c", "--containerlist"):
            CONTAINERLIST = arg
        elif opt in ("-s", "--step"):
            RESOLUTION = arg
        elif opt == "--start":
            START = arg
        elif opt == "--end":
            END = arg
        elif opt == "--period":
            PERIOD = int(arg)
        elif opt == "--instancelist":
            INSTANCELIST = int(arg)

    if PROMETHEUS_URL == '':
        logging.error(
            "You should use -h or --host to specify your prometheus server's url, e.g. http://prometheus:9090")
        print_help_info()
        sys.exit(2)
    elif CONTAINERLIST == '':
        logging.error(
            "You should use -c or --containerlist to specify the names of the container which you want to query all the metrics of")
        print_help_info()
        sys.exit(2)

    if OUTPUTFILE == '':
        OUTPUTFILE = 'result.csv'
        logging.warning("You didn't specify output file's name, will use default name %s", OUTPUTFILE)
    if RESOLUTION == '':
        RESOLUTION = '10s'
        logging.warning("You didn't specify query resolution step width, will use default value %s", RESOLUTION)
    if PERIOD == '' and START == '' and END == '':
        PERIOD = 10
        logging.warning(
            "You didn't specify query period or start&end time, will query the latest %s miniutes' data as a test",
            PERIOD)


def print_help_info():
    print('')
    print('Metrics2CSV Help Info')
    print('    metrics2csv.py -h <prometheus_url> -c <container_name_LIST> [-o <outputfile>]')
    print('or: metrics2csv.py --host=<prometheus_url> --container=<container_name> [--outfile=<outputfile>]')
    print('---')
    print(
        'Additional options: --start=<start_timestamp_or_rfc3339> --end=<end_timestamp_or_rfc3339> --period=<get_for_most_recent_period(int miniutes)>')
    print('                    use start&end or only use period')




def query_tiandi_metric_names():
    metricName=[]
    #将container名字和列名结合
    for containerName in range(len(CONTAINERLIST)):
        for index in range(len(TiandiMetricNames)):
            metricName.append(CONTAINERLIST[containerName]+"/"+TiandiMetricNames[index])
    for instanceName in range(len(INSTANCELIST)):
        for index in range(len(TiandiMetricNames2)):
            metricName.append(INSTANCELIST[instanceName] + "/" + TiandiMetricNames2[index])
    print(metricName)
    return metricName

def query_tiandi_metric1_names():
    metricName=[]
    #将container名字和列名结合
    for containerName in range(len(CONTAINERLIST)):
        for index in range(len(TiandiMetricNames)):
            metricName.append(CONTAINERLIST[containerName]+"/"+TiandiMetricNames[index])
    print(metricName)
    return metricName

def query_tiandi_metric2_names():
    metricName=[]
    #将container名字和列名结合
    for instanceName in range(len(INSTANCELIST)):
        for index in range(len(TiandiMetricNames2)):
            metricName.append(INSTANCELIST[instanceName] + "/" + TiandiMetricNames2[index])
    print(metricName)
    return metricName



#处理1的数据
def query_tiandi_metric_values1(metricnames,end_time,start_time):
    csvset = dict()
    for index in range(len(metricnames)):
        list = metricnames[index].split('/')
        #print(list[0]+"    "+list[1])
        #print(TiandiQueryList[index % len(TiandiQueryList)])
        response = requests.get(PROMETHEUS_URL + RANGE_QUERY_API,
                                params={'query': TiandiQueryList[index % len(TiandiQueryList)] % list[0], 'start': start_time,
                                        'end': end_time, 'step': RESOLUTION}, auth=('admin', 'admin'))

        print(response)
        results = response.json()['data']['result']
        #print(results)
        if results != []:
            for value in results[0]['values']:
                if index == 0:
                    csvset[value[0]] = [value[1]]
                else:
                    if value[0] in csvset :
                        csvset[value[0]].append(value[1])
        else:
            for index in range(end_time, start_time, -10):
                if index in csvset:
                    csvset[index].append("null")
        #按竖列输出的数据！！！null代表没有该项数据
    return csvset

#处理2的数据
def query_tiandi_metric_values2(metricnames,end_time,start_time):
    csvset = dict()
    for index in range(len(metricnames)):
        list = metricnames[index].split('/')
        query = TiandiQueryList2[index % len(TiandiQueryList2)] % list[0]
        response = requests.get(PROMETHEUS_URL2 + RANGE_QUERY_API,
                                params={'query': TiandiQueryList2[index % len(TiandiQueryList2)] % list[0], 'start': start_time,
                                        'end': end_time, 'step': RESOLUTION}, auth=('admin', 'admin'))

        print(response)
        results = response.json()['data']['result']
        #print(results)
        if results != []:
            for value in results[0]['values']:
                if index == 0:
                    csvset[value[0]] = [value[1]]
                else:
                    if value[0] in csvset:
                        csvset[value[0]].append(value[1])
        else:
            for index in range(end_time,start_time,-10):
                if index in csvset:
                    csvset[index].append("null")
        #按竖列输出的数据！！！null代表没有该项数据
    return csvset


#写csv
def write2csv(filename, metricnames, dataset1,dataset2):
    global PERIOD
    global RESOLUTION

    if PERIOD != '':
        times = PERIOD * 60 / int(RESOLUTION)
    else:
        times = datetime_timestamp(END_STR)-datetime_timestamp(START_STR) / int(RESOLUTION)

    num=0
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp'] + metricnames)
        for timestamp in sorted(dataset1.keys(), reverse=True):
            num = num + 1
            if (num>times): break
            if timestamp in dataset2:
                writer.writerow([timestamp] + dataset1[timestamp]+dataset2[timestamp])
        #for timestamp in sorted(dataset2.keys(), reverse=True):
        #    writer.writerow([timestamp] + dataset2[timestamp])


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)

def main():
    handle_args(sys.argv[1:])
    #处理参数
    # metricnames = query_metric_names()
    metricnames = query_tiandi_metric_names()
    #处理抬头
    logging.info("Querying metric names succeeded, metric number: %s", len(metricnames))
    # csvset = query_metric_values(metricnames=metricnames)
    metricnames1 = query_tiandi_metric1_names()
    metricnames2 = query_tiandi_metric2_names()


    #处理开始时间和结束时间
    if PERIOD != '':
        end_time = int(time.time())
        start_time = end_time - 60 * PERIOD
    else:
        #end_time = END
        #start_time = START
        end_time = datetime_timestamp(END_STR)
        start_time = datetime_timestamp(START_STR)

    csvset1 = query_tiandi_metric_values1(metricnames=metricnames1, end_time = end_time , start_time = start_time)
    csvset2 = query_tiandi_metric_values2(metricnames=metricnames2, end_time = end_time , start_time = start_time)
    #print(csvset1)
    #print(csvset2)
    #dataset = dict(csvset2, **csvset1)
    #生成数据集
    logging.info("Querying metric values succeeded, rows of data: %s", len(csvset1))
    write2csv(filename=OUTPUTFILE, metricnames=metricnames, dataset1=csvset1,dataset2=csvset2)
    #写文件

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()