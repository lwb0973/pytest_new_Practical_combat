import pymysql
from pymysql.cursors import DictCursor
from common.yaml_read_handler import read_yaml
import settings

read_config = read_yaml(settings.READ_YAML_FILE)
sqldb_config = read_config['sqldb'][0]


class MySQLHelper:
    def __init__(self, charset='utf8mb4'):
        self.conn = pymysql.connect(
            host=sqldb_config['host'],
            port=sqldb_config['port'],
            user=sqldb_config['user'],
            password=sqldb_config['password'],
            database=sqldb_config['database'],
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor  # 返回字典格式结果
        )
        self.cursor = self.conn.cursor()

    def query(self, sql, params=None):
        """执行查询"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        """执行增删改"""
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.rowcount

    def insert(self, table, data: dict):
        """插入一条数据"""
        keys = ', '.join([f"`{k}`" for k in data.keys()])  # 加反引号处理字段名
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        return self.execute(sql, list(data.values()))

    def update(self, table, data: dict, where: str, params: list):
        """更新数据"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        return self.execute(sql, list(data.values()) + params)

    def delete(self, table, where: str, params: list):
        """删除数据"""
        sql = f"DELETE FROM {table} WHERE {where}"
        return self.execute(sql, params)

    def close(self):
        self.cursor.close()
        self.conn.close()


# db = MySQLHelper()
# # 调用查询示例
# results = db.query("SELECT * FROM user_ip WHERE region_code = %s", 710000)
# for row in results:
#     print(row)
#
# # 调用插入示例
# data = {'id': 3,
#         'ip': '172.16.88.246',
#         'version': 1,
#         'region code': 710000,
#         'domain code': 2,
#         'created at': 1748350686,
#         'latest access at': 1748425456
#         }
# resutil = db.insert('user_ip', data)
# print(resutil)
#
# # 调用更新示例
# data = {'created_at': 1748350688}
# where = 'id = %s'
# params = [3]
# resutil = db.update('user_ip', data, where, params)
# print(resutil)
#
# # 调用删除示例
# data = {'created_at': 1748350688}
# where = 'id = %s'
# params = [3]
# resutil = db.delete('user_ip', where, params)
# print(resutil)
