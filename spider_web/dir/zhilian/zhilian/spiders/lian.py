# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import signals
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import DontCloseSpider


class LianSpider(scrapy.Spider):
    name = 'lian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=664&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&=0&_v=0.57946422&x-zp-page-request-id=1f6635341f574b7fa278c8a8a9bd60ab-1574887740558-569248&x-zp-client-id=52b60cac-9a01-4be0-fd41-daf4c24b928d&MmEwMD=4HYn2.iY6N6mjVE05pJzdU5TMFEd1wev5nm4dByg9WsRA_pnymLcKA0OWk.lhErSSMZP3x_jHHyuDfZc_JLahOCysxCOwo7P8NtcDRRh1ZESo8eg065nXXhENspo8RfpEJypuUdOkUM8UumyFOZI0Y9VrfpM4_KmNVppprljQPMY2xGQiD3Adl7xQevC5aBCsUua6WAa_S9qoYXTZPS7okq4dhGXGQtJNt5UKk8NOcwwxAbLdTM2tYyPT4E_DA1_D4BBztIloSjYc5VkAJztmcC_OBTy5rwSf00.iOK_4UFHAisTt2qQK3_vbr_DeTxA5WWFns99QlTMNY3XskGriqysJ_yXdKzp6uTw.tMICARAMr9_e4gPcEufJrze_aBcsceGtUxA4EVYFzLuAuZ5xuD2EN80Ba8gVHYjvOYWJ03HOfHQkOsGEULGnsr99mRy_eNG']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args,**kwargs)
        crawler.signals.connect(spider.spider_idle,signals.spider_idle)
        spider._set_crawler(crawler)
        return spider

    def start_requests(self):
        yield  scrapy.Request(
            url=self.start_urls[0],
            headers=self.headers,
            dont_filter=True
        )

    def parse(self, response):
        datas = json.loads(response.text)["data"]["results"]
        for data in datas:
            data_dict = {}
            data_dict["jobname"] = data["jobName"]
            print(data_dict)

    def schedule_next_requests(self):
        """Schedules a request if available"""
        # TODO: While there is capacity, schedule a batch of redis requests.
        for req in self.start_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        # XXX: Handle a sentinel to close the spider.
        self.schedule_next_requests()
        raise DontCloseSpider

