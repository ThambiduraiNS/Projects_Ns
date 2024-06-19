from rest_framework import serializers
from Admin_Login_App.models import *

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course  # Assuming `courses` is the correct model name
        fields = '__all__'

class PlacementPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerLogo
        fields = ['name', 'logo']

    def create(self, validated_data):
        return PartnerLogo.objects.create(**validated_data)

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['student_name', 'picture', 'course', 'date', 'testimonial']

    def create(self, validated_data):
        return Testimonial.objects.create(**validated_data)

class PlacementStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementStory
        fields = ['student_name', 'course', 'testimonial_video', 'date']

    def create(self, validated_data):
        return PlacementStory.objects.create(**validated_data)

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

    def create(self, validated_data):
        return FAQ.objects.create(**validated_data)

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['images', 'title', 'description', 'course']

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['Logo', 'Job_Heading', 'Location', 'Experience', 'No_Of_Openings', 'Salary', 'Status', 'Job_Type', 'Qualification', 'Job_Description', 'Skills_Required']

    def create(self, validated_data):
        return Career.objects.create(**validated_data)
