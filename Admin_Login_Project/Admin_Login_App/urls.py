from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    admin_login_view, dashboard_view, logout_view, user_logout,admin_login_submit,
    AdminLoginAPI, get_admin_usernames,
    CourseListCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView,
    course_view, course_page_view, navbar_save_view,navbar_view_course,
    update_course, delete_course, view_course, pdf, RegisterView, LogoutView
    # MyTokenObtainPairView, MyTokenRefreshView
)

urlpatterns = [

    # path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_login_submit/', admin_login_submit, name='admin_login_submit'),
    
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_logout/', user_logout, name='user_logout'),
    
    path('api/admin_login/', AdminLoginAPI.as_view(), name='admin_login_api'),
    path('api/get_admin_usernames/', get_admin_usernames.as_view(), name='get_admin_usernames'),
    
    path('api/courses/', CourseListCreateView.as_view(), name='course_list_create'),
    path('api/courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('api/update_courses/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('api/delete_courses/<int:pk>/', CourseDetailView.as_view(), name='course_delete'),
    
    path('courses/', course_view, name='courses'),
    path('course_page/', course_page_view, name='course_page'),
    path('navbar_save_course/', navbar_save_view, name='navbar_save_course'),
    path('navbar_view_course/', navbar_view_course, name='navbar_view_course'),
    path('update_course/<int:id>/', update_course, name='update_course'),
    path('view_course/<int:id>/', view_course, name='view_course'),
    path('delete_course/<int:id>/', delete_course, name='delete_course'),
    
    path('pdf/', pdf, name='pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

