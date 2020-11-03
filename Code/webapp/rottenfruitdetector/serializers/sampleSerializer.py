from rest_framework import serializers

class SampleSerializer(serializers.Serializer):
        imageId = serializers.CharField()
        rotten = serializers.IntegerField()

class ResponseSerializer(serializers.Serializer):
        imageId = serializers.CharField()
        rotten = serializers.IntegerField()