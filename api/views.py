from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import DestroyAPIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.conf import settings
from .models import Container, Image
from .serializers import ImageSerializer, UserSerializer, UserProfileSerializer, ChangePasswordSerializer
from .permissions import IsAdminUser, IsRegularUser

User = get_user_model()

# ✅ User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ✅ User Login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# ✅ Admin-Only View
class AdminOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Welcome Admin! You have full access."})

# ✅ User-Only View
class UserOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get(self, request):
        return Response({"message": "Welcome User! You have limited access."})

# ✅ User Profile Update
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user

# ✅ Change Password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(self.get_object(), serializer.validated_data)
        return Response({"message": "Password updated successfully!"})

# ✅ Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# ✅ List All Users (Admin Only)
class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

# ✅ Delete User Account
class DeleteUserView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        if not user:
            return Response({"detail": "User not found", "code": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User account deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

# ✅ Image Upload with Admin Notification
class ImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()

            # ✅ Notify Admin via Email
            send_mail(
                subject="📸 New Image Uploaded!",
                message=f"A new image has been uploaded to container {request.data.get('container')}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            return Response({"message": "Image uploaded & admin notified!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Fetch Images with Date Filter
class ImageFetchView(APIView):
    def get(self, request, *args, **kwargs):
        container_number = request.query_params.get('container_number')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not container_number:
            return Response({"error": "Container number is required."}, status=status.HTTP_400_BAD_REQUEST)

        images = Image.objects.filter(container__container_number=container_number)

        # Convert and filter by date range
        if start_date:
            start_date = timezone.make_aware(datetime.combine(parse_date(start_date), datetime.min.time()))
            images = images.filter(uploaded_at__gte=start_date)

        if end_date:
            end_date = timezone.make_aware(datetime.combine(parse_date(end_date), datetime.max.time()))
            images = images.filter(uploaded_at__lte=end_date)

        serializer = ImageSerializer(images, many=True)
        return Response({"images": serializer.data}, status=status.HTTP_200_OK)

# ✅ Create New Container
class CreateContainerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        container_number = request.data.get("container_number")
        if not container_number:
            return Response({"error": "Container number is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Container.objects.filter(container_number=container_number).exists():
            return Response({"error": "Container already exists"}, status=status.HTTP_400_BAD_REQUEST)

        container = Container.objects.create(container_number=container_number, uploaded_by=request.user)
        return Response({
            "id": container.id,
            "container_number": container.container_number,
            "created_at": container.created_at
        }, status=status.HTTP_201_CREATED)
