from rest_framework import serializers
from ...models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    this is a serializer to show a list of task
    """

    user = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "is_complete",
            "absolute_url",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):

        request = self.context.get("request")
        validated_data["user"] = request.user.profile
        return super().create(validated_data)

    def get_absolute_url(self, obj):

        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        """
        this is a function for overwrite fields to show
        """

        request = self.context.get("request")
        data = super().to_representation(instance)

        if request.parser_context.get("kwargs").get("pk"):

            data.pop("absolute_url", None)

        return data
