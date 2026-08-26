from rest_framework import serializers
from board_app.models import Board, Task, TaskComment
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = UserProfile
        
        fields = [
            "id",
            "email",
            "fullname"
        ]

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="creator.id", read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
            "members",
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status=Task.Status.TO_DO).count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority=Task.Priority.HIGH).count()


class TaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    reviewer = UserInfoSerializer(read_only=True, allow_null=True)
    assignee = UserInfoSerializer(read_only=True, allow_null=True)
    class Meta:
        model = Task
        
        fields = [
                    "id",
                    "board",
                    "title",
                    "description",
                    "status",
                    "priority",
                    "assignee",
                    "reviewer",
                    "due_date",
                    "comments_count",
                ]
        
    def get_comments_count(self, obj):
                return obj.comments.count()



class TaskCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskComment
    


