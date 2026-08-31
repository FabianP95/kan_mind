"""Serializer layer for boards, tasks, comments, and member metadata."""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from board_app.models import Board, Task, TaskComment
from user_auth_app.models import UserProfile


class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="userprofile.email", read_only=True)
    fullname = serializers.CharField(source="userprofile.fullname", read_only=True)

    class Meta:

        model = UserProfile

        fields = ["id", "email", "fullname"]


class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="creator.id", read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
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
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="reviewer",
        allow_null=True,
        required=False,
    )
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="assignee",
        allow_null=True,
        required=False,
    )

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
            "assignee_id",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate(self, attrs):
        request = self.context.get("request")
        board = attrs.get("board")
        user = request.user
        assignee = attrs.get("assignee")
        reviewer = attrs.get("reviewer")

        if (
            self.instance is not None
            and board is not None
            and board != self.instance.board
        ):
            raise ValidationError("Dieser Task gehört nicht zu dem angegeben Board.")

        if not board:
            board = self.instance.board

        if not (board.creator == user or board.members.filter(id=user.id).exists()):
            raise PermissionDenied(
                "Du musst Mitglied dieses Boards sein oder der Creator, um eine Task zu erstellen."
            )

        if assignee and not (
             board.creator_id == assignee.id or board.members.filter(id=assignee.id).exists()
        ):
            raise ValidationError("Assignee nicht Mitglied des Boards.")

        if reviewer and not (
             board.creator_id == reviewer.id or board.members.filter(id=reviewer.id).exists()
        ):
            raise ValidationError("Reviewer nicht Mitglied des Boards.")

        return attrs


class TaskCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.userprofile.fullname", read_only=True)

    class Meta:
        model = TaskComment
        fields = [
            "id",
            "created_at",
            "author",
            "content",
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="creator.id", read_only=True)
    members = UserInfoSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        ]


class UpdateBoardSerializer(serializers.ModelSerializer):
    owner_data = UserInfoSerializer(source="creator", read_only=True, many=False)
    members_data = UserInfoSerializer(source="members", read_only=True, many=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_data",
            "members_data",
            "members",
        ]
