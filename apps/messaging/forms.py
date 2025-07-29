from django import forms
from django.contrib.auth.models import User
from .models import Message, Conversation


class MessageForm(forms.ModelForm):
    """
    Form for creating new messages
    """
    class Meta:
        model = Message
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your message here...',
                'required': True
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.jpg,.jpeg,.png,.pdf,.doc,.docx'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Message'
        self.fields['attachment'].label = 'Attachment (optional)'
        self.fields['attachment'].help_text = 'Supported formats: JPG, PNG, PDF, DOC, DOCX (Max 5MB)'


class ConversationForm(forms.ModelForm):
    """
    Form for starting new conversations (refactored to match ProductForm style)
    """
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        empty_label="Select recipient...",
        help_text="Choose the user you want to message."
    )

    message_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your message here...',
            'required': True
        }),
        label='Message',
        help_text="Enter the content of your message."
    )

    class Meta:
        model = Conversation
        fields = ['subject', 'recipient']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject...',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Exclude current user from recipient choices
        if self.user:
            self.fields['recipient'].queryset = User.objects.exclude(pk=self.user.pk)
        self.fields['subject'].help_text = "Give your conversation a clear subject."

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject:
            raise forms.ValidationError("Subject is required.")
        if len(subject) < 3:
            raise forms.ValidationError("Subject must be at least 3 characters long.")
        return subject

    def clean_message_content(self):
        message = self.cleaned_data.get('message_content', '').strip()
        if not message:
            raise forms.ValidationError("Message content is required.")
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message

    def save(self, commit=True):
        conversation = super().save(commit=False)
        if commit:
            conversation.save()
            conversation.participants.add(self.user, self.cleaned_data['recipient'])
            # Create the first message
            Message.objects.create(
                conversation=conversation,
                sender=self.user,
                content=self.cleaned_data['message_content']
            )
        return conversation


class ContactSellerForm(forms.Form):
    """
    Form for contacting a seller about a specific product
    """
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter subject...',
            'required': True
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ask about this product...',
            'required': True
        })
    )

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        self.buyer = kwargs.pop('buyer', None)
        super().__init__(*args, **kwargs)
        
        if self.product:
            self.fields['subject'].initial = f"Question about: {self.product.title}"

    def save(self):
        """Create conversation and message"""
        if self.product and self.buyer:
            # Check if conversation already exists
            existing_conversation = Conversation.objects.filter(
                participants=self.buyer,
                product=self.product
            ).filter(participants=self.product.seller).first()

            if existing_conversation:
                conversation = existing_conversation
            else:
                conversation = Conversation.objects.create(
                    subject=self.cleaned_data['subject'],
                    product=self.product
                )
                conversation.participants.add(self.buyer, self.product.seller)

            # Create message
            Message.objects.create(
                conversation=conversation,
                sender=self.buyer,
                content=self.cleaned_data['message']
            )
            
            return conversation
        return None


class QuickReplyForm(forms.Form):
    """
    Simple form for quick replies in conversations
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Type your reply...',
            'required': True
        }),
        label=''
    )