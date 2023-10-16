from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from authentication.serializers import ChangePasswordSerializer, EmailConfirmationSerializer, LoginSerializer, RegisterSerializer, ResendOTPCodeSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from authentication.use_cases.change_password_use_case import ChangePasswordUsecase
from authentication.use_cases.email_confirmation_use_case import EmailConfirmationUseCase
from authentication.use_cases.login_use_case import LoginUseCase
from authentication.use_cases.register_user_use_case import RegisterUserUseCase
from authentication.use_cases.reset_password_request_use_case import ResetPasswordRequestUseCase
from authentication.use_cases.reset_password_use_case import ResetPasswordUsecase
from notification.signals import user_registered
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = LoginUseCase() \
            .execute(username=username, password=password)
        profil_type = user.type_profil

        account_serializer = None
        school_serializer = None
        student_serializer = None

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        data = {
            'refresh': str(refresh),
            'access': access_token,
            'user': user.id,
            'account': account_serializer.data if account_serializer else None,
            'parent_students': student_serializer.data if student_serializer else None,
            'profil_type': profil_type,
            'school': school_serializer.data if school_serializer else None
        }
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        profil_type = serializer.validated_data['profil_type']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        phone_number = serializer.validated_data['phone_number']
        country = serializer.validated_data['country']

        user_case = RegisterUserUseCase()

        user = user_case.execute(
            username=username,
            email=email,
            password=password,
            profil_type=profil_type,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            country=country
        )
        return Response(data=user.id, status=201)



class EmailConfirmationView(CreateAPIView):
    serializer_class = EmailConfirmationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        email = serializer.validated_data['email']

        user_id = EmailConfirmationUseCase.execute(code=code, email=email)

        return Response(status=200, data=user_id)



class ResendOTPCodeView(CreateAPIView):
    serializer_class = ResendOTPCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return
        user_registered.send(sender=self.__class__, user_id=user.id)
        return Response(status=status.HTTP_200_OK)


class ResetPasswordRequestView(CreateAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        form_data = serializer.validated_data
        email = form_data.get('email')
        ResetPasswordRequestUseCase().execute(email=email)
        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']
        code = validated_data['code']
        
        ResetPasswordUsecase.execute(email=email, password=password, code=code)
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        old_password = validated_data['old_password']
        new_password = validated_data['new_password']

        user = request.user

        ChangePasswordUsecase()\
            .execute(user=user, old_password=old_password, new_password=new_password)
        return Response(status=status.HTTP_200_OK)
