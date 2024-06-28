import io
import os
import requests

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.authentication import JWTAuthentication
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .forms import CoursesForm, UpdateCourseForm, viewCourseForm
from .models import AdminLogin, Course, PartnerLogo, Testimonial, PlacementStory, FAQ, Blog, Career
from .serializers import CourseSerializer, UserSerializer

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .authentication import JWTAuthentication
# ----------------------------- Admin Views ----------------------------



def admin_login_view(request):
    return render(request, 'Admin_Login_App/AdminLogin.html')

def admin_login_submit(request):
    # print(request)
    return HttpResponse("Welcome")
    # return render(request, 'Admin_Login_App/AdminLogin.html')

def dashboard_view(request):
    return render(request, 'Admin_Login_App/Admin_Body.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('admin_login')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

# ---------------------------- Admin Login API ----------------------------

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AdminLoginAPI(APIView):
    
    # def post(self, request):
    #     username = request.data.get('username')
    #     print(username)
    #     password = request.data.get('password')
    #     print(password)
    #     user = authenticate(username=username, password=password)
    #     if user:
    #         refresh = RefreshToken.for_user(user)
    #         return Response({
    #             'access': str(refresh.access_token),
    #             'refresh': str(refresh)
    #         })
    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        # user = AdminLogin.objects.filter(email=email).first()
        user = AdminLogin.objects.filter(username = username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
    

        token = jwt.encode(payload, 'secret', algorithm='HS256')
    
        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        # token = jwt.decode(jwt.encode(payload, 'secret', algorithm='HS256'), 'secret', algorithms=['HS256'])

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True, max_age=24 * 60 * 60)
        response.data = {
            'jwt': token
        }
        return response

# ---------------------------- Admin User Info API ----------------------------

class get_admin_usernames(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     admin_usernames = AdminLogin.objects.values_list('username', flat=True)
    #     return Response(list(admin_usernames))

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(jwt=token, key='secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = AdminLogin.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# ---------------------------- Course Views ---------------------------------

def course_view(request):
    data = Course.objects.order_by('Title').all()
    paginator = Paginator(data, 5)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'Admin_Login_App/courses.html', {'page_obj': page_obj})

def course_page_view(request):
    form = CoursesForm()
    return render(request, 'Admin_Login_App/course_page.html', {'form': form})

def navbar_save_view(request):
    return render(request, 'Admin_Login_App/navbar_save_course.html')

def navbar_view_course(request):
    return render(request, 'Admin_Login_App/navbar_view_course.html')

def update_course(request, id):
    course = Course.objects.get(id=id)
    form = UpdateCourseForm(instance=course)
    return render(request, 'Admin_Login_App/course_update.html', {'form': form, 'datas': course})

def view_course(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'Admin_Login_App/view_course.html', {'datas': course})

def delete_course(request, id):
    obj = Course.objects.get(id=id)
    return render(request, 'Admin_Login_App/navbar.html', {'datas': obj})

# ---------------------------- Course API -----------------------------------

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class CourseUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    partial = True
    
    
class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(print("delete Movie"))
# ----------------------------- PDF Generation ----------------------------

def pdf(request):
    data = Course.objects.all()
    field_height = 20
    total_height = len(data) * field_height * 6  # Assuming you have 6 fields per course

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=(letter[0], total_height))
    p.setFont('Times-Roman', 14)
    y_position = total_height - 20

    for course_obj in data:
        data_row = f"Course Name: {course_obj.Title}, Technologies: {course_obj.Technologies}, Description: {course_obj.Description}, Status: {course_obj.status}"
        p.drawString(20, y_position, data_row)
        y_position -= field_height

        try:
            response = requests.get(course_obj.Images.url, stream=True)
            if response.status_code == 200:
                image = PILImage.open(response.raw)
                image_path = f"image_{course_obj.id}.png"
                image.save(image_path)
                p.drawImage(image_path, 20, y_position - 100, width=100, height=100)
                y_position -= 120
        except Exception as e:
            p.drawString(20, y_position, f"Image could not be loaded: {str(e)}")
            y_position -= field_height

        if y_position <= 50:
            p.showPage()
            p.setFont('Times-Roman', 14)
            y_position = total_height - 20

    p.showPage()
    p.save()

    buffer.seek(0)
    x = datetime.now()
    date_format = x.strftime("%Y-%m-%d")
    time_format = x.strftime("%Hhr-%Mm-%Ss")
    save_path = f'pdf/formapp_{date_format}_{time_format}.pdf'
    
    with open(save_path, 'wb') as f:
        f.write(buffer.getbuffer())
    
    return HttpResponse(f"PDF file has been generated and saved at: {save_path}")
