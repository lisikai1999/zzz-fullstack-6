from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from apps.borrowing.models import BorrowingConfig


class Command(BaseCommand):
    help = '初始化系统数据（管理员账号和借阅配置）'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin', password='admin123', email='admin@library.com'
            )
            user.profile.role = 'admin'
            user.profile.save()
            self.stdout.write(self.style.SUCCESS('管理员账号已创建: admin / admin123'))
        else:
            self.stdout.write('管理员账号已存在')

        configs = [
            ('standard', 30, 2, 0.50, 5),
            ('premium', 60, 3, 0.30, 10),
            ('student', 14, 1, 0.20, 3),
        ]
        for membership, days, renew, fine, count in configs:
            BorrowingConfig.objects.get_or_create(
                membership_type=membership,
                defaults={
                    'max_borrow_days': days,
                    'max_renew_times': renew,
                    'fine_per_day': fine,
                    'max_borrow_count': count,
                }
            )
        self.stdout.write(self.style.SUCCESS('借阅配置已初始化'))
