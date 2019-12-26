from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    nick_name = models.CharField(max_length=50,verbose_name="昵称",default="")
    birthday = models.DateField(verbose_name="生日",null=True,blank=True)
    gender = models.CharField(choices=(("male","男"),("female","女")),default="male",max_length=5)
    image = models.ImageField(upload_to="image/%Y/%m",default="image/default.png",max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.nick_name

class FileContent(models.Model):
    file_zip = models.FileField(upload_to="upload/%Y/%m")
    cmd = models.CharField(max_length=20,verbose_name="运行",default="")
    display_name = models.CharField(max_length=20,verbose_name="显示名",default="")
    file_id = models.CharField(max_length=30,verbose_name="爬虫id",default="")
    settings_path = models.CharField(max_length=50, verbose_name="配置文件",default="")
    spider_class = models.CharField(max_length=50,verbose_name="爬虫类",default="")
    status = models.CharField(choices=((1,"start"),(2,"pause"),(3,"stop"),(4,"unpause")),max_length=15,default="")

    class Meta:
        verbose_name = "压缩包"
        verbose_name_plural = verbose_name
        db_table = "zip_info"
