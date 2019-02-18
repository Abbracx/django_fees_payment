from django.conf import settings
# from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from djapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('djapp/', include('djapp.urls')),
    path('logout/', views.user_logout, name='logout'),
    path('branch_list/', views.branch_list, name='branch_list'),
    path('pay_fees/<str:order_name>', views.pay_fees, name='pay_fees'),
    path('charge', views.charge, name='charge'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_fail/', views.payment_fail, name='payment_fail'),
    path('import_user/', views.import_user, name='import_user'),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
