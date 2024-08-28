from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    membership_number = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    last_login = models.DateTimeField(null=True, blank=True)  # 추가: last_login 필드
    is_superuser = models.BooleanField(default=False)  # 추가: is_superuser 필드
    is_staff = models.BooleanField(default=False)  # 추가: is_staff 필드
    is_active = models.BooleanField(default=True)  # 추가: is_active 필드
    date_joined = models.DateTimeField(auto_now_add=True)  # 추가: date_joined 필드


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class Pboard(models.Model):
    board_number = models.AutoField(primary_key=True)  # 자동으로 증가하는 게시판 번호
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 작성자와 연결된 외래 키
    title = models.CharField(max_length=200)  # 게시글 제목 필드
    content = models.TextField()  # 게시글 내용 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 자동으로 설정되는 작성 날짜
    view_c = models.IntegerField(default=0)  # 게시판 조회수를 저장하는 필드
    likes = models.IntegerField(default=0)  # 좋아요 수를 저장하는 필드
    CATEGORY_CHOICES = [
        ('recommendation', '추천'),
        ('chat', '사담'),
        ('review', '후기'),
        ('transport', '교통정보'),
        ('restaurant', '근처 맛집'),
        ('other', '기타'),
    ]

    FONT_SIZE_CHOICES = [
        ('16px', '16px'),
        ('18px', '18px'),
        ('20px', '20px'),
        ('22px', '22px'),
        ('24px', '24px'),
    ]

    FONT_FAMILY_CHOICES = [
        ('Hahmlet', 'Hahmlet'),
        ('Orbit', 'Orbit'),
        ('Dongle', 'Dongle'),
        ('Jua', 'Jua'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    font_size = models.CharField(max_length=10, choices=FONT_SIZE_CHOICES)
    font_family = models.CharField(max_length=20, choices=FONT_FAMILY_CHOICES)  # 모델에 font_family 필드 추가
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Pboard'  # 데이터베이스 테이블 이름 설정



class Pcomment(models.Model):
    board = models.ForeignKey(Pboard, on_delete=models.CASCADE, related_name='comments')  # 게시판과 댓글 연결
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 날짜

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Pcomment'  # 데이터베이스 테이블 이름 설정



class Pinformation(models.Model):
    id = models.AutoField(primary_key=True)  # 명시적으로 기본 키 필드 추가
    festival_name = models.CharField(max_length=50, db_column='축제명')
    venue = models.CharField(max_length=50, db_column='개최장소')
    start_date = models.DateField(db_column='축제시작일자')
    end_date = models.DateField(db_column='축제종료일자')
    content = models.TextField(db_column='축제내용')
    phone_number = models.CharField(max_length=50, db_column='전화번호')
    website = models.URLField(db_column='홈페이지주소')
    road_address = models.CharField(max_length=50, db_column='소재지도로명주소')
    jibun_address = models.CharField(max_length=50, db_column='소재지지번주소')
    latitude = models.FloatField(db_column='위도')
    longitude = models.FloatField(db_column='경도')
    provider = models.CharField(max_length=20, db_column='제공기관명')
    region = models.CharField(max_length=20, db_column='지역')

    class Meta:
        db_table = 'Pinformation'

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Pboard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

    class Meta:
        db_table = 'Like'
        unique_together = ('user', 'post')