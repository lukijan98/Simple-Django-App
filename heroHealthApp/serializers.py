from rest_framework import serializers
from .models import Device, Pill, Config


# class DeviceSerializer(serializers.Serializer):
#     class Meta:
#         model = Device
#         fields = '__all__'

class PillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        exclude = ['config']


class ConfigFrontendSerializer(serializers.ModelSerializer):
    pills = PillSerializer(source='pill_set',many=True)

    class Meta:
        model = Config
        exclude = ['device', 'active']

    def create(self, validated_data):
        pills_data = validated_data.pop('pill_set')
        device = self.context['device']
        config = Config.objects.create(device=device, **validated_data)
        for pill in pills_data:
            Pill.objects.create(config=config, **pill)
        return config

