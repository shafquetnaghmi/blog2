from django.urls import path
from . import views
app_name='app1'

urlpatterns = [
    path("",views.list_view,name="post_list"),
    path('tag/<slug:tag_slug>/',views.list_view,name="post_list_by_tag"),
    #path("",views.PostListView.as_view(),name="post_list"),
    path("<str:post>/<int:id>/",views.post_detail,name="post_details"),    
    path('<int:post_id>/share/',views.post_share,name="post_share"),
    path('<int:post_id>/comment/',views.post_comment,name="post_comment"),
    path("search/",views.post_search,name="search"),
    path('write/',views.CreateBlogView,name="write")

]
