# -*- coding: utf-8 -*-
from Config.UserAgents import USER_AGENTS
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  # UserAegent中间件
import random


# 随机返回User-Agent
class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))
