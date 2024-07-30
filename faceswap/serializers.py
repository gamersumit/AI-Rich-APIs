from rest_framework import serializers
from .models import FaceSwap

class FaceSwapSerializer(serializers.ModelSerializer):
    source_url = serializers.SerializerMethodField()
    target_url = serializers.SerializerMethodField()
    swapped_url = serializers.SerializerMethodField()

    class Meta:
        model = FaceSwap
        fields = ['id', 'source_url', 'target_url', 'swapped_url']

    def get_source_url(self, obj):
        if obj.source:
            return obj.source.url
        return None

    def get_target_url(self, obj):
        if obj.target:
            return obj.target.url
        return None

    def get_swapped_url(self, obj):
        if obj.swapped:
            return obj.swapped.url
        return None
