from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_details'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('search/', views.SearchResults.as_view(), name='search_results'),
    path('post/<slug:slug>/comment/', views.CommentCreate.as_view(), name='add_comment'),
    path('post/<slug:slug>/bookmark/', views.BookmarkToggle.as_view(), name='bookmark_toggle'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
