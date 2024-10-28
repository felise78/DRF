# Ne permettez que la lecture
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer,\
    ProductDetailSerializer, ProductListSerializer, ArticleSerializer

# le mixin : 

class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()

class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
 
    def get_queryset(self):
        return Category.objects.all()

class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
 
    serializer_class = CategoryListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()

# class CategoryViewset(ReadOnlyModelViewSet):
 
 
#     def get_queryset(self):
#         return Category.objects.filter(active=True)
 
#     def get_serializer_class(self):
#     # Si l'action demandée est retrieve nous retournons le serializer de détail
#         if self.action == 'retrieve':
#             return self.detail_serializer_class
#         return super().get_serializer_class()

#     # ajouter une action disable  que nous souhaitons accessible en POST:
#     @action(detail=True, methods=['post'])
#     def disable(self, request, pk):
#         # Nous avons défini notre action accessible sur la méthode POST seulement
#         # elle concerne le détail car permet de désactiver une catégorie

#         # Nous avons également mis en place une transaction atomique car plusieurs requêtes vont être exécutées
#         # en cas d'erreur, nous retrouverions alors l'état précédent

#         # Désactivons la catégorie
#         self.get_object().disable()
#         # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
#         return Response()

class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
 
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
 
    def get_queryset(self):
    # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

class AdminArticleViewset(ModelViewSet):
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        return Article.objects.all()

class ArticleViewset(ReadOnlyModelViewSet):
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
    # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Article.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

# AVEC le router / ModelViewSet / mais sans READONLY ce qui autorise trop d'operations

# from rest_framework.viewsets import ModelViewSet
 
# from shop.models import Category
# from shop.serializers import CategorySerializer
 
# class CategoryViewset(ModelViewSet):
 
#     serializer_class = CategorySerializer
 
#     def get_queryset(self):
#         return Category.objects.all()


# AVEC APIView :

# from rest_framework.views import APIView
# from rest_framework.response import Response
 
# from shop.models import Category
# from shop.models import Product
# from shop.serializers import CategorySerializer
# from shop.serializers import ProductSerializer
 
# class CategoryAPIView(APIView):
 
#     def get(self, *args, **kwargs):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)

# class ProductAPIView(APIView):
 
#     def get(self, *args, **kwargs):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)