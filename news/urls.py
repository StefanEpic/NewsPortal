from django.urls import path
from .views import PostsList, CategoryList, AuthorList, PostDetail, PostCreate, PostUpdate, PostDelete, PersonalView, \
    subscribe_author, subscribe_category, unsubscribe_author, unsubscribe_category, upgrade_me

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('personal/<int:pk>/', PersonalView.as_view(), name='personal'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('authors/<int:pk>', AuthorList.as_view(), name='author_list'),
    path('categories/<int:pk>/subscribe', subscribe_category, name='subscribe_category'),
    path('authors/<int:pk>/subscribe', subscribe_author, name='subscribe_author'),
    path('categories/<int:pk>/unsubscribe', unsubscribe_category, name='unsubscribe_category'),
    path('authors/<int:pk>/unsubscribe', unsubscribe_author, name='unsubscribe_author'),
]
