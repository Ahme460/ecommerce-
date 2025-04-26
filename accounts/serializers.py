from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
import random
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            phone=validated_data.get('phone', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        return user

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            user.set_password(data['new_password'])
            user.save()
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return data



class SendResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        reset_code = str(random.randint(100000, 999999))  # كود مكون من 6 أرقام

        user.reset_code = reset_code
        user.save()

        # هنا تبعت الإيميل بالكود
        self.send_email(user.email, reset_code)

    def send_email(self, email, code):
        from django.core.mail import send_mail
        send_mail(
            'Your Password Reset Code',
            f'Your reset code is: {code}',
            'no-reply@yourdomain.com',  # لازم تضبط الإيميل ده في settings
            [email],
            fail_silently=False,
        )
        


class CheckResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.CharField(max_length=6)


    def validate(self, data):
        email = data.get('email')
        reset_code = data.get('reset_code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if user.reset_code != reset_code:
            raise serializers.ValidationError("Invalid reset code.")

        data['user'] = user
        return data
