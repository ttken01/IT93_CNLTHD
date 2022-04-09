from rest_framework import serializers
from .models import Category, Course, Lesson, Tag, User, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Category
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
    image =serializers.SerializerMethodField(source='image')


    def get_image(self, obj):
        request = self.context['request']
        # if obj.image and obj.image.name.startswith("/static"):
        #     pass
        # else:
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)


    class Meta:
        model = Course
        fields = ['id', 'subject', 'created_date', 'image', 'category_id']



class TagSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSeriazlier(many=True)

    def get_image(self, obj):
        request = self.context['request']
        # if obj.image and obj.image.name.startswith("/static"):
        #     pass
        # else:
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'updated_date', 'course_id', 'image', 'tags']


class LessonDetailSerializer(LessonSerializer):
    class Meta:
        model = Lesson
        fields = LessonSerializer.Meta.fields + ['content']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'lesson']



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['active']