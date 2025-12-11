from rest_framework import serializers
from .models import Okrug, Address, Device, TypeA

class TypeASerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeA
        fields = ['id', 'name']


class DeviceSerializer(serializers.ModelSerializer):
    type = TypeASerializer()

    class Meta:
        model = Device
        fields = ['id', 'cms', 'ip', 'type']


class AddressSerializer(serializers.ModelSerializer):
    # допускаем вложенную запись устройств
    okrug = serializers.PrimaryKeyRelatedField(queryset=Okrug.objects.all())
    okrug_name = serializers.SerializerMethodField()
    back_device = DeviceSerializer(many=True, required=False)

    class Meta:
        model = Address
        fields = ['id', 'name', 'description', 'adr_id', 'lat', 'lng', 'okrug', 'okrug_name', 'back_device']

    def get_okrug_name(self, obj):
        return obj.okrug.name if obj.okrug is not None else None

    def create(self, validated_data):
        devices_data = validated_data.pop('back_device', [])
        address = Address.objects.create(**validated_data)

        for dev_data in devices_data:
            type_data = dev_data.pop('type')
            type_obj, _ = TypeA.objects.get_or_create(**type_data)
            Device.objects.create(address=address, type=type_obj, **dev_data)
        return address

    def update(self, instance, validated_data):
        devices_data = validated_data.pop('back_device', None)

        instance.name = validated_data.get('name', instance.name)
        instance.adr_id = validated_data.get('adr_id', instance.adr_id)
        if 'okrug' in validated_data:
            instance.okrug = validated_data['okrug']
        instance.save()

        if devices_data is not None:
            # простая стратегия: удалить старые и добавить новые
            instance.back_device.all().delete()
            for dev_data in devices_data:
                type_data = dev_data.pop('type')
                type_obj, _ = TypeA.objects.get_or_create(**type_data)
                Device.objects.create(address=instance, type=type_obj, **dev_data)

        return instance