from rest_framework import serializers
from second_app.models import Task, Category, SubTask, User
from datetime import date
import re

#USER REGISTRATION

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def validate_password(self, value):
        if not re.search(r"\d", value) or not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру и заглавную букву.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


#СATEGORY

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория с таким именем уже существует.")
        return value

    def create(self, validated_data):
        name = validated_data.get("name")
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": "Категория с таким именем уже существует."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name")
        if Category.objects.exclude(pk=instance.pk).filter(name=name).exists():
            raise serializers.ValidationError({"name":"Категория с таким именем уже существует"})
        return super().update(instance, validated_data)


#TASK

class BulkTaskSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        tasks = []
        for item in validated_data:
            categories = item.pop('categories', [])
            task = Task.objects.create(**item)
            task.categories.set(categories)
            tasks.append(task)
        return tasks

class TaskSerializer(serializers.ModelSerializer):
    #categories = CategorySerializer(many=True, required=False)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    class Meta:
        model = Task
        fields = '__all__'
        list_serializer_class = BulkTaskSerializer
        read_only_fields = ['owner']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'categories', 'created_at']
        read_only_fields = ['created_at']

    def validate_deadline(self, value):
        if value < date.today():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
        return value




class SubTaskSerializer(serializers.ModelSerializer):
    main_task_name = serializers.CharField(source='main_task.title', read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'status', 'created_at', 'deadline', 'main_task_name', 'task']
        read_only_fields = ['owner']

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']




