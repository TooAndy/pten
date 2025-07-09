
import hashlib
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


class TencentCdnProxy():
    """使用腾讯 CDN 作为代理时, 使用这个类
    """
    def __init__(self, host, key, timestamp_bit=10):
        self.key = key
        self.timestamp_bit = int(timestamp_bit)
        self.host = host

    def generate_sign(self, path, ts=None):
        """
        根据传参, 生成签名

        :param url: 包含协议的url, 不包含path, 例如 https://notice.aniss.fun
        :param path: url path, 例如 /abc/efg
        :param ts: 当前时间戳 10位
        :return: 签名
        """
        key = self.key                               # 鉴权密钥
        now = int(time.mktime(time.strptime(ts, "%Y%m%d%H%M%S"))
                if ts else time.time())                # 如果输入了时间，用输入ts，否则用当前ts
        ttl_format = self.timestamp_bit                                     # 时间进制，10或16，只有typeD支持
        ts = now if ttl_format == 10 else hex(now)[2:]
        sign = hashlib.md5(f"{key}{path}{ts}".encode(encoding="utf-8")).hexdigest()
        return sign, ts


    def proxy(self, url, param=None, value=None):
        """
        替换 URL 中指定参数的值。

        :param url: 原始 URL 地址
        :param param: 需要替换的参数名
        :param value: 替换后的参数值
        :return: 替换后的 URL 地址
        """
        # 解析 URL
        parsed_url = urlparse(url)

        # 解析查询参数
        query_params = parse_qs(parsed_url.query)

        if param:
            # 替换指定参数的值
            query_params[param] = [value]

        sign, ts = self.generate_sign(parsed_url.path)
        query_params["sign"] = [sign]
        query_params["t"] = [ts]

        # 重新构建查询字符串
        new_query = urlencode(query_params, doseq=True)

        # 重新构建完整的 URL
        new_url = urlunparse((
            parsed_url.scheme,  # 协议
            self.host,         # 域名
            parsed_url.path,    # 路径
            parsed_url.params,  # 参数
            new_query,          # 新的查询字符串
            parsed_url.fragment  # 片段
        ))
        return new_url