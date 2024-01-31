import pytz
from django.shortcuts import render
from .serializers import (ProfileSerializer, LoginSerializer,
                          ChangePasswordSerializer, FindAccountSerializer,
                          OtpSerializer, ForgetPasswordSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (HTTP_408_REQUEST_TIMEOUT, HTTP_404_NOT_FOUND,
                                   HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED)
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Otp
from datetime import datetime, timedelta
from .permissions import IsSeller, IsBuyer
import random


# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Register(APIView):

    def post(self, request):

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': "user added"},status=HTTP_201_CREATED)
        else:
            return Response({'msg': 'something went wrong'}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({"msg": "User login successfully", "token": token})
            else:
                return Response({"msg": "Wrong username and password"}, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({"msg": "something Wrong"}, status=HTTP_400_BAD_REQUEST)


class SellerView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        query_set = Profile.objects.all()
        serializer = ProfileSerializer(query_set, many=True)
        return Response(serializer.data)


class BuyerView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        query_set = Profile.objects.all()
        serializer = ProfileSerializer(query_set, many=True)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            profile = Profile.objects.get(pk=request.user.id)
            if profile.check_password(old_password):
                profile.set_password(new_password)
                profile.save()
                return Response({'msg': "Password changed"})
            else:
                return Response({'msg': "Wrong old password"}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class FindAccount(APIView):

    def post(self, request):

        serializer = FindAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            try:
                profile = Profile.objects.get(email=serializer.data.get('email'))
            except Exception as e:
                return Response({"error": "No Account Found"}, status=HTTP_404_NOT_FOUND)

            if profile:
                otp = str(random.random()).split('.')[1][0:6]
                try:
                    otp_obj = Otp(otp_data=otp, user=profile)
                    otp_obj.save()
                except Exception as e:
                    return Response({'msg': str(e)})

                return Response({"Success": True, "msg": "OTP has been sended to your account", "user": profile.id})
        else:
            return Response({"error": serializer.errors},status=HTTP_400_BAD_REQUEST)


class OtpView(APIView):

    def post(self, request):

        serializer = OtpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            otp = serializer.data.get('otp')
            try:
                otp_object = Otp.objects.get(otp_data=otp)
            except Exception as e:
                return Response({"msg": "Invalid OTP"},status=HTTP_404_NOT_FOUND)

            # return Response({"msg": "OTP Expired", 'success': False})
            if datetime.now(pytz.utc) < otp_object.created_at + timedelta(minutes=15):
                if otp == otp_object.otp_data:

                    return Response({"msg": "Verified",  "success": True})
                else:
                    return Response({'msg': "Wrong Otp", "success": False}, status=HTTP_400_BAD_REQUEST)
            else:
                otp_object.delete()
                return Response({"msg": "expired", "success": False}, status=HTTP_408_REQUEST_TIMEOUT)


class ForgetPasswordView(APIView):

    def post(self, request):

        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.data.get('new_password')
            otp = serializer.data.get('otp')
            try:
                otp_obj = Otp.objects.get(otp_data=otp)
            except Exception as e:
                return Response({'msg': str(e)})
            otp_obj.user.set_password(new_password)
            otp_obj.user.save()
            return Response({'msg': "Password changed"})
        else:
            return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)
