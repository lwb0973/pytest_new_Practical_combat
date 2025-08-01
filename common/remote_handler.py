import paramiko
import settings
from common.yaml_read_handler import read_yaml


read_config = read_yaml(settings.READ_YAML_FILE)
ssh_config = read_config['ssh'][0]


class RemoteFileManager:
    def __init__(self):
        self.hostname = ssh_config['hostname']
        self.port = ssh_config['port']
        self.username = ssh_config['username']
        self.password = ssh_config['password']
        self.client = None

    def connect(self):
        """建立SSH连接"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, self.port, self.username, self.password)

    def close(self):
        """关闭SSH连接"""
        if self.client:
            self.client.close()

    def execute(self, command):
        """执行Shell命令"""
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def create_file(self, path, content=''):
        """创建文件并写入内容"""
        cmd = f'echo "{content}" > {path}'
        return self.execute(cmd)

    def read_file(self, path):
        """读取文件内容"""
        cmd = f'cat {path}'
        return self.execute(cmd)

    def update_file(self, path, new_content):
        """修改文件内容"""
        return self.create_file(path, new_content)

    def delete_file(self, path):
        """删除文件"""
        cmd = f'rm -f {path}'
        return self.execute(cmd)


# 调用ssh封装的方法示例
# remote=RemoteFileManager()
# # 执行建立连接
# remote.connect()
# # 创建文件写入内容
# remote.create_file('/home/test.txt', 'hello worldddd')
# # 执行shell命令
# executes = remote.execute('cat /home/test.txt')
# # 修改文件内容
# remote.update_file('/home/test.txt', 'caiguanweishabi')
# output, error = remote.read_file('/home/test.txt')
# # strip()去除开头可结尾的空表字符包括 \n、\r、\t、空格等
# clean_output = output.strip()
# print(clean_output)
# # 删除文件
# delete_file = remote.delete_file('/home/test.txt')
# # 关闭ssh连接
# remote.close()
