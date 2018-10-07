#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import datetime as dt
import pymongo


class FeatureRecord:
    def __init__(self, _user, _host, _display, _year, _month, _day, _hour, _minute, _linger, _lic_count):
        self.m_user = _user
        self.m_host = _host
        self.m_display = _display
        self.m_lic_count = int(_lic_count) if _lic_count else 0
        self.m_start_datetime = dt.datetime(*[int(x) for x in [_year, _month, _day, _hour, _minute]]) \
            if _year and _month and _day and _hour and _minute else None
        self.m_linger = int(_linger) if _linger else 0
        self.m_end_datetime = self.m_start_datetime + dt.timedelta(seconds=self.m_linger) \
            if self.m_start_datetime and self.m_linger else None

    def __eq__(self, _other):
        return (self.m_user == _other.m_user) and \
               (self.m_host == _other.m_host) and \
               (self.m_display == _other.m_display)

    def __hash__(self):
        return hash((self.m_user, self.m_host, self.m_display))


lmutil_time_pattern = r'(?P<mday>\w+)\s(?P<month>\d+)/(?P<day>\d+)(/(?P<year>\d{4}))?\s(?P<hour>\d+):(?P<minute>\d+)'


def parse_record(_line, _year):
    groups = re.match(r'^(?P<user>.+?)'
                      r'\s(?P<host>.+?)'
                      r'\s(?P<display>.+?)'
                      r'\s\((?P<lic_version>.+?)\)'
                      r'\s\((?P<lic_server>.+?)\s(?P<port_handler>.\d+)\)'
                      r',\sstart\s' + lmutil_time_pattern +
                      r'(,\s(?P<lic_count>\d+)\slicenses)?'
                      r'(\s\(linger:\s(?P<linger>.+?)\))?'
                      r'.*$', _line)
    return FeatureRecord(groups.group('user'), groups.group('host'), groups.group('display'), _year,
                         groups.group('month'), groups.group('day'), groups.group('hour'), groups.group('minute'),
                         groups.group('linger'), groups.group('lic_count')) if groups else None


def parse_log(_file):
    with open(_file, 'r') as log:
        record_indent = ' ' * 4
        current_year = 0
        log_sections = {}
        current_section = ''
        for line in log:
            groups = re.match(r'^Flexible License Manager status on ' + lmutil_time_pattern, line)
            if groups:
                current_year = int(groups.group('year'))
                continue
            groups = re.match(r'^Users of (?P<section>\w+?):.*$', line)
            if groups:
                current_section = groups.group('section')
                log_sections[current_section] = []
                continue
            if re.match(r'^%s\S+.*$' % record_indent, line) and current_section in log_sections:
                log_sections[current_section].append(parse_record(line.strip(), current_year))
    return log_sections


def task1(_records):
    print('Task 1. Unique users count of ixchariot_fs:')
    count = len(set(_records))
    print(count)
    return {'task_number': 1,
            'task_description': 'unique users count of ixchariot_fs',
            'count': count}


def task2(_records):
    print('Task 2. Hosts, who uses ixchariot_fs more then one time:')
    same_hosts = {}
    for record in _records:
        if record.m_host not in same_hosts:
            same_hosts[record.m_host] = [record]
        else:
            same_hosts[record.m_host].append(record)
    same_hosts_info = {}
    for host_name, host_records in same_hosts.items():
        if len(host_records) > 1:
            same_hosts_info[host_name] = []
            print(host_name, end=': ')
            for host_record in host_records:
                if host_record.m_start_datetime:
                    same_hosts_info[host_name].append({'start_time': host_record.m_start_datetime})
                    print(host_record.m_start_datetime, end='')
                if host_record.m_end_datetime:
                    same_hosts_info[host_name][0]['end_time'] = host_record.m_end_datetime
                    print(' - ', host_record.m_end_datetime, end='')
                else:
                    print(', ', end='')
            print()
    return {'task_number': 2,
            'task_description': 'hosts, who uses ixchariot_fs more then one time',
            'hosts': same_hosts_info
            }


def task3(_records):
    print('Task 3. Hosts with more then 30 licenses:')
    hosts = []
    for record in _records:
        if record.m_lic_count > 30:
            print(record.m_host)
            hosts.append(record.m_host)
    return {'task_number': 3,
            'task_description': 'hosts with more then 30 licenses',
            'hosts': hosts}


if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client['lmstat_db']
    collection = db['tasks']
    sections = parse_log('data.log')
    t1 = task1(sections['ixchariot_fs'])
    print(t1)
    if not collection.find_one(t1):
        collection.insert_one(t1)
    t2 = task2(sections['ixchariot_fs'])
    print(t2)
    if not collection.find_one(t2):
        collection.insert_one(t2)
    t3 = task3(sections['chr_pairs_fs'])
    print(t3)
    if not collection.find_one(t3):
        collection.insert_one(t3)
