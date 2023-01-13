from django.db import models 
class MenuItem(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='menu_images/')
    price=models.DecimalField(max_digits=5,decimal_places=2)
    category=models.ManyToManyField('Category',related_name='item')
   #each category can have many menu item and many menu item can have many categoies
    
    def __str__(self):
        return self.name 
class Category(models.Model):
    name=models.CharField(max_length=100) 
    def __str__(self):
        return self.name 

class OrderModels(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    items=models.ManyToManyField('MenuItem',related_name='order',blank=True)
    name=models.CharField(max_length=50,blank=True)
    email=models.CharField(max_length=50,blank=True)
    street=models.CharField(max_length=50,blank=True)
    city=models.CharField(max_length=50,blank=True)
    state=models.CharField(max_length=20,blank=True)
    zipcode=models.IntegerField(blank=True,null=True)
    #each order can have multiple menuitems and each menu items can have multiple order
    
    def __str__(self):
        return f'Order:{self.created_on.strftime("%b %d %I: %M %p")}' 
    



