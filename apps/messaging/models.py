from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Conversation(models.Model):
    """
    Model representing a conversation between two users
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Optional: Link to a product if conversation is about a specific product
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='conversations'
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        return f"Conversation: {self.subject}"

    def get_absolute_url(self):
        return reverse('messaging:conversation', kwargs={'pk': self.pk})

    def get_other_participant(self, user):
        """Get the other participant in the conversation"""
        return self.participants.exclude(pk=user.pk).first()

    def get_last_message(self):
        """Get the most recent message in this conversation"""
        return self.messages.order_by('-created_at').first()

    def mark_as_read_for_user(self, user):
        """Mark all messages in this conversation as read for a specific user"""
        unread_messages = self.messages.exclude(sender=user).filter(
            messageread__user=user,
            messageread__is_read=False
        )
        for message in unread_messages:
            message_read, created = MessageRead.objects.get_or_create(
                message=message,
                user=user,
                defaults={'is_read': True, 'read_at': timezone.now()}
            )
            if not created and not message_read.is_read:
                message_read.is_read = True
                message_read.read_at = timezone.now()
                message_read.save()

    def has_unread_messages_for_user(self, user):
        """Check if conversation has unread messages for a specific user"""
        return self.messages.exclude(sender=user).filter(
            models.Q(messageread__isnull=True) |
            models.Q(messageread__user=user, messageread__is_read=False)
        ).exists()


class Message(models.Model):
    """
    Model representing individual messages within a conversation
    """
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    # Optional: Attach files to messages
    attachment = models.FileField(
        upload_to='message_attachments/', 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"

    def is_read_by_user(self, user):
        """Check if message has been read by a specific user"""
        if self.sender == user:
            return True  # Sender always "read" their own message
        try:
            message_read = self.messageread_set.get(user=user)
            return message_read.is_read
        except MessageRead.DoesNotExist:
            return False

    def mark_as_read_by_user(self, user):
        """Mark message as read by a specific user"""
        if self.sender != user:  # Don't create read status for sender
            message_read, created = MessageRead.objects.get_or_create(
                message=self,
                user=user,
                defaults={'is_read': True, 'read_at': timezone.now()}
            )
            if not created and not message_read.is_read:
                message_read.is_read = True
                message_read.read_at = timezone.now()
                message_read.save()


class MessageRead(models.Model):
    """
    Model to track read status of messages for each user
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('message', 'user')
        verbose_name = 'Message Read Status'
        verbose_name_plural = 'Message Read Statuses'

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"{self.user.username} - {status}"

    def save(self, *args, **kwargs):
        if self.is_read and not self.read_at:
            self.read_at = timezone.now()
        super().save(*args, **kwargs)