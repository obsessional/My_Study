

import paramiko

class SSHConnection(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()  # 建立连接
    def _connect(self):
        transport = paramiko.Transport(self._host, self._port)
        transport.connect(username=self._username, password=self._password)
        self._transport = transport
    # 执行命令
    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        return data

def ssh_command():
    # 创建ssh客户端
    ssh = paramiko.SSHClient()
    # 第一次ssh远程时会提示输入yes或者no
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 密码方式远程连接
    ssh.connect("172.30.242.132", 22, username='crmddzx', password='dcos@01', timeout=20)
    # 执行命令
    port = "31055"
    cmds = "docker ps |grep " + str(port) + " |awk '{ print $1 }'"
    stdin, stdout, stderr = ssh.exec_command(cmds)
    # 获取命令执行结果,返回的数据是一个list
    result = stdout.readlines()[0]
    print(result)

    cmds2 = "docker exec -ti " + str(result) + " /bin/sh"
    stdin, stdout, stderr = ssh.exec_command(cmds2,timeout=10)
    # 获取命令执行结果,返回的数据是一个list
    result = stdout.readlines()
    print(result)

    cmds3 = "ls -l"
    stdin, stdout, stderr = ssh.exec_command(cmds3)
    # 获取命令执行结果,返回的数据是一个list
    result = stdout.readlines()
    print(result)
    ssh.close()

if __name__ == "__main__":
    ssh_command()