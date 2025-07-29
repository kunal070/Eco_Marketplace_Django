from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Max
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import Conversation, Message, MessageRead
from .forms import MessageForm, ConversationForm, ContactSellerForm, QuickReplyForm


class InboxView(LoginRequiredMixin, ListView):
    """
    User's message inbox showing all conversations
    """
    model = Conversation
    template_name = 'messaging/inbox.html'
    context_object_name = 'conversations'
    paginate_by = 20

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user,
            is_active=True
        ).annotate(
            message_count=Count('messages'),
            last_message_date=Max('messages__created_at')
        ).order_by('-last_message_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Messages'
        
        # Count unread conversations and add user info to conversations
        unread_count = 0
        for conversation in context['conversations']:
            conversation.has_unread = conversation.has_unread_messages_for_user(self.request.user)
            conversation.other_participant = conversation.get_other_participant(self.request.user)
            if conversation.has_unread:
                unread_count += 1
        
        context['unread_count'] = unread_count
        return context


class ConversationView(LoginRequiredMixin, DetailView):
    """
    Individual conversation view showing message thread
    """
    model = Conversation
    template_name = 'messaging/conversation.html'
    context_object_name = 'conversation'

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user,
            is_active=True
        ).prefetch_related('messages__sender', 'participants')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        
        # Mark conversation as read for current user
        conversation.mark_as_read_for_user(self.request.user)
        
        # Get messages with pagination
        messages_list = conversation.messages.filter(is_deleted=False)
        paginator = Paginator(messages_list, 50)
        page_number = self.request.GET.get('page')
        messages_page = paginator.get_page(page_number)
        
        context['messages'] = messages_page
        context['reply_form'] = QuickReplyForm()
        context['other_participant'] = conversation.get_other_participant(self.request.user)
        context['page_title'] = f'Conversation: {conversation.subject}'
        
        return context

    def post(self, request, *args, **kwargs):
        """Handle quick reply form submission"""
        conversation = self.get_object()
        form = QuickReplyForm(request.POST)
        
        if form.is_valid():
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=form.cleaned_data['content']
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('messaging:conversation', pk=conversation.pk)
        
        # If form is invalid, redisplay with errors
        context = self.get_context_data()
        context['reply_form'] = form
        return render(request, self.template_name, context)


class ComposeMessageView(LoginRequiredMixin, CreateView):
    """
    Create new conversation and send first message
    """
    model = Conversation
    form_class = ConversationForm
    template_name = 'messaging/compose.html'
    success_url = reverse_lazy('messaging:inbox')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Compose Message'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Message sent successfully!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactSellerView(FormView):
    """
    Contact seller about a specific product
    """
    template_name = 'messaging/contact_seller.html'
    form_class = ContactSellerForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get product from URL or session
        product_id = self.kwargs.get('product_id') or self.request.GET.get('product')
        if product_id:
            from apps.products.models import Product
            try:
                product = Product.objects.get(pk=product_id)
                kwargs['product'] = product
                kwargs['buyer'] = self.request.user
            except Product.DoesNotExist:
                pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id') or self.request.GET.get('product')
        if product_id:
            from apps.products.models import Product
            try:
                context['product'] = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                pass
        context['page_title'] = 'Contact Seller'
        return context

    def form_valid(self, form):
        conversation = form.save()
        if conversation:
            messages.success(self.request, 'Message sent to seller successfully!')
            return redirect('messaging:conversation', pk=conversation.pk)
        else:
            messages.error(self.request, 'Error sending message. Please try again.')
            return self.form_invalid(form)
    
    def get_success_url(self):
        # This won't be used since we redirect in form_valid, but FormView requires it
        return reverse_lazy('messaging:inbox')


@login_required
@require_POST
def mark_as_read(request):
    """
    AJAX endpoint to mark messages as read
    """
    conversation_id = request.POST.get('conversation_id')
    message_id = request.POST.get('message_id')
    
    try:
        if conversation_id:
            conversation = get_object_or_404(
                Conversation, 
                pk=conversation_id, 
                participants=request.user
            )
            conversation.mark_as_read_for_user(request.user)
            return JsonResponse({'status': 'success', 'message': 'Conversation marked as read'})
        
        elif message_id:
            message = get_object_or_404(
                Message, 
                pk=message_id, 
                conversation__participants=request.user
            )
            message.mark_as_read_by_user(request.user)
            return JsonResponse({'status': 'success', 'message': 'Message marked as read'})
        
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def delete_conversation(request, pk):
    """
    Soft delete a conversation for the current user
    """
    conversation = get_object_or_404(
        Conversation, 
        pk=pk, 
        participants=request.user
    )
    
    if request.method == 'POST':
        # Remove user from conversation participants
        conversation.participants.remove(request.user)
        
        # If no participants left, mark conversation as inactive
        if conversation.participants.count() == 0:
            conversation.is_active = False
            conversation.save()
        
        messages.success(request, 'Conversation deleted successfully!')
        return redirect('messaging:inbox')
    
    return render(request, 'messaging/delete_conversation.html', {
        'conversation': conversation,
        'page_title': 'Delete Conversation'
    })


@login_required
def search_conversations(request):
    """
    Search conversations by subject or participant name
    """
    query = request.GET.get('q', '').strip()
    conversations = Conversation.objects.filter(participants=request.user, is_active=True)
    
    if query:
        conversations = conversations.filter(
            Q(subject__icontains=query) |
            Q(participants__username__icontains=query) |
            Q(participants__first_name__icontains=query) |
            Q(participants__last_name__icontains=query)
        ).distinct()
    
    paginator = Paginator(conversations.order_by('-updated_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Add user info to conversations
    for conversation in page_obj:
        conversation.has_unread = conversation.has_unread_messages_for_user(request.user)
        conversation.other_participant = conversation.get_other_participant(request.user)
    
    return render(request, 'messaging/search_results.html', {
        'conversations': page_obj,
        'query': query,
        'page_title': f'Search Results: {query}' if query else 'Search Conversations'
    })