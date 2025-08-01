import os
import yaml


def read_yaml(yamlpath):
    '''读取yaml数据'''
    if not os.path.isfile(yamlpath):
        raise FileNotFoundError("文件路径不存在，请检査路径是否正确:{}".format(yamlpath))
    # open读取yqml,获取文本内容
    with open(yamlpath, 'r', encoding='utf-8') as f:
        cfg = f.read()
        content = yaml.load(cfg, Loader=yaml.FullLoader)
        return content
