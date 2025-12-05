from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import Address, Okrug, Device
from .serializers import AddressSerializer

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
            addr = Address.objects.filter(adr_number__icontains=query).select_related('okrug')
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
