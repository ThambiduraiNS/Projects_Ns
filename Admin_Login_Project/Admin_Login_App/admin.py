from django.contrib import admin
from .models import AdminLogin, Course, Technology, PartnerLogo, Testimonial, PlacementStory, FAQ, Blog, Career

# Register your models here.

class LoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'ph_no', 'is_active', 'is_admin', 'is_staff']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['Title', 'Technologies', 'status', 'created_at', 'modified_at']

class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['Technologies']

class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'created_at', 'modified_at', 'is_active']

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'course', 'date', 'is_active']

class PlacementStoryAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'course', 'date', 'is_active']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at', 'is_active']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_at', 'is_active']

class CareerAdmin(admin.ModelAdmin):
    list_display = ['Job_Heading', 'Location', 'Experience', 'No_Of_Openings', 'Salary', 'Status', 'Job_Type', 'created_at', 'is_active']

admin.site.register(AdminLogin, LoginAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(PartnerLogo, PartnerLogoAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(PlacementStory, PlacementStoryAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Career, CareerAdmin)
