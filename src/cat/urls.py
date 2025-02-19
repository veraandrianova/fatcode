from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('get_hint/', views.HintView.as_view()),
    path('inventory/<int:id>/', views.InventoryView.as_view(
        {"post": "create", "get": "list", 'patch': 'update'}
    )),
    path('phrases/', views.PhraseView.as_view()),
    path('', views.CatView.as_view({"get": "list"}), name="cat_list"),
    path('<int:pk>/', views.CatView.as_view({"get": "retrieve"}), name="cat_detail"),
    path('your/', views.CatUserView.as_view({"get": "list"}), name="user_cat"),
    path('your/<int:pk>/', views.CatUserView.as_view({"patch": "update"}), name="cat_update"),
    path('top/', views.TopCatView.as_view()),
]
