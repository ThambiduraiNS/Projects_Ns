from io import BytesIO 
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
from reportlab.lib.pagesizes import letter, TABLOID
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
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

# def pdf(request):
#     data = Course.objects.all()
    
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=TABLOID)
#     elements = []

#     # Define the table data
#     table_data = [["Course Name", "Technologies", "Description", "Image"]]
    
#     for course_obj in data:
#         # Retrieve the image
#         image_path = ""
#         image_data = None
#         print(course_obj.Images.url)
#         try:
#             response = requests.get(course_obj.Images.url, stream=True)
#             if response.status_code == 200:
#                 image = PILImage.open(response.raw)
#                 image_path = f"temp_image_{course_obj.id}.png"
#                 image.save(image_path)
#                 image_data = Image(image_path, 2*inch, 2*inch)
#         except Exception as e:
#             image_data = Paragraph("Image not available", getSampleStyleSheet()['Normal'])

#         # Create a Paragraph for the description to handle overflow
#         description = Paragraph(course_obj.Description, getSampleStyleSheet()['Normal'])

#         # Add the course data to the table
#         course_row = [
#             course_obj.Title,
#             course_obj.Technologies,
#             description,
#             image_data
#         ]
#         table_data.append(course_row)

#     # Create the table
#     table = Table(table_data, colWidths=[2*inch, 1.5*inch, 3.5*inch, 2*inch])

#     # Add a table style
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 14),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     elements.append(table)
#     doc.build(elements)

#     buffer.seek(0)
#     x = datetime.datetime.now()
#     date_format = x.strftime("%Y-%m-%d")
#     time_format = x.strftime("%H-%M-%S")
#     save_path = f'pdf/course_list_{date_format}_{time_format}.pdf'
    
#     with open(save_path, 'wb') as f:
#         f.write(buffer.getvalue())
    
#     return HttpResponse(f"PDF file has been generated and saved at: {save_path}")


from django.http import Http404

from . import renderers

def pdf(request, *args, **kwargs):
    data = Course.objects.all()
    
    if not data:
        raise Http404("No courses available.")
    
    content_list = []
    for course_obj in data:
        content_list.append({
            'Course_Name': course_obj.Title, 
            'Technologies': course_obj.Technologies,
            'Description': course_obj.Description,
            'Images': course_obj.Images,
        })
        print(course_obj.Images)
    content = {'courses': content_list}
    return renderers.render_to_pdf('Admin_Login_App/course_data_list.html', content)

import csv
from django.template import loader
from django.http import HttpResponse

import openpyxl
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.styles import Font, Alignment, Border, Side
from PIL import Image as PILImage
from io import BytesIO

def csv_view(request):
    data = Course.objects.all()

    # Create an Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active

    # Define header row with font style and alignment
    header_row = ['Course Name', 'Topics', 'Description', 'Images']
    ws.append(header_row)
    for cell in ws[1]:
        cell.font = Font(bold=True, color='FF0000')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Set column widths for better readability
    column_widths = [20, 30, 50, 20]
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

    # Add data rows with alignment and borders
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for idx, item in enumerate(data, start=2):
        ws.append([item.Title, item.Technologies, item.Description])

        # Align text and apply borders
        for cell in ws[idx]:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            cell.border = thin_border

        # Add image to the worksheet if it exists
        if item.Images:
            image_path = item.Images.path  # Get the file path of the image

            # Resize the image
            with PILImage.open(image_path) as img:
                max_width = 50
                max_height = 50
                img.thumbnail((max_width, max_height))

                # Save the resized image to a BytesIO object
                image_stream = BytesIO()
                img.save(image_stream, format='PNG')
                image_stream.seek(0)

                # Create an ExcelImage object from the BytesIO object
                excel_img = ExcelImage(image_stream)

                # Adjust the row height to match the image height
                row_height = img.height * 0.75  # Adjust the scaling factor if needed
                ws.row_dimensions[idx].height = row_height

                # Center the image in the cell
                col_width = ws.column_dimensions['D'].width
                img_width, img_height = excel_img.width, excel_img.height
                x_offset = (col_width * 7.5 - img_width) / 2  # Approx 7.5 pixels per Excel column unit
                y_offset = (row_height - img_height) / 2

                excel_img.anchor = f'D{idx}'  # Adjust the cell reference to the correct column
                ws.add_image(excel_img)

                # Set the position of the image using offset
                excel_img.anchor += f" - {int(x_offset)} - {int(y_offset)}"

    # Create an in-memory file-like object to save the workbook
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Create the HTTP response with Excel content type and attachment header
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="generated_excel.xlsx"'

    return response


