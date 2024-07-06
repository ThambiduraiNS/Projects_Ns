from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    admin_login_view, dashboard_view, logout_view, user_logout,admin_login_submit,
    AdminLoginAPI, get_admin_usernames,
    CourseListCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView,
    course_view, course_page_view, navbar_save_view,navbar_view_course,
    update_course, delete_course, view_course, export_courses_csv, export_courses_excel, export_courses_pdf, 
    listing_api, KeywordListView,
    RegisterView, LogoutView
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
    
    # path('courses/', course_view, name='courses'),
    # path('courses/', course_view, name='courses'),  # Main courses view
    # path('courses/<int:page>/', course_view, name='course-by-page'),  # Paginated view
    path('course_page/', course_page_view, name='course_page'),
    path('navbar_save_course/', navbar_save_view, name='navbar_save_course'),
    path('navbar_view_course/', navbar_view_course, name='navbar_view_course'),
    path('update_course/<int:id>/', update_course, name='update_course'),
    path('view_course/<int:id>/', view_course, name='view_course'),
    path('delete_course/<int:id>/', delete_course, name='delete_course'),
    
    # path('pdf/', pdf, name='pdf'),
    # path('excel/', excel_view, name='excel'),
    # path('csv/', csv_view, name='csv'),
    
    path('export_courses_csv/', export_courses_csv, name='export_courses_csv'),
    path('export_courses_excel/', export_courses_excel, name='export_courses_excel'),
    path('export_courses_pdf/', export_courses_pdf, name='export_courses_pdf'),
    
    path("course", KeywordListView.as_view(),name="course"),
    # path("course/<int:page>/", listing, name="course-page"),
    # path("page/", listing_api, name="course-api"),
    # path("page/<int:page>/", listing_api, name="course-api"),
    
    
    
    path('courses/', course_view, name='courses'),  # Main courses view
    path('page/', listing_api, name='course-api'),  # API endpoint for courses pagination
    path('page/<int:page>/', course_view, name='course-by-page'),  # Paginated view
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

