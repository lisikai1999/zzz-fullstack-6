from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('librarian', '图书管理员'),
        ('reader', '读者'),
    )
    MEMBERSHIP_CHOICES = (
        ('standard', '标准'),
        ('premium', '高级'),
        ('student', '学生'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='standard')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    id_card = models.CharField(max_length=30, blank=True)
    max_borrow_count = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
