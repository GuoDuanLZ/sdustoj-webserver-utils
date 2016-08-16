from ..sdustoj_server.redis_connections import pool
from redis import Redis


def send_message(name, data):
    """
    发送消息到指定消息队列。
    :param name: redis中消息队列的名字，字符串
    :param data: 要发送的消息，字符串
    :return: None
    """
    r = Redis(connection_pool=pool)
    r.rpush(name, data)
