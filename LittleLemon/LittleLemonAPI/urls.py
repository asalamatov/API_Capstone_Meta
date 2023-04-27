from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.menuitems_list),
    path('menu-items/<str:menuItem>', views.menuitem_detail),
    
    path('categories/', views.CategoriesView.as_view()),
    
    path('groups/manager/users/', views.ManagerUsersView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerSingleUserView.as_view()),
    path('groups/delivery-crew/users/', views.Delivery_crew_management.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.Delivery_crew_management_single_view.as_view()),
    
    path('cart/menu-items/', views.CustomerCart.as_view()),
        
    path('orders/', views.Orders_view.as_view()),
    path('orders/<int:pk>', views.Single_Order_view.as_view()),
    
    path('api-token-auth/', obtain_auth_token),
]










