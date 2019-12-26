from django.shortcuts import render,HttpResponse
import shutil
from django.http import JsonResponse,QueryDict
from django.views.generic.base import View
import json
from django.views.decorators.csrf import csrf_protect
import zipfile

from .models import FileContent
from utils.get_module import get_modules, get_spider_name
from utils.encrypt import get_encrpt
from service import nodeService
from spidermanager.crawlers import STATUS
import os



# Create your views here.


class Login(View):



    def post(self,request):
        d = {"token":"admin-token"}
        return HttpResponse(json.dumps(d), content_type="application/json")


class Files(View):



    def post(self,request):
        file = request.FILES.get("file")
        file_dir = "C:/Users/liang/Desktop/spider_web/dir"
        Zipdir = zipfile.ZipFile(file).extractall(file_dir)
        name = file.name.split(".")[0]
        zip_dir = os.path.join(file_dir, f"{name}/{name}/spiders")

        spider_file = [file for file in os.listdir(zip_dir) if "__" not in file][0].split(".")[0]
        settings_file = file_dir.split("/")[-1] + "."+ name + "." +  name + "."
        setting_path = settings_file + "settings"
        spider_class = settings_file + "spiders." + spider_file
        files = FileContent.objects.filter(display_name=name)
        # if len(files):
        #     return JsonResponse({
        #     "status":"error",
        #     "error":"zip exist",
        #     "message":"fail",})
        # else:

        file_id = get_encrpt(name)

        display_name = name
        File_save = FileContent.objects.create(
            file_zip=file,
            cmd="",
            display_name=display_name,
            file_id=file_id,
            settings_path=setting_path,
            spider_class=spider_class
        )
        File_save.save()
        return HttpResponse(json.dumps({
            "status":"ok",
            "error":"",
            "message":"success",


        }),content_type="application/json")


class SpiderOperate(View):

    def get(self, request):
        spideLIst = FileContent.objects.all()
        datas = {
            "status":"ok",
            "message":"success",
            "data":{"list":[]},
            "total": len(spideLIst),
            "error":"",
        }
        for spider in spideLIst:
            spider_data = {}
            spider_data["cmd"] = spider.cmd
            spider_data["display_name"] = spider.display_name
            spider_data["_id"] = spider.file_id
            datas["data"]["list"].append(spider_data)
        return JsonResponse(datas)


class SpiderInfo(View):


    def get(self, request, id):
         spider = FileContent.objects.filter(file_id=id)

         data_dict = {
             "status":"ok",
             "message":"success",
             "data":{
                 "_id":id,
                 "name":spider[0].display_name,

                "cmd":spider[0].cmd
             }

         }
         return JsonResponse(data_dict)

    def post(self, request, id):
        spider = FileContent.objects.filter(file_id=id)
        data_dict = json.loads(request.body.decode())
        if len(spider):
            spider = spider[0]
            spider.cmd = data_dict["cmd"]
            spider.display_name = data_dict["name"]
            spider.save()
        return JsonResponse({"status":"ok"})



    def delete(self, request, id):
        spider = FileContent.objects.filter(file_id=id)

        if spider:
            spiderInfo = spider[0]
            dir = f"C:/Users/liang/Desktop/spider_web/dir/{spiderInfo.display_name}"
            shutil.rmtree(dir)
            spider[0].delete()


            return JsonResponse({"status":"ok","message":"success"})


class SpiderFile(View):

    def get(self, request, id):
        pass


class SpiderStart(View):

    def get(self, request, id):
        resp = dict()
        try:
            spiderId = FileContent.objects.filter(file_id=id)

            if spiderId:
                spider = spiderId[0]
                spider.status = 1
                spider.save()
                nodeService.start_spider(spider)
                resp["result"] = 1
        except Exception as e:
            print(e)
            resp["result"] = 0
        return  JsonResponse(resp)


class SpiderControl(View):

    def get(self,request,id,flag):
        resp = dict()

        try:
            spiderId = FileContent.objects.filter(file_id=id)
            if spiderId:
                spider = spiderId[0]
                if flag == STATUS.UNPAUSE:
                    spider.status = 1
                else:
                    spider.status = flag
                spider.save()
                nodeService.control_spider(spider,flag)
                resp['result'] = 1
        except Exception as e:
            resp['result'] = 0
        return JsonResponse(resp)


















