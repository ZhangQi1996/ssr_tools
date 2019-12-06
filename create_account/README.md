# create_account

批量创建账号

## 安装三方库

1. 如果没有pip，先安装pip；有则进行第2步

   ```
   sudo yum -y install epel-release
   sudo yum -y install python-pip
   ```

2. 安装三方库

   ```
   pip install xlrd
   pip install pexpect
   ```

## 使用说明

~~1. 将需要新增的用户名，端口号，密码，限制设备数，总流量填入到create_account.xlsx表格中~~

~~2. 拷贝create_account.py脚本和create_account.xlsx表格到与ssrmu.sh文件的同级目录下~~

~~3. 运行脚本 python create_account.py~~
1. 已经在同级目录添加了ssrmu.sh以及其依赖的mujson_mgr.py文件

#####注：如果需要重新配置加密方式，协议等，在create_account.py的main函数中的config字典中修改

* 支持两种导入方式
    1. txt （默认）
        * 多种方式
        * python create_account.py
        * python create_account.py -f
        * python create_account.py --file file-name
        * txt的格式参见使用帮助
    2. excel
        * python create_account.py -e
        * python create_account.py --excel excel-name sheet-name

* 使用帮助
```
python create_account.py -h
```
