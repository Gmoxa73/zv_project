from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Address, Okrug, Device, Work
from .serializers import AddressSerializer, WorkSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().select_related('okrug').prefetch_related('back_device__type')
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # или [AllowAny]


def address_list(request):
    query = request.GET.get('q', '').strip()
    radio = request.GET.get('ch', '').strip()

    # Добавить поиск по id по ip или по адресу

    if query:
        if radio == '1':
            addr = Address.objects.filter(name__icontains=query).select_related('okrug')
        elif radio == '2':
            addr = Address.objects.filter(back_device__ip__icontains=query).select_related('okrug')
        elif radio == '3':
            addr = Address.objects.filter(adr_id__icontains=query).select_related('okrug')
        elif radio == '4':
            addr = Address.objects.filter(cms__icontains=query).select_related('okrug')
    else:
        addr = Address.objects.all().select_related('okrug')


    # Округа из найденных адресов
    okrug_ids = {a.okrug_id for a in addr.order_by('adr_id') if a.okrug}
    okrugs = Okrug.objects.filter(id__in=okrug_ids).annotate(address_count=Count('back_addresses'))

    if len(okrug_ids) == 1:
        template = 'raion_detail2.html'
    elif len(okrugs) > 1:
        template = 'start.html'
    else:
        template = 'start.html'

    context = {
        'addr': addr,
        'okrugs': okrugs,
        'one_okrug': len(okrug_ids) == 1,
        'okrug_names': [a.okrug.name for a in addr if a.okrug],
        'groups': {a.okrug.name: [] for a in addr if a.okrug},  # можно заполнить списки позже если нужно
        'q': query,
    }
    return render(request, template, context)

def raion_detail(request, pk, q=None):
    okrug = get_object_or_404(Okrug, pk=pk)
    query = request.GET.get('q', '').strip()
    radio = request.GET.get('ch', '').strip()
    if query:
        if radio == '1':
            addresses = Address.objects.filter(
                okrug=okrug,
                name__icontains=query  # можно расширить на другие поля
            )
        elif radio == '3':
            addresses = Address.objects.filter(
                okrug=okrug,
                adr_id__icontains=query,
            )
        elif radio == '2':
            addresses = Address.objects.filter(
                okrug=okrug,
                back_device__ip__icontains=query,
            )
    else:
        addresses = Address.objects.filter(okrug=okrug)

    context = {
        'okrug': okrug,
        'addresses': addresses,
        'query': query,
    }
    return render(request, 'raion_detail.html', context)

def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'device_detail.html', {'device': device})

def destination_page(request, addr_id):
    return render(request, 'destination_page.html', {'addr_id': addr_id})

class WorkListCreateView(APIView):
    """
    GET: список работ
    POST: создание новой работы
    """

    def get(self, request):
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class WorkDetailView(RetrieveUpdateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer