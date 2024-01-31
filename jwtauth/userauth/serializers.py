from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(style={'input_type': "password"}, read_only=True)

    class Meta:

        model = Profile
        fields = ['email', 'name', 'password', 'password1', 'is_seller', 'is_buyer']

        extra_kwargs = {
            'password': {'write_only': True},

        }

        def validate(self, attrs):
            password = attrs.get('password')
            password1 = attrs.get('password1')

            if password1 != password:
                raise serializers.ValidationError('Password & confirm password in not matching')

            return attrs

    def create(self, validate_data):
        return Profile.objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Profile
        fields = ['email', 'password']


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['email', 'name']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):

        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("New password and confirm new password must match.")
        return attrs


class FindAccountSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)


class OtpSerializer(serializers.Serializer):

    otp = serializers.IntegerField(required=True)


class ForgetPasswordSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):

        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("New password and confirm new password must match.")
        return attrs











