from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = (
        ('available', '可借'),
        ('borrowed', '已借出'),
        ('reserved', '已预约'),
        ('maintenance', '维护中'),
    )

    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    title = models.CharField(max_length=255, verbose_name='书名')
    author = models.CharField(max_length=255, verbose_name='作者')
    publisher = models.CharField(max_length=255, blank=True, verbose_name='出版社')
    publish_date = models.DateField(null=True, blank=True, verbose_name='出版日期')
    categories = models.ManyToManyField(Category, related_name='books', blank=True, verbose_name='分类')
    description = models.TextField(blank=True, verbose_name='简介')
    cover_image = models.URLField(blank=True, verbose_name='封面链接')
    total_copies = models.PositiveIntegerField(default=1, verbose_name='总册数')
    available_copies = models.PositiveIntegerField(default=1, verbose_name='可借册数')
    location = models.CharField(max_length=100, blank=True, verbose_name='馆藏位置')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.isbn})"
