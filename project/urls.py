from rest_framework import routers
from django.contrib import admin
from django.urls import path, include

#JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
 
from shop.views import CategoryViewset, ProductViewset, ArticleViewset, AdminCategoryViewset, AdminArticleViewset
# from shop.views import CategoryAPIView
# from shop.views import ProductAPIView
# transformer notre  ApiView  en un  ModelViewset pour que notre view puisse être connectée à notre routeur.
# Un ModelViewset  est comparable à une super vue Django qui regroupe à la fois CreateView, UpdateView, DeleteView, ListView  et DetailView.

# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’


# router.register('category', CategoryViewset, basename='category')
# router.register('product', CategoryViewset, basename='product')
# router.register('article', CategoryViewset, basename='article')
# ca ne marchait pas car j'avais CategoryViewset partout !!!


#/!\ Attention a la deuxieme variable !!!
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
router.register('admin/article', AdminArticleViewset, basename='article-category')
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
