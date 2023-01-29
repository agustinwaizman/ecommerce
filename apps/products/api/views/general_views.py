from rest_framework import viewsets
from rest_framework.response import Response
from apps.base.api import GeneralListApiView
from apps.products.models import MeasureUnit
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer, IndicatorSerializer


class MeasureUnitViewSet(viewsets.GenericViewSet):
    """
    Unidad en la que se mide la cantidad de stock de un producto
    """
    model = MeasureUnit
    serializer_class = MeasureUnitSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def list(self, request):
        """
        Retorna todas las unidades de medidas disponibles.

        params.
        name ----> nombre de la unidad de medida
        """
        data = self.get_queryset()
        data = self.get_serializer(data, many = True)
        return Response(data.data)

    def create(self,request):
        return Response({})


class IndicatorViewSet(viewsets.GenericViewSet):
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def list(self, request):
        """
        Retorna todas los indicadores de descuento disponibles.

        params.
        name ----> nombre del indicador
        """
        data = self.get_queryset()
        data = self.get_serializer(data, many = True)
        return Response(data.data)


class CategoryProductViewSet(viewsets.GenericViewSet):
    serializer_class = CategoryProductSerializer