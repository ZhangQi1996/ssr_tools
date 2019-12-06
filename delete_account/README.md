# delete_account

批量删除账号

依赖库：

- xlrd
- pexpect

## 使用说明

~~1. 将需要删除的端口号填入到delete_account.xlsx表格中~~
~~2. 拷贝create_account.py脚本和create_account.xlsx表格到与ssrmu.sh文件的同级目录下~~
1. 已经在同级目录添加了ssrmu.sh以及其依赖的mujson_mgr.py文件
2. **注意目前程序仅支持py3**
3. 默认编码utf-8
4. 建议先切换到su下再进行操作

* 支持两种导入方式
    1. txt （默认）
        * 多种方式
        * sudo python delete_account.py
        * sudo python delete_account.py -f
        * sudo python delete_account.py --file file-name
        * txt的格式参见使用帮助
    2. excel
        * sudo python delete_account.py -e
        * sudo python delete_account.py --excel excel-name sheet-name

* 使用帮助
```
python delete_account.py -h
```


