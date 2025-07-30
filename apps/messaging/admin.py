from django.contrib import admin
from .models import Conversation, Message, MessageRead


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['subject', 'get_participants', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['subject', 'participants__username', 'participants__email']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'created_at', 'is_deleted', 'get_content_preview']
    list_filter = ['is_deleted', 'created_at', 'sender']
    search_fields = ['content', 'sender__username', 'conversation__subject']
    readonly_fields = ['created_at']
    
    def get_content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = 'Content Preview'


@admin.register(MessageRead)
class MessageReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'read_at']
    list_filter = ['is_read', 'read_at']
    search_fields = ['user__username', 'message__content']
    readonly_fields = ['read_at']