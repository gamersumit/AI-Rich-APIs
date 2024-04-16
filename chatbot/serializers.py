from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    question = serializers.CharField(max_length = 10000)