from django.db import models
from django.contrib.auth.models import User
from base.model import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_accout_activatio_email
from siteApp.models import *
# Create your models here.



class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_varified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)
    prifile_image = models.ImageField(upload_to='profile')


    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False,cart__user = self.user).count()


class userProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=150,blank=True)
    address = models.TextField(blank=True)
    


@receiver(post_save,sender = User)
def send_email_token(sender, instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            print(f"Sending email to {email} with token {email_token}")  
            send_accout_activatio_email(email,email_token)
    except Exception as e :
        print(e)


class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, null=True, blank=True)  # Transaction ID from JazzCash
    payment_method = models.CharField(max_length=50, null=True, blank=True)  # E.g., 'JazzCash'
    payment_date = models.DateTimeField(null=True, blank=True) 

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.get_total_price())
        if self.coupon:
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price

        return sum(price)



class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
   


    def get_product_price(self):
        price = [self.product.price]
        return sum(price)
    
    def get_total_price(self):
        return self.product.price * self.quantity