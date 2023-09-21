from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from . models import *

from django.contrib.auth.hashers import make_password, check_password


def index(request):
    if request.method == "POST":
        product_id = request.POST.get('cartid')
        remove = request.POST.get('remove')
        print("Product_id=", product_id)

        cart_id = request.session.get('cart')
        print("cart_id =", cart_id)
        if cart_id:
            quantity = cart_id.get(product_id)

            if quantity:
                if remove:
                    if quantity <= 1:

                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity-1
                else:
                    cart_id[product_id] = quantity+1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1

        request.session['cart'] = cart_id
        print("session =", request.session['cart'])

    category_obj = Category.objects.all()

    cat_id = request.GET.get('category_id')

    product_name=request.GET.get('search')

    if cat_id:
        product_obj = Product.objects.filter(product_category=cat_id)
    elif product_name:
        product_obj = Product.objects.filter(product_name__icontains=product_name)
    else:
        product_obj = Product.objects.all()

    context = {
        'category_obj': category_obj,
        'product_obj': product_obj
    }

    return render(request, 'home.html', context=context)


def contact(request):
    return render(request, 'contact.html')


def signup(request):
    if request.method == "POST":
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mbl')
        gender = request.POST.get('gender')

        s = Registrations(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=make_password(password),
            mobile=mobile,
            gender=gender
        )
        s.save()
        return HttpResponse("data saved successfully")


def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # fetch_obj=Registrations.objects.all()
        # fetch_obj=Registrations.objects.filter(email='p@gmail.com')
    try:
        fetch_obj = Registrations.objects.get(email=email)
        if check_password(password, fetch_obj.password):
            request.session['name'] = fetch_obj.first_name
            request.session['customer_id'] = fetch_obj.id
            return redirect('home')
            return HttpResponse("login successful")
        else:
            return HttpResponse("plz entae a valid password..")

    except:
        return HttpResponse("plz  enter a valid email....")


def Logout(request):
    request.session.clear()
    return redirect('home')


def cart_details(request):
    ids = list(request.session.get('cart').keys())
    cart_obj = Product.objects.filter(id__in=ids)
    return render(request, 'cart.html', {'cart_obj': cart_obj})


def check_cart(request):
    if request.method == "POST":
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customer_id = request.session.get('customer_id')
        

        if not customer_id:
            return HttpResponse("plz Login...")
        
        cart = request.session.get('cart')
        product_details = Product.objects.filter(id__in=list(cart.keys()))

        for pro in product_details:
            order_details=Order(
                address=address,
                mobile=mobile,
                customer=Registrations(id=customer_id),
                product=pro,
                price=pro.product_price,
                quantity=cart.get(str(pro.id)),
            )
            order_details.save()

        return HttpResponse("Order successfully created")


def order_details(request):
    customer_id=request.session.get('customer_id')
    fetch_order=Order.objects.filter(customer=customer_id)
    tp=0
    for i in fetch_order:
        tp=tp+(i.price *i.quantity)
    context={
        'fetch_order':fetch_order,
        'tp':tp
    }
    return render(request,'order.html',context=context)


from rest_framework import routers, serializers, viewsets
from .serializations import RegistrationsSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = Registrations.objects.all()
    serializer_class = RegistrationsSerializer
