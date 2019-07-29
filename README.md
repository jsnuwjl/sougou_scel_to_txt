# 搜狗细胞词库全词库
## 实现功能
* 1.爬取了搜狗细胞词库中的所有词库文件
* 2.将scel文件转换为txt文件

## 注意
* 需要在代码目录下构建scel和txt2个空文件夹
* 分词好的结果已在词库.txt内

## 代码执行顺序
* 1.get_scel.py 获取所有的scel文件 并写入scel文件夹内
* 2.scel_to_txt.py 将scel文件逐个解析 并写入txt文件夹内
* 3.main.py 合并所有txt文件
