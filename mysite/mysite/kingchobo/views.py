from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  # 로그인된 사용자만 접근 가능하도록 설정
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PboardForm, PcommentForm
from .models import Pboard , Pcomment # Pboard , Pcomment  모델 추가
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Pinformation
from django.http import JsonResponse
from .models import Pboard, Like
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from .models import Pboard
from django.db.models import Count, Value


def board_list(request):
    # 기본 정렬 방식: 최신순 정렬
    order_by = request.GET.get('order_by', 'created_at')

    if order_by == 'likes':
        # 좋아요 수 기준으로 정렬 (NULL 또는 0일 경우 0으로 처리)
        posts = Pboard.objects.all().select_related('user').annotate(
            likes_order=Coalesce('likes', Value(0)),
            comment_count=Count('comments')
        ).order_by('-likes_order', '-created_at')
    elif order_by == 'comments':
        # 댓글 수 기준으로 정렬
        posts = Pboard.objects.all().select_related('user').annotate(
            likes_order=Coalesce('likes', Value(0)),
            comment_count=Count('comments')
        ).order_by('-comment_count', '-created_at')
    else:
        # 최신순 정렬
        posts = Pboard.objects.all().select_related('user').annotate(
            likes_order=Coalesce('likes', Value(0)),
            comment_count=Count('comments')
        ).order_by('-created_at')

    # Paginator 설정 - 한 페이지에 10개 게시물
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'board.html', {'posts': page_obj, 'order_by': order_by})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('kingchobo:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('kingchobo:home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('kingchobo:home')


def home(request):
    return render(request, 'home.html')

@login_required
def board_write(request):
    if request.method == 'POST':
        form = PboardForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.font_size = form.cleaned_data['font_size']
            post.font_family = request.POST.get('font_family')  # 폼에서 선택된 값을 그대로 저장
            post.save()
            return redirect('kingchobo:board_list')
        else:
            print(form.errors)
    else:
        form = PboardForm()
    return render(request, 'board_write.html', {'form': form})




def show_board(request, board_number):
    post = get_object_or_404(Pboard, board_number=board_number)
    
    # view_c가 None인 경우 기본값 0으로 설정
    if post.view_c is None:
        post.view_c = 0
    
    post.view_c += 1  # 조회수 1 증가
    post.save()  # 변경사항 저장
    
    is_owner = request.user == post.user  # 현재 사용자가 게시글 작성자인지 확인
    return render(request, 'show_board.html', {'post': post, 'is_owner': is_owner})



@login_required
def edit_board(request, board_number):
    post = get_object_or_404(Pboard, board_number=board_number)
    if request.user != post.user:  # 현재 사용자가 게시글 작성자가 아닐 때
        return redirect('kingchobo:show_board', board_number=board_number)

    if request.method == 'POST':
        form = PboardForm(request.POST, instance=post)
        if form.is_valid():
            form.save()  # 게시글 수정
            return redirect('kingchobo:show_board', board_number=board_number)
    else:
        form = PboardForm(instance=post)
    return render(request, 'edit_board.html', {'form': form})


@login_required
def delete_board(request, board_number):
    post = get_object_or_404(Pboard, board_number=board_number)
    if request.user == post.user:  # 현재 사용자가 게시글 작성자인 경우
        post.delete()  # 게시글 삭제
    return redirect('kingchobo:board_list')

#댓글 추가, 수정, 삭제
@login_required
def add_comment(request, board_number):
    post = get_object_or_404(Pboard, board_number=board_number)
    if request.method == 'POST':
        form = PcommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = post
            comment.user = request.user
            comment.save()
            return redirect('kingchobo:show_board', board_number=board_number)
    else:
        form = PcommentForm()
    return render(request, 'show_board.html', {'post': post, 'form': form})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Pcomment, id=comment_id)
    if request.user != comment.user:
        return redirect('kingchobo:show_board', board_number=comment.board.board_number)

    if request.method == 'POST':
        form = PcommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('kingchobo:show_board', board_number=comment.board.board_number)
    else:
        form = PcommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Pcomment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('kingchobo:show_board', board_number=comment.board.board_number)

@login_required
def like_post(request, board_number):
    post = get_object_or_404(Pboard, board_number=board_number)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # 좋아요가 처음 눌렸을 때만 좋아요 수를 증가시킴
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})
    else:
        # 이미 좋아요를 누른 경우 오류 메시지를 반환
        return JsonResponse({'error': 'Already liked'}, status=400)


def search(request):
    query = request.GET.get('q', '')  # 검색어를 GET 파라미터에서 가져옵니다.
    page_number = request.GET.get('page', 1)  # 페이지 번호를 GET 파라미터에서 가져옵니다.

    # 축제명을 포함한 필터링
    festivals = Pinformation.objects.filter(festival_name__icontains=query)

    # 페이지네이션 설정 (한 페이지에 10개씩 출력)
    paginator = Paginator(festivals, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query
    })


def category_view(request):
    # Pinformation 모델에서 모든 고유 지역을 가져옵니다.
    regions = Pinformation.objects.values_list('region', flat=True).distinct()
    context = {
        'regions': regions
    }
    return render(request, 'category_view.html', context)

def region_festivals(request, region_name):
    # 선택된 지역의 축제 목록을 가져옵니다.
    festivals_list = Pinformation.objects.filter(region=region_name)
    
    # 페이지네이션 설정 (한 페이지에 10개씩 출력)
    paginator = Paginator(festivals_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'region': region_name,
        'page_obj': page_obj
    }
    return render(request, 'region_festivals.html', context)

def save_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        font_size = request.POST.get('font_size')
        font_family = request.POST.get('font_family')
        
        post = Pboard.objects.create(
            title=title,
            content=content,
            font_size=font_size,
            font_family=font_family,
            user=request.user
        )
        return redirect('kingchobo:board_list')

def search_spring(request):
    query = '꽃'
    festivals = Pinformation.objects.filter(festival_name__icontains=query)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(festivals, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query
    })

def search_summer(request):
    query = '물'
    festivals = Pinformation.objects.filter(festival_name__icontains=query)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(festivals, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query
    })

def search_fall(request):
    query = '단풍'
    festivals = Pinformation.objects.filter(festival_name__icontains=query)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(festivals, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query
    })

def search_winter(request):
    query = '눈'
    festivals = Pinformation.objects.filter(festival_name__icontains=query)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(festivals, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query
    })

