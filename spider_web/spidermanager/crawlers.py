import logging
from threading import Thread
from multiprocessing import Process, Lock
import psutil
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from utils.get_module import get_spider_name, get_modules



logger = logging.getLogger("SpiderManager")


def thread_terminate(process):
    def _terminate(process):
        process.terminate()

    Thread(target=_terminate, args=(process,)).start()

class STATUS:
    START = 0x01
    PAUSE = 0x02
    STOP = 0x03
    UNPAUSE = 0x04


class SpiderProcess(Process):
    def __init__(self, spiderId, spider_cls, settings):
        Process.__init__(self)
        self.lock = Lock()
        self.spiderId = spiderId
        self.spider_cls = spider_cls
        self.settings = settings

    def run(self):
        proc = CrawlerProcess(self.settings)
        proc.crawl(self.spider_cls)
        proc.start()

    def pause(self):
        with self.lock:
            try:
                p = psutil.Process(self.pid)
                p.suspend()
            except Exception as e:
                logger.exception(e)

    def unpause(self):
        with self.lock:
            try:
                p = psutil.Process(self.pid)
                p.resume()
            except Exception as e:
                logger.exception(e)

    def is_alive(self) -> bool:

        try:
            p = psutil.Process(self.pid)
            return p.is_running()
        except Exception as e:
            return False

    def terminate(self) -> None:
        with self.lock:
            try:
                p = psutil.Process(self.pid)
                children = p.children()
                for child in children:
                    child.terminate()
                    child.wait()
                p.kill()
                p.wait()
                if psutil.pid_exists(self.pid):
                    p.kill()
            except Exception as e:
                pass


class SpiderManager:
    spiderJobs = dict()



    def create_job(self,spider):
        spider_cls = get_spider_name(spider.spider_class)
        settings = self.load_settings(spider)
        self.delete_job(spider)
        proc = SpiderProcess(spider.file_id, spider_cls, settings)
        self.spiderJobs[spider.file_id] = proc
        return True

    def load_settings(self, spider):
        settings = Settings()
        settings_file = get_modules(spider.settings_path)
        settings.setmodule(settings_file)

        return settings

    def delete_job(self, spider):
        if spider.file_id in self.spiderJobs and self.stop_job(spider):
            del self.spiderJobs[spider.file_id]
            return True
        return False

    def stop_job(self, spider):
        if spider.file_id in self.spiderJobs:
            proc = self.spiderJobs[spider.file_id]
            thread_terminate(proc)
            return True
        else:
            return False

    def start_job(self, spider):
        if self.create_job(spider):
            proc = self.spiderJobs[spider.file_id]
            proc.start()
            return True
        return False

    def pause_job(self, spider):
        if spider.file_id in self.spiderJobs:
            proc = self.spiderJobs[spider.file_id]
            proc.pause()
            return True
        else:
            return False

    def unpause_job(self, spider):
        if spider.file_id in self.spiderJobs:
            proc = self.spiderJobs[spider.file_id]
            proc.unpause()
            return True
        else:
            return False

    def spider_status(self, spider):
        if spider.id in self.spiderJobs:
            return self.spiderJobs[spider.id].is_alive()
        return False

    def control_job(self, spider, flag):
        result = False
        if STATUS.STOP == flag:
            result = self.stop_job(spider)
        if STATUS.PAUSE == flag:
            result = self.pause_job(spider)
        if STATUS.UNPAUSE == flag:
            result = self.unpause_job(spider)
        return result








