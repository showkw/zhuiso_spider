from Config.UserAgents import USER_AGENTS
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy import crawler
import random

#随机返回User-Agent
class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))