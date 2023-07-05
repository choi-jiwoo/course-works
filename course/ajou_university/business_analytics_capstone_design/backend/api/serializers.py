from rest_framework.serializers import ModelSerializer
from api.models import Stay, Cafe, Res, CafeTag, ResTag, CafeKwrd, ResKwrd


class StaySerializer(ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'


class CafeSerializer(ModelSerializer):
    class Meta:
        model = Cafe
        fields = '__all__'


class ResSerializer(ModelSerializer):
    class Meta:
        model = Res
        fields = '__all__'


class CafeTagSerializer(ModelSerializer):
    class Meta:
        model = CafeTag
        fields = '__all__'


class ResTagSerializer(ModelSerializer):
    class Meta:
        model = ResTag
        fields = '__all__'


class CafeKwrdSerializer(ModelSerializer):
    class Meta:
        model = CafeKwrd
        fields = '__all__'


class ResKwrdSerializer(ModelSerializer):
    class Meta:
        model = ResKwrd
        fields = '__all__'

