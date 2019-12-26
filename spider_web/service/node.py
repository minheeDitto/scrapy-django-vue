from threading import Lock
from spidermanager.crawlers import SpiderManager
from users.models import FileContent


class NodeService:
    spiderManager = None

    def __init__(self):
        self.spiderManager = SpiderManager()

    def start_spider(self, spider):
        return self.spiderManager.start_job(spider)

    def control_spider(self, spider, flag):
        """
        停止暂停取消暂停爬虫
        :param id:
        :param flag:
        :return:
        """
        return self.spiderManager.control_job(spider, flag)

    def delete_spider(self, id):
        spider = FileContent.objects.filter(file_id=id)
        if spider:
            self.spiderManager.delete_job(spider)
            spider.delete()
            return True
        else:
            return False

