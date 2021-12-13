import re
from django.shortcuts import render
from django.views.generic import (
    CreateView, DetailView,ListView,UpdateView,DeleteView
)
from .models import Post,Channel,Comment, Vote, SubComment
from users.models import Point
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ChannelUpdateForm
from django.urls import reverse
from notifications import notify
# Create your views here.
def home(request):
  return render(request,'anime/newsfeed.html')

class CreatePostView(LoginRequiredMixin,CreateView):
  model = Post
  fields = ['title', 'content','image']
  template_name = 'anime/test.html'
  def form_valid(self,form):
    form.instance.channel = Channel.objects.get(slug=self.kwargs['slug'])
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostDetailView(DetailView):
  model = Post
  template_name = 'anime/post_detail.html'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    comments = self.get_object().comment_set.all().order_by('-timestamped')
    context['comments'] = comments
    try:
      context['vote_value'] = Vote.get_vote(user=self.request.user,object=self.get_object()).value
    except (Vote.DoesNotExist, TypeError) as e:
      context['vote_value'] = 0
    return context

@login_required
def comment_submit(request,**kwargs):
  try:
    original_post = Post.objects.get(id=kwargs['pk'])
  except (Post.DoesNotExist):
    return HttpResponseBadRequest()
  content = request.POST.get('content')
  if not content:
    return HttpResponseBadRequest()
  author = request.user
  comment = Comment.objects.create(author=author,original_post=original_post,content=content)
  comment.save()
  return JsonResponse({'new_comment_id':comment.id})

class ChannelDetailView(ListView):
  model = Post
  template_name = 'anime/channel_detail.html'
  paginate_by = 20
  context_object_name = 'channel_posts'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user= self.request.user
    try:
      channel = Channel.objects.get(slug=self.kwargs['slug'])
    except:
      return HttpResponseBadRequest()
    context['top_members_point'] = Point.objects.filter(channel=channel).order_by('-point')[:5]
    context['isMember'] = channel.members.filter(id=user.id).exists()
    context['object']= channel
    return context
  
  def get_queryset(self):
    user= self.request.user
    try:
      channel = Channel.objects.get(slug=self.kwargs['slug'])
      posts = Post.objects.filter(channel=channel).order_by('-point_today','-timestamped').all()
    except:
      return HttpResponseBadRequest()
    queryset=[]
    for post in posts:
      print(post.point_today)
      try:
        vote_value = Vote.get_vote(user = user,object = post).value  
      except (Vote.DoesNotExist, TypeError) as e:
        vote_value = 0
      queryset.append([post,vote_value])
    return queryset
  
@login_required
def read_all_notification(request):
  if request.method == 'POST':
    request.user.notifications.mark_all_as_read()
    return HttpResponse('<h1>successful</h1>')

class ChannelAutoCompleteView(autocomplete.Select2QuerySetView):
  def get_queryset(self):
      if not self.request.user.is_authenticated:
          return Channel.objects.none()
      qs = Channel.objects.all()
      print(self)
      if self.q:
          qs = qs.filter(name__icontains=self.q)

      return qs
  def get_results(self, context):
    """Return data for the 'results' key of the response."""
    return [
        {
            'id': self.get_result_value(result),
            'text': self.get_result_label(result),
            'selected_text': self.get_selected_result_label(result),
            'channel_avatar':result.channel_avatar.url,
            'channel_cover':result.channel_cover.url,
            'name':result.name,
            'member_count': result.members.count()
        } for result in context['object_list']
    ]
    
class SearchChannelView(ListView):
  model = Channel
  template_name = 'anime/group_list.html'  # <app>/<model>_<viewtype>.html
  context_object_name = 'channels'
  # paginate_by = 5
  
  def get_queryset(self):
    query = self.request.GET.get('q')
    return Channel.objects.filter(name__icontains=query)
  
@login_required
def vote(request):
    # The type of object we're voting on, can be 'submission' or 'comment'
    vote_object_type = request.POST.get('what', None)

    # The ID of that object as it's stored in the database, positive int
    vote_object_id = request.POST.get('what_id', None)

    # The value of the vote we're writing to that object, -1 or 1
    # Passing the same value twice will cancel the vote i.e. set it to 0
    new_vote_value = request.POST.get('vote_value', None)
    # By how much we'll change the score, used to modify score on the fly
    # client side by the javascript instead of waiting for a refresh.
    vote_diff = 0

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        user = request.user

    try:  # If the vote value isn't an integer that's equal to -1 or 1
        # the request is bad and we can not continue.
        new_vote_value = int(new_vote_value)

        if new_vote_value not in [-1, 1]:
            raise ValueError("Wrong value for the vote!")

    except (ValueError, TypeError):
        return HttpResponseBadRequest()

    # if one of the objects is None, 0 or some other bool(value) == False value
    # or if the object type isn't 'comment' or 'submission' it's a bad request
    if not all([vote_object_type, vote_object_id, new_vote_value]) or \
            vote_object_type not in ['comment', 'post']:
        return HttpResponseBadRequest()

    # Try and get the actual object we're voting on.
    try:
        if vote_object_type == "comment":
            vote_object = Comment.objects.get(id=vote_object_id)
            # content_type = ContentType.objects.get(model='comment')
        elif vote_object_type == "post":
            vote_object = Post.objects.get(id=vote_object_id)
            # content_type = ContentType.objects.get(model='post')
        else:
            return HttpResponseBadRequest()  # should never happen

    except (Comment.DoesNotExist, Post.DoesNotExist):
        return HttpResponseBadRequest()

    # Try and get the existing vote for this object, if it exists.
    try:
        vote = Vote.get_vote(user=user,object=vote_object)
    except Vote.DoesNotExist:
        # Create a new vote and that's it.
        vote = Vote.create(user=user,
                           vote_object=vote_object,
                           vote_value=new_vote_value)
        vote.save()
        vote_diff = new_vote_value
        return JsonResponse({'error'   : None,
                             'voteDiff': vote_diff})

    # User already voted on this item, this means the vote is either
    # being canceled (same value) or changed (different new_vote_value)
    if vote.value == new_vote_value:
        # canceling vote
        vote_diff = vote.cancel_vote()
        if not vote_diff:
            return HttpResponseBadRequest(
                'Something went wrong while canceling the vote')
    else:
        # changing vote
        vote_diff = vote.change_vote(new_vote_value)
        if not vote_diff:
            return HttpResponseBadRequest(
                'Wrong values for old/new vote combination')

    return JsonResponse({'error'   : None,
                         'voteDiff': vote_diff})
@login_required
def join_channel(request,**kwargs):
  user = request.user
  slug = kwargs['slug']
  channel = Channel.objects.get(slug=slug)
  if channel.members.filter(id=user.id).exists():
    return JsonResponse({'message':'success'})
  else:
    channel = Channel.objects.get(slug=slug)
    channel.members.add(user)
  return JsonResponse({'message':'error'})

class CreateChannelView(LoginRequiredMixin,CreateView):
  model = Channel
  template_name = 'anime/channel_create.html'
  fields = ['name', 'description']
  def form_valid(self,form):
    form.instance.creator = self.request.user
    return super().form_valid(form)



class HomePage(ListView):
  model = Post
  template_name = 'anime/newsfeed.html'  
  context_object_name = 'posts'
  paginate_by = 20 
  def get_queryset(self):
    user = self.request.user
    queryset = []
    if user.is_authenticated:
      posts_set = Post.objects.all().order_by('-timestamped')
      for post in posts_set:
        try:
          vote_value = Vote.get_vote(user = user,object = post).value
        except Vote.DoesNotExist:
          vote_value = 0
        queryset.append([post,vote_value])
    else:
      posts_set = Post.objects.all().order_by('-timestamped')
      for post in posts_set:
        vote_value = 0
        queryset.append([post,vote_value])
    return queryset
    
def badges(request):
  return render(request, 'anime/badges.html')
  
class ChannelUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Channel
    template_name = 'anime/update_channel.html'
    form_class = ChannelUpdateForm
    def form_valid(self,form):
      form.instance.creator = self.request.user
      return super().form_valid(form)
    
    def test_func(self):
        channel = self.get_object()
        return self.request.user == channel.creator
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    template_name = 'anime/post_update.html'
    fields = ['title','content']
    def form_valid(self,form):
      form.instance.author = self.request.user
      return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    def get_success_url(self):
      print('vao duoc day')
      return reverse('profile',kwargs={'pk':self.get_object().author.pk})
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def subcomment_submit(request,**kwargs):
  user = request.user
  content = request.POST.get('content')
  parent_comment = Comment.objects.get(id=int(request.POST.get('parent_comment_id')))
  if not content:
    return HttpResponseBadRequest()
  sub_comment = SubComment.objects.create(author=user,parent_comment=parent_comment,content=content)
  sub_comment.save()
  return JsonResponse({'content':content})


