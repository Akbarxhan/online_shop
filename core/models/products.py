from django.db import models
from django.db.models import IntegerChoices
from django.utils.text import slugify

from core.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    deleted = models.BooleanField(default=False)

    # soft delete
    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

        self.brand_product.all().delete()

    def save(self, *args ,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

    class CustomManager(models.Manager):
        def all(self):
            return self.model.objects.filter(deleted=False)

        def get(self,*args,**kwargs):
            return self.model.objects.filter(deleted=False,*args,**kwargs).first()

    objects = CustomManager()


class Brand(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='brand/')
    deleted = models.BooleanField(default=False)

    # soft delete
    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
    # unga tegishli productlar ham o'chadi
        self.brand_product.all().delete()



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class CustomManager(models.Manager):
        def all(self):
            return self.model.objects.filter(deleted=False)

        def get(self, *args, **kwargs):
            return self.model.objects.filter(deleted=False, *args, **kwargs).first()

    objects = CustomManager()

# class RateChoice(IntegerChoices)




class Product(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField(upload_to='products/',max_length=512)
    info = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    delete = models.BooleanField(default=False)
    # price
    price = models.PositiveIntegerField(default=0)
    discount = models.IntegerField(default=0)

    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True, related_name='brand_product')
    ctg = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True, related_name='ctg_product')

    def get_price(self):
        return self.price * (1-self.discount/100)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()


class Rate(models.Model):
    user =models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    rate = models.SmallIntegerField(default=5,choices=[
        (1,'*'),
        (2, '**'),
        (3, '**'),
        (4, '****'),
        (5, '*****')
    ])
    product =models.ForeignKey(Product,on_delete=models.CASCADE, related_name='product_rate')


class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="cart_pro")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_cart')
    quentity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0,editable=False)

    def save(self,*args,**kwargs):
        self.total_price = self.product.get_price() * self.quentity