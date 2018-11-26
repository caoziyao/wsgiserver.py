import os, json
import datetime


def log(*args, **kwargs):
    """log 日志"""
    dt = datetime.datetime.now()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log', 'log.txt'))
    with open(path, 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        # print(dt, *args, file=f, **kwargs)


def json_save(path, data):
    """保持 json 格式字符串到文件"""
    data = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def json_loads(path):
    """从文件读取
    返回对象字典
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        return json.loads(data)


