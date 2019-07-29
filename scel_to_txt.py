# -*- coding: utf-8 -*-
import os
import struct
#拼音表偏移，
startPy = 0x1540
# 汉语词组表偏移
startChinese = 0x2628
# 全局拼音表
GPy_Table = {}

# 原始字节码转为字符串
def byte2str(data):
    pos = 0
    str = ''
    while pos < len(data):
        c = chr(struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0])
        if c != chr(0):
            str += c
        pos += 2
    return str


# 获取拼音表
def getPyTable(data):
    data = data[4:]
    pos = 0
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        lenPy = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        py = byte2str(data[pos:pos + lenPy])
        GPy_Table[index] = py
        pos += lenPy


# 获取一个词组的拼音
def getWordPy(data):
    pos = 0
    ret = ''
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        ret += GPy_Table[index]
        pos += 2
    return ret


# 读取中文表
def getChinese(data):
    GTable = []
    pos = 0
    while pos < len(data):
        # 同音词数量
        same = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        # 拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        # 拼音索引表
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len])
        # 中文词组
        pos += py_table_len
        for i in range(same):
            # 中文词组长度
            c_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 词频
            pos += 2
            count = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 保存
            GTable.append((count, py, word))
            # 到下个词的偏移位置
            pos += ext_len
    return GTable


def scel2txt(file_name):
    print('-' * 60)
    with open(file_name, 'rb') as f:
        data = f.read()
    print("词库名：", byte2str(data[0x130:0x338]))  # .encode('GB18030')
    print("词库类型：", byte2str(data[0x338:0x540]))
    print("描述信息：", byte2str(data[0x540:0xd40]))
    print("词库示例：", byte2str(data[0xd40:startPy]))
    getPyTable(data[startPy:startChinese])
    #元组(词频,拼音,中文词组)的列表 如：[(3, 'bingdong', '冰冻'), (6, 'fushui', '腹水')]
    getChinese(data[startChinese:])
    print("getChinese(data[startChinese:])={}".format(getPyTable(data[startPy:startChinese])))
    return getChinese(data[startChinese:])

if __name__ == '__main__':
    # scel所在文件夹路径
    in_path = r"C:\Users\jx\PycharmProjects\文本处理\搜狗细胞词库转换txt\scel"
    # 输出词典所在文件夹路径
    out_path = r"C:\Users\jx\PycharmProjects\文本处理\搜狗细胞词库转换txt\txt"
    fin = [fname for fname in os.listdir(in_path) if fname[-5:] == ".scel"]
    for f in fin:
        try:
            for word in scel2txt(os.path.join(in_path, f)):
                file_path = (os.path.join(out_path, str(f).split('.')[0] + '.txt'))
                # 保存结果
                with open(file_path, 'a+', encoding='utf-8')as file:
                    file.write(word[2] + '\n')
            # os.remove(os.path.join(in_path, f))
        except Exception as e:
            print(e)
            pass