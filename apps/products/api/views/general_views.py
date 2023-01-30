from rest_framework import viewsets
from rest_framework import status
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

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id = self.kwargs['pk'], state = True)

    def list(self, request):
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        return Response(data.data)

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Categoria registrada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Categoria actualizada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if self.get_object().exists():
            category = self.get_object().get()
            category.state = False
            category.save()
            return Response({'message':'Categoria eliminada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'message':'No se encontro la categoria'}, status=status.HTTP_400_BAD_REQUEST)