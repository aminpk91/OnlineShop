from PIL import Image
from django.db import models
from django.utils.text import slugify
# Create your models here.



class Tag(models.Model):
    name = models.CharField(max_length=255)
    tag_parent = models.ForeignKey(to = 'self', on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return self.name


def model_image_directory_path_article(instance, filename):
    return f'{instance.__class__.__name__}/{instance.slug}/{filename}'


class Article(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(null=True,blank=True)
    tags = models.ManyToManyField(to=Tag)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to=model_image_directory_path_article,null=True,blank=True)

    def __str__ (self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode =True)
        # super().save(*args, **kwargs)
        # img = Image.open(self.image.path)
        # output_size = (840, 620)
        # img = img.resize(output_size)
        # img.save(self.image.path)
        return super().save(*args, **kwargs)


def model_image_directory_path(instance, filename):
    return f'{instance.__class__.__name__}/{instance.article.slug}/{slugify(instance.sub_title)}/{filename}'


class Paragraph(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE,related_name='paragraph')
    sub_title = models.CharField(max_length=500)
    body = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=model_image_directory_path,null=True,blank=True)

    def __str__(self):
        return self.sub_title


class BlogComment(models.Model):
    author = models.CharField(max_length=255,default='ناشناس')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE,related_name='comment',null=True)
    reply_to = models.ForeignKey(to='self',related_name='replies',on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True)


