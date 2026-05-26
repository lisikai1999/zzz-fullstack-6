from django.db import models
from django.contrib.auth.models import User
from apps.books.models import Book


class BorrowingConfig(models.Model):
    membership_type = models.CharField(max_length=20, unique=True, verbose_name='会员类型')
    max_borrow_days = models.IntegerField(default=30, verbose_name='最大借阅天数')
    max_renew_times = models.IntegerField(default=2, verbose_name='最大续借次数')
    fine_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0.50, verbose_name='每日罚款')
    max_borrow_count = models.IntegerField(default=5, verbose_name='最大借阅数量')

    class Meta:
        verbose_name = '借阅配置'
        verbose_name_plural = '借阅配置'

    def __str__(self):
        return f"{self.membership_type} - {self.max_borrow_days}天"


class BorrowingRecord(models.Model):
    STATUS_CHOICES = (
        ('borrowed', '借出'),
        ('returned', '已还'),
        ('overdue', '逾期'),
        ('lost', '丢失'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowing_records', verbose_name='借阅人')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowing_records', verbose_name='图书')
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='借阅日期')
    due_date = models.DateTimeField(verbose_name='应还日期')
    return_date = models.DateTimeField(null=True, blank=True, verbose_name='归还日期')
    renew_count = models.IntegerField(default=0, verbose_name='续借次数')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed', verbose_name='状态')
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name='罚款金额')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"
