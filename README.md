# 搜狗细胞词库全词库
## 实现功能
* 1.爬取了[搜狗细胞词库](https://pinyin.sogou.com/dict/)中的所有词库文件
* 2.对搜狗输入法的scel格式的细胞词库文件进行解析。

## 注意
* 需要在代码目录下构建`scel`和`txt`2个空文件夹
* 我自己已经做好的词库结果在`词库.txt`内

## 代码执行顺序
* 1.`get_scel.py` 获取所有的scel文件 并写入`scel`文件夹内
* 2.`scel_to_txt.py` 将scel文件逐个解析 并写入`txt`文件夹内
* 3.`main.py` 合并所有txt文件

