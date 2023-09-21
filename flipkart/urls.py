from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework import routers

from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path("",views.index,name='home'),
    path("contact",views.contact,name='contact'),
    path("signup",views.signup,name='signup'),
    path("login",views.Login,name='login'),
    path("logout",views.Logout,name='logout'),
    path("cart",views.cart_details,name='cart'),
    path("checkout",views.check_cart,name='checkout'),
    path("order",views.order_details,name='order'),
    path('api/', include(router.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)