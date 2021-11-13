from django.db import models
from django.utils.text import slugify
import os
from PIL import Image
from django.db import models
# Create your models here.


class Category (models.Model):
    name = models.CharField(max_length=100,verbose_name="دسته بندی")
    cat_parent = models.ForeignKey(to='Category',on_delete=models.CASCADE,blank=True,null=True,related_name='child_cat',verbose_name="از مجموعه")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Brands (models.Model):
    name = models.CharField(max_length=50,verbose_name="نام برند")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

class Cat_attr(models.Model):
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE,verbose_name="دسته بندی")
    attr_name = models.CharField(max_length=255,verbose_name="نام ویژگی")

    def __str__(self):
        return self.attr_name

    class Meta:
        verbose_name = "ویژگی دسته "
        verbose_name_plural = "جزییات دسته"

class Productbase(models.Model):

    name = models.CharField(max_length=255,verbose_name="نام محصول")
    slug = models.SlugField(blank=True,null=True,verbose_name="نشانی")
    description = models.TextField(blank=True, null=True,verbose_name="توضیحات")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT,verbose_name="دسته بندی")
    brand = models.ForeignKey(Brands, on_delete=models.RESTRICT,null=True,verbose_name="برند")
    previous_price = models.FloatField(default=0.0,verbose_name="قیمت قبلی")
    price = models.FloatField(default=0.0,verbose_name="قیمت")
    added_time = models.DateTimeField(auto_now_add=True,verbose_name="تاریج ایجاد")
    #updated_time = models.DateTimeField(auto_now_add=True)
    qty = models.IntegerField(default=1,verbose_name="موجودی")
    rate = models.IntegerField(default=3,verbose_name="امتیاز محصول")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


    def __str__ (self):
        return self.name

    def save(self,*args,**kwargs):

        if self.rate > 5:
            self.rate = 5
        if self.rate < 1:
            self.rate = 1

        if not self.slug:
            self.slug = slugify(self.name,allow_unicode =True)
        return super().save(*args,**kwargs)


class Product_attr(models.Model):
    product = models.ForeignKey(to=Productbase,on_delete=models.CASCADE,related_name="attrs",verbose_name="نام محصول")
    cat_attr = models.ForeignKey(to=Cat_attr,on_delete=models.CASCADE,verbose_name="ویژگی دسته")
    attr = models.CharField(max_length=255,verbose_name="ویژگی")

    def __str__(self):
        return self.attr

    class Meta:
        verbose_name = " جزییات محصول"
        verbose_name_plural = "جزییات محصولات"


def model_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'{instance.__class__.__name__}/{instance.product.id}/{filename}'


class ImageProduct(models.Model):
    product = models.ForeignKey(Productbase, on_delete=models.CASCADE, related_name='img',verbose_name="نام محصول")
    image = models.ImageField(upload_to=model_image_directory_path,verbose_name="تصویر محصول")
    default = models.BooleanField(default=False,verbose_name="عکس پیش فرض")

    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        output_size = (540,420)
        img = img.resize(output_size)
        img.save(self.image.path)

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصولات"

class ProductComment(models.Model):
    author = models.CharField(max_length=255,default='ناشناس')
    article = models.ForeignKey(to=Productbase, on_delete=models.CASCADE,related_name='comment',null=True)
    reply_to = models.ForeignKey(to='self',related_name='replies',on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True)
    # rate = models.IntegerField()
