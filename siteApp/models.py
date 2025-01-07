from django.db import models

from base.model import BaseModel
from django.utils.text import slugify
# Create your models here.



class Category(BaseModel):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category_image = models.ImageField(upload_to='category')


    def save(self,*args ,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name





class Product(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,related_name='products')
   
    
    def save(self,*args ,**kwargs):
        self.slug = slugify(self.title)
        super(Product,self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class ProductImage(BaseModel):
    product = models.ForeignKey('Product',on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='products/')




class Coupon(BaseModel):
    coupn_code = models.CharField(max_length=10)
    is_expire = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)