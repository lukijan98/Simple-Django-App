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
    pills = PillSerializer(source='pill_set', many=True)

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

    def update(self, instance, validated_data):
        if self.hasChanged(instance, validated_data):
            config = self.create(validated_data)
            Config.objects.filter(id=instance.id).update(active=False)
            return config
        else:
            return instance


    def hasChanged(self, instance, validated_data):
        if instance.passcode != validated_data["passcode"]:
            return True
        if instance.timezone_name != validated_data["timezone_name"]:
            return True
        instance_pills = Pill.objects.filter(config_id=instance.id)
        for pill in validated_data['pill_set']:
            find = instance_pills.filter(**pill)
            if not find.exists():
                return True
        return False
