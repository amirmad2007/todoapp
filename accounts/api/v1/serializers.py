from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from ...models import MyUser as User, Profile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id

        return validated_data


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, attrs):

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("passwords does not match.")

        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"passwords": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError("this user does not exist.")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):

        user = self.context["request"].user

        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError("old password is not correct")

        if user.check_password(attrs.get("password")):
            raise serializers.ValidationError("this password is your old password.")

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("passwords does not match.")

        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"passwords": list(e.messages)})

        user.set_password(attrs.get("password"))
        user.save()
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email", read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):

        user = self.context.get("user")
        if user.check_password(attrs.get("password")):
            raise serializers.ValidationError(
                {"details": "this password is your old password."}
            )

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("passwords does not match.")

        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"passwords": list(e.messages)})

        user.set_password(attrs.get("password"))
        user.save()
        return attrs
