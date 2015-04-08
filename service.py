#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-08 20:53:11
# @Author  : jonnyF (fuhuixiang@jonnyf.com)
# @Link    : http://jonnyf.com


import socket
import threading
import sys
import string
import ConfigParser

cf = ConfigParser.ConfigParser()

cf.read('default.conf')

ip = cf.get('cache', 'ip')
port = cf.getint('cache', 'port')
Listen = cf.getint('cache', 'Listen')
timeout = cf.getint('cache', 'timeout')
Accept_size = cf.getint('cache', 'Accept_size')


def jonnyS(client, address):
    try:

        # client, address = args
    #设置超时时间
        client.settimeout(timeout)

    #接收数据的大小
        buf = client.recv(Accept_size)

    #将接收到的信息原样的返回到客户端中
        print buf
        bufs = buf.split('+')
        settings = bufs[0]
        setting = settings.split(' ')
        operation = setting[0]
        key = setting[1]
        flags = setting[2]
        expiration_time = setting[3]
        value = bufs[1]
        client.send(buf)

    #超时后显示退出
    except socket.timeout:
        print 'time out'

    #关闭与客户端的连接
    client.close()


def main():
    #创建socket对象。调用socket构造函数
    #AF_INET为ip地址族，SOCK_STREAM为流套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #将socket绑定到指定地址，第一个参数为ip地址，第二个参数为端口号
    sock.bind((ip, port))

    #设置最多连接数量
    sock.listen(Listen)
    while True:

        #服务器套接字通过socket的accept方法等待客户请求一个连接
        # client, address = sock.accept()
        thread = threading.Thread(target=jonnyS, args=sock.accept())
        thread.start()

if __name__ == '__main__':
    main()
