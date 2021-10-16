from rest_framework import serializers
from .models import Device, Pill, Config


class DeviceSerializer(serializers.Serializer):
    passcode = serializers.CharField(max_length=128)
    timezone_name = serializers.CharField(max_length=128)

class ConsumableSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=128)
    form = serializers.CharField(max_length=128)
    dosage = serializers.CharField(max_length=128)
    expiration_date = serializers.DateField()
    passcode_mandatory = serializers.BooleanField()
    max_doses = serializers.IntegerField()


class SlotSerializer(serializers.Serializer):
    slot_index = serializers.IntegerField()
    consumable_id = serializers.CharField(max_length=128)
    exact_pill_count = serializers.IntegerField()


class TableSerializer(serializers.Serializer):
    device = DeviceSerializer()
    consumables = ConsumableSerializer(many=True)
    slots = SlotSerializer(many=True)

class ConfigDeviceSerializer(serializers.Serializer):
    Table = TableSerializer()

    def create(self, validated_data):
        table_data = validated_data['Table']
        device = self.context['device']
        config = Config.objects.create(device=device, **(table_data['device']))
        consumables = table_data['consumables']
        for consumable in consumables:
            slots = table_data["slots"]
            myslot = None
            for slot in slots:
               if myslot is None:
                  if consumable["id"] in slot.values():
                    myslot = slot
                    # table_data["slots"].remove(myslot)
                    break
            Pill.objects.create(config=config, name=consumable['name'],
                                expires=consumable['expiration_date'],
                                dosage=consumable['dosage'],
                                passcode_required=consumable['passcode_mandatory'],
                                form=consumable['form'],max_manual_doses=consumable['max_doses'],
                                slot=myslot['slot_index'],exact_pill_count=myslot['exact_pill_count'])
        return config


    def update(self, instance, validated_data):
        if self.hasChanged(instance, validated_data):
            config = self.create(validated_data)
            Config.objects.filter(id=instance.id).update(active=False)
            return config
        else:
            return instance

    def hasChanged(self, instance, validated_data):
        if instance.passcode != ((validated_data['Table'])['device'])["passcode"]:
            return True
        if instance.timezone_name != ((validated_data['Table'])['device'])["timezone_name"]:
            return True
        instance_pills = Pill.objects.filter(config_id=instance.id)
        consumables = (validated_data['Table'])['consumables']
        for consumable in consumables:
            slots = (validated_data['Table'])["slots"]
            myslot = None
            for slot in slots:
               if myslot is None:
                  if consumable["id"] in slot.values():
                    myslot = slot
                    # table_data["slots"].remove(myslot)
                    break
            find = instance_pills.filter(name=consumable['name'],
                                expires=consumable['expiration_date'],
                                dosage=consumable['dosage'],
                                passcode_required=consumable['passcode_mandatory'],
                                form=consumable['form'],max_manual_doses=consumable['max_doses'],
                                slot=myslot['slot_index'],exact_pill_count=myslot['exact_pill_count'])
            if not find.exists():
                return True

        return False


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
