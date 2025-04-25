# rag_system/serializers.py
from rest_framework import serializers
from .models import Conversation, Message, Document, Entity


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "role", "content", "metadata", "created_at"]


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ["id", "entity_type", "name", "mentions", "created_at"]


class ConversationListSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at", "updated_at", "message_count"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    entities = EntitySerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at", "updated_at", "messages", "entities"]


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    conversation_id = serializers.UUIDField(required=False, allow_null=True)
    language = serializers.CharField(required=False, default="en")


class QueryResponseSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField()
    message_id = serializers.UUIDField()
    answer = serializers.CharField()
    sources = serializers.ListField(child=serializers.DictField(), required=False)
    timing = serializers.DictField(required=False)


class RebuildIndexResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    documents_added = serializers.IntegerField()
    message = serializers.CharField()
