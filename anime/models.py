from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.conf import settings
from .rename import PathAndRename


# Create your models here.


class Studio(models.Model):
    time_created = models.DateTimeField()


class Anime(models.Model):
    TYPES = [('TV', 'Television'), ('MOV', 'Movie'),
             ('MG', 'Manga'), ('LN', 'Light novel')]
    name = models.CharField(max_length=100)
    original_author = models.CharField(max_length=50)
    time_published = models.DateTimeField()
    number_of_episode = models.SmallIntegerField()
    type = models.CharField(max_length=15, choices=TYPES)
    is_finished = models.BooleanField(default=False)
    studio = models.ManyToManyField(Studio)
    is_airing = models.BooleanField(default=False)


class Channel(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    anime = models.OneToOneField(
        Anime, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(User, related_name='channels', blank=True)
    channel_cover = models.ImageField(
        upload_to=PathAndRename('channel_pics'), default='default_channel_cover.jpg')
    channel_avatar = models.ImageField(
        upload_to=PathAndRename('channel_pics'), default='default_channel_avatar.jpg')
    description = models.TextField(max_length=200)
    moderators = models.ManyToManyField(User, related_name='moderators', blank=True, null=True)
    timestamped = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, blank=True, primary_key=True)
    created_by_user = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('channel-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def remove_post(self, post):
        self.post_set.remove(post)
        post.delete()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    vote_object_id = models.PositiveIntegerField()
    vote_object = GenericForeignKey('vote_object_type', 'vote_object_id')
    value = models.IntegerField(default=0)

    @classmethod
    def create(cls, user, vote_object, vote_value):
        """
        Create a new vote object and return it.
        It will also update the ups/downs/score fields in the
        vote_object instance and save it.
        :param user: RedditUser instance
        :type user: RedditUser
        :param vote_object: Instance of the object the vote is cast on
        :type vote_object: Comment | Submission
        :param vote_value: Value of the vote
        :type vote_value: int
        :return: new Vote instance
        :rtype: Vote
        """

        # vote_object.author.profile.total_point += vote_value
        vote_object.author.profile.award_points(vote_value, vote_object.channel)

        vote = cls(user=user,
                   vote_object=vote_object,
                   value=vote_value)

        # the value for new vote will never be 0
        # that can happen only when removing up/down vote.
        vote_object.score += vote_value
        vote_object.point_today += vote_value
        vote_object.save()
        vote_object.author.save()

        return vote

    @classmethod
    def get_vote(cls, user, object):
        if isinstance(object, Post):
            return Vote.objects.get(user=user, post_model__id=object.id)
        elif isinstance(object, Comment):
            return Vote.objects.get(user=user, comment_model__id=object.id)

    def save(self, *args, **kwargs):
        self.vote_object.save()
        self.vote_object.author.save()
        self.vote_object.author.profile.save()
        return super().save(*args, **kwargs)

    def change_vote(self, new_vote_value):
        if self.value == -1 and new_vote_value == 1:  # down to up
            vote_diff = 2
            self.vote_object.score += 2
            self.vote_object.point_today += 2
            # self.vote_object.ups += 1
            # self.vote_object.downs -= 1
        elif self.value == 1 and new_vote_value == -1:  # up to down
            vote_diff = -2
            self.vote_object.score -= 2
            self.vote_object.point_today -= 2
            # self.vote_object.ups -= 1
            # self.vote_object.downs += 1
        elif self.value == 0 and new_vote_value == 1:  # canceled vote to up
            vote_diff = 1
            # self.vote_object.ups += 1
            self.vote_object.score += 1
            self.vote_object.point_today += 1
        elif self.value == 0 and new_vote_value == -1:  # canceled vote to down
            vote_diff = -1
            # self.vote_object.downs += 1
            self.vote_object.score -= 1
            self.vote_object.point_today -= 1
        else:
            return None

        if isinstance(self.vote_object, Post):

            self.vote_object.author.profile.award_points(vote_diff, self.vote_object.channel)
        else:
            self.vote_object.author.profile.total_point += vote_diff

        self.value = new_vote_value

        self.save()

        return vote_diff

    def cancel_vote(self):
        if self.value == 1:
            vote_diff = -1
            # self.vote_object.ups -= 1
            self.vote_object.score -= 1
            self.vote_object.point_today -= 1
        elif self.value == -1:
            vote_diff = 1
            # self.vote_object.downs -= 1
            self.vote_object.score += 1
            self.vote_object.point_today += 1
        else:
            return None

        self.vote_object.author.profile.award_points(vote_diff, self.vote_object.channel)
        self.value = 0
        self.save()

        return vote_diff


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    timestamped = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=PathAndRename('post_pics'), null=True, blank=True)
    vote = GenericRelation(Vote, related_query_name='post_model', content_type_field='vote_object_type',
                           object_id_field='vote_object_id')
    point_today = models.IntegerField(default=0)
    imagekit_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk, 'slug': self.channel.slug})


class Comment(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamped = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    content = models.TextField()
    vote = GenericRelation(Vote, related_query_name='comment_model', content_type_field='vote_object_type',
                           object_id_field='vote_object_id')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.original_post.pk, 'slug': self.original_post.channel.slug})

    def __str__(self):
        return 'Comment ' + self.content + ' cua ' + self.author.username


class SubComment(models.Model):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    timestamped = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamped']

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.parent_comment.original_post.pk,
                                              'slug': self.parent_comment.original_post.channel.slug})
