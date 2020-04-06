from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Sprint, Task

# User model might be swapped out for another and that the intent of
# our application is to make it as reusable as possible. We will need to use
# the get_user_model Django utility in board/serializers.py to create this
# switch in a clean way.
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', )


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', )


class TaskSerializer(serializers.ModelSerializer):
    # assigned is a foreign key to the User model.
    # This displays the user’s primary key, but
    # our URL structure expects to reference users
    # by their username.
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,
                                            required=False)

    # status_display is a read-only field to be serialized that
    # returns the value of the get_status_display method on the serializer.
    status_display = serializers.SerializerMethodField('get_status_display')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status',
                  'status_display', 'order', 'assigned', 'started', 'due',
                  'completed', )

    def get_status_display(self, obj):
        return obj.get_status_display()
