#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pexpect
import xlrd
import sys
import logging
import time
import re
import os

ARGS_CUR_POS = 0

def get_userinfo(excel_name, sheet_name):
    logging.info("读取{}表格，{}页签。")
    try:
        wb = xlrd.open_workbook(excel_name)
        ws = wb.sheet_by_name(sheet_name)
    except:
        logging.info("打开EXCEL表格失败，请确认{0}文件，{1}页签是否存在。".format(excel_name, sheet_name))
        sys.exit(-1)
    user_info = []
    port_col = 0
    for i in range(0, ws.ncols):
        if ws.cell(rowx=0, colx=i).value == u"端口":
            port_col = i

    for j in range(1, ws.nrows):
        port = str(int(ws.cell(rowx=j, colx=port_col).value))
        user_info.append(port)

    return user_info


def delete_one_account(port):
    process = pexpect.spawn("bash ssrmu.sh", logfile=sys.stdout, encoding='utf-8')
    process.expect("管理脚本")
    process.sendline("7")
    process.expect("用户配置")
    process.sendline("2")
    process.expect("要删除的用户")
    process.sendline(port)
    time.sleep(0.5)


def delete_account(user_info):
    for port in user_info:
        delete_one_account(port)
    show_account()
    return True


def show_account():
    process = pexpect.spawn("bash ssrmu.sh", logfile=sys.stdout, encoding='utf-8')
    process.expect("请输入数字")
    process.sendline("5")
    process.expect("用户总数")
    time.sleep(1)


def delete_acc_by_excel(excel_name="delete_account.xlsx", sheet_name="Sheet1"):
    if not os.path.exists(excel_name):
        logging.error("%s文件不存在" % excel_name)
        sys.exit(-1)
    # 获取EXCEL信息
    user_info = get_userinfo(excel_name, sheet_name)
    if not user_info:
        logging.error("读取EXCEL内容为空，任务失败。")
        sys.exit(-1)
    user_info = get_userinfo(excel_name, sheet_name)
    delete_account(user_info)
    logging.info("任务完成。")


def judge():
    """判断是否args越界"""
    if ARGS_CUR_POS < len(sys.argv):
        return True
    logging.error("输入参数不合法，任务失败。")
    usage()
    sys.exit(-1)


def is_numeric(port: str):
    try:
        ret = int(port)
        if 1023 < ret < 65536:
            return True
        else:
            raise Exception('the port num is out index')
    except Exception as e:
        logging.error("the format of %s is illegal, it must be a num and between 1024 and 65535" % port)
        sys.exit(-1)


def delete_acc_by_file(file_name='delete_account.txt'):
    if not os.path.exists(file_name):
        logging.error("%s文件不存在" % file_name)
        sys.exit(-1)
    user_info = []
    p = re.compile("^#.*$")
    with open(file=file_name, mode='r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.rstrip('\n').strip()
            if line == '' or p.match(line) is not None:
                continue
            port = re.split('\\s+', line)
            if len(port) == 1 and is_numeric(port[0]):
                user_info.append(int(port[0]))
            else:
                logging.error("the format of %s is illegal." % file_name)
                sys.exit(-1)
    delete_account(user_info)
    logging.info("任务完成。")


def usage():
    logging.info('''
Usage: python delete_account.py [-h] [-f] [--file <file-name>] [-e/--excel <excel-name> <sheet-name>]
-h: print the usage of this script.
-f: use the default file named 'delete_account.txt' as a file used to delete acc.
--file <file-name>: file-name that a specific file named by you as a file used to delete acc. 
-e: use default delete_account.xlsx and Sheet1 as excel name and sheet name respectively.
--excel <excel-name> <sheet-name>: specify your excel file and the sheet name used to delete acc.
default: if no args is input, the script will exec just like 'python delete_account.py -f'
-----------------------------
the non-excel file used to delete acc must format just like:
=========================================================
# delete_account.txt
# the lines headed by '#' and blank lines will be ignored
# one port num that must between 1024 and 65535 per line
1314
1315
=========================================================
    ''')


def switch():
    global ARGS_CUR_POS
    ARGS_CUR_POS += 1
    judge()
    if sys.argv[ARGS_CUR_POS] == '-e':
        delete_acc_by_excel()
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '--excel':
        ARGS_CUR_POS += 1
        judge()
        excel_name = sys.argv[ARGS_CUR_POS]
        ARGS_CUR_POS += 1
        judge()
        sheet_name = sys.argv[ARGS_CUR_POS]
        ARGS_CUR_POS += 1
        delete_acc_by_excel(excel_name=excel_name, sheet_name=sheet_name)
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '--file':
        ARGS_CUR_POS += 1
        judge()
        file_name = sys.argv[ARGS_CUR_POS]
        delete_acc_by_file(file_name=file_name)
        sys.exit(0)
    elif sys.argv[ARGS_CUR_POS] == '-f':
        delete_acc_by_file()
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
        delete_acc_by_file()
        sys.exit(0)
    switch()



