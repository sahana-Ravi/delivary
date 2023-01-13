from django.shortcuts import render
from django.views import View 
from .models import MenuItem
from .models import OrderModels
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request,'customer/index.html') 

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request,'customer/about.html') 

class Order(View):
    def get(self, request, *args, **kwargs):
        #get every item form each category  
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizers')
        entre = MenuItem.objects.filter(category__name__contains='Entre')
        deserts = MenuItem.objects.filter(category__name__contains='Desert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        #pass into the context
        context = {
            'appetizers':appetizers,
            'entre':entre,
            'desert':deserts,
            'drinks':drinks,
        }


        #render the template
        return render(request,'customer/order.html',context) 
    @csrf_exempt
    def post(self,request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zipcode=request.POST.get('zip')
        oreder_items={
            'items':[]
        }
        # to return the list of all the id's selected
        items = request.POST.getlist('items[]') 
       
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {

                'id': menu_item.pk,
                'name':menu_item.name,
                'price':menu_item.price,
            }
            oreder_items['items'].append(item_data) 

        price=0
        item_ids =[]
        for item in oreder_items['items']:
            price+=item['price']
            item_ids.append(item['id']) 
        order = OrderModels.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zipcode=zipcode)
        order.items.add(*item_ids)
        #after everything is done send confirmation email 
        body=('Thank you for your order! Your Food will be deliverd soon\n'
        f'your total:{price}\n'
        'Thank you again for your order')
        send_mail(
            'Thank you for your order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )
        context = {
            'items': oreder_items['items'],
            'price': price,
            'username':name,
        }
        return render(request,'customer/order_confermation.html',context)
