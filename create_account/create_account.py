#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import xlrd
import pexpect
import sys
import logging
import time
import re
import os

ARGS_CUR_POS = 0

# 配置项
config = {
    "加密方式": "10",
    "协议插件": "1",
    "混淆插件": "1",
    "限制的设备数": "3",
    "单线程 限速上限": "",
    "总速度 限速上限": "",
    "总流量上限": "50",
    "禁止访问的端口": "22",
}


def get_userinfo(excel_name, sheet_name):
    logging.info("读取{}表格，{}页签。")
    try:
        wb = xlrd.open_workbook(excel_name)
        ws = wb.sheet_by_name(sheet_name)
    except:
        logging.info("打开EXCEL表格失败，请确认{0}文件，{1}页签是否存在。".format(excel_name, sheet_name))
        return {}
    user_info = {}
    password_col = 0
    port_col = 0
    user_col = 0
    dev_col = 0
    flow_col = 0
    for i in range(0, ws.ncols):
        if ws.cell(rowx=0, colx=i).value == u"用户名":
            user_col = i
        elif ws.cell(rowx=0, colx=i).value == u"端口":
            port_col = i
        elif ws.cell(rowx=0, colx=i).value == u"密码":
            password_col = i
        elif ws.cell(rowx=0, colx=i).value == u"设备数":
            dev_col = i
        elif ws.cell(rowx=0, colx=i).value == u"总流量":
            flow_col = i

    for j in range(1, ws.nrows):
        user_name = str(ws.cell(rowx=j, colx=user_col).value)
        # port = str(int(ws.cell(rowx=j, colx=port_col).value))
        # password = str(ws.cell(rowx=j, colx=password_col).value)
        user_info.update({user_name: {
            "pass_word": str(ws.cell(rowx=j, colx=password_col).value),
            "port": str(int(ws.cell(rowx=j, colx=port_col).value)),
            "dev": str(int(ws.cell(rowx=j, colx=dev_col).value)),
            "flow": str(int(ws.cell(rowx=j, colx=flow_col).value)),
        }})

    return user_info


def create_one_account(process, user_name, value, config):
    process.expect("要设置的用户")
    process.sendline(user_name)
    process.expect("端口")
    process.sendline(value["port"])
    process.expect("密码")
    process.sendline(value["pass_word"])
    process.expect("加密方式")
    process.sendline(config["加密方式"])
    process.expect("协议插件")
    process.sendline(config["协议插件"])
    process.expect("混淆插件")
    process.sendline(config["混淆插件"])
    process.expect("限制的设备数")
    process.sendline(value["dev"])
    process.expect("单线程 限速上限")
    process.sendline(config["单线程 限速上限"])
    process.expect("总速度 限速上限")
    process.sendline(config["总速度 限速上限"])
    process.expect("总流量上限")
    process.sendline(value["flow"])
    process.expect("禁止访问的端口")
    process.sendline(config["禁止访问的端口"])


def create_account(user_info, config):
    process = pexpect.spawn("bash ssrmu.sh", logfile=sys.stdout, encoding='utf-8')
    process.expect("管理脚本")
    process.sendline("7")
    process.expect("用户配置")
    process.sendline("1")

    sorted_user = sorted(user_info.items(), key=lambda x: x[0])
    for key, value in sorted_user:
        create_one_account(process, key, value, config)
        try:
            process.expect("是否继续")
            process.sendline("Y")
        except:
            # process.expect("错误")
            process = pexpect.spawn("bash ssrmu.sh", logfile=sys.stdout, encoding='utf-8')
            process.expect("管理脚本")
            process.sendline("7")
            process.expect("用户配置")
            process.sendline("1")

    show_account()
    return True


def show_account():
    process = pexpect.spawn("bash ssrmu.sh", logfile=sys.stdout, encoding='utf-8')
    process.expect("请输入数字")
    process.sendline("5")
    process.expect("已使用流量总和")
    time.sleep(1)


def create_acc_by_file(file_name='create_account.txt'):
    if not os.path.exists(file_name):
        logging.error("%s文件不存在" % file_name)
        sys.exit(-1)
    user_info = {}
    p = re.compile("^#.*$")
    with open(file=file_name, mode='r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.rstrip('\n').strip()
            if line == '' or p.match(line) is not None:
                continue
            user = re.split('\\s+', line)
            if len(user) < 5:
                logging.error("the format of %s is illegal." % file_name)
                sys.exit(-1)
            user_info.update({user[0]: {
                "pass_word": user[1],
                "port": user[2],
                "dev": user[3],
                "flow": user[4],
            }})
    # 创建账号
    create_account(user_info, config)
    logging.info("任务完成。")


def create_acc_by_excel(excel_name="create_account.xlsx", sheet_name="Sheet1"):
    if not os.path.exists(excel_name):
        logging.error("%s文件不存在" % excel_name)
        sys.exit(-1)
    # 获取EXCEL信息
    user_info = get_userinfo(excel_name, sheet_name)
    if not user_info:
        logging.error("读取EXCEL内容为空，任务失败。")
        sys.exit(-1)
    # 创建账号
    create_account(user_info, config)
    logging.info("任务完成。")


def judge():
    """判断是否args越界"""
    if ARGS_CUR_POS < len(sys.argv):
        return True
    logging.error("输入参数不合法，任务失败。")
    usage()
    sys.exit(-1)


def usage():
    logging.info('''
Usage: python create_account.py [-h] [-f] [--file <file-name>] [-e/--excel <excel-name> <sheet-name>]
-h: print the usage of this script.
-f: use the default file named 'create_account.txt' as a file used to create acc.
--file <file-name>: file-name that a specific file named by you as a file used to create acc. 
-e: use default create_account.xlsx and Sheet1 as excel name and sheet name respectively.
--excel <excel-name> <sheet-name>: specify your excel file and the sheet name used to create acc.
default: if no args is input, the script will exec just like 'python create_account.py -f'
-----------------------------
the non-excel file used to create acc must format just like:
=========================================================
# create_account.txt
# the lines headed by '#' and blank lines will be ignored
# user_name port password dev_num sum_traffic
# 用户名 密码 端口 设备数量 总流量
david password 1314 3 30
=========================================================
    ''')


def switch():
    global ARGS_CUR_POS
    ARGS_CUR_POS += 1
    judge()
    if sys.argv[ARGS_CUR_POS] == '-e':
        create_acc_by_excel()
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '--excel':
        ARGS_CUR_POS += 1
        judge()
        excel_name = sys.argv[ARGS_CUR_POS]
        ARGS_CUR_POS += 1
        judge()
        sheet_name = sys.argv[ARGS_CUR_POS]
        ARGS_CUR_POS += 1
        create_acc_by_excel(excel_name=excel_name, sheet_name=sheet_name)
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '--file':
        ARGS_CUR_POS += 1
        judge()
        file_name = sys.argv[ARGS_CUR_POS]
        create_acc_by_file(file_name=file_name)
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '-f':
        create_acc_by_file()
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '-h':
        usage()
        sys.exit(0)
    else:
        logging.error("the args you input are illegal..")
        usage()
        sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists('ssrmu.sh'):
        raise Exception('请将ssrmu.sh脚本与本脚本放于同一目录中')
    if len(sys.argv) == 1:
        create_acc_by_file()
        sys.exit(0)
    switch()



