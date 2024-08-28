# kingchobo/urls.py
from django.urls import path
from . import views

app_name = 'kingchobo'  # app_name 설정

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),  # home URL 패턴 정의
    path('board/', views.board_list, name='board_list'),  # 게시판 목록 페이지 URL 패턴 추가
    path('board/write/', views.board_write, name='board_write'),  # 게시글 작성 페이지 URL 패턴 추가
    path('board/<int:board_number>/', views.show_board, name='show_board'),  # 게시글 상세 페이지
    path('board/<int:board_number>/edit/', views.edit_board, name='edit_board'),  # 게시글 수정 페이지
    path('board/<int:board_number>/delete/', views.delete_board, name='delete_board'),  # 게시글 삭제
    path('board/<int:board_number>/comment/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('logout/', views.logout_view, name='logout'),  # 로그아웃 URL 패턴 추가
    path('search/', views.search, name='search'),
    path('category/', views.category_view, name='category_view'),
    path('category/<str:region_name>/', views.region_festivals, name='region_festivals'),
    path('post/<int:board_number>/like/', views.like_post, name='like_post'),
    path('save-post/', views.save_post, name='save_post'),
    path('search/spring/', views.search_spring, name='search_spring'),
    path('search/summer/', views.search_summer, name='search_summer'),
    path('search/fall/', views.search_fall, name='search_fall'),
    path('search/winter/', views.search_winter, name='search_winter'),
]