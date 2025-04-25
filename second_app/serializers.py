from rest_framework import serializers
from second_app.models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'
