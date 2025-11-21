from django.urls import path
from library import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('books/<str:book_isbn>/', views.book, name='book'),
    path('books/<str:book_isbn>/addcomment/', views.addcomment, name='addcomment'),

    # authentication
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html'), name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    # profile
    path('profile/', views.profile, name='profile'),
    path('profile/profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile/password_edit/',
         auth_views.PasswordChangeView.as_view(template_name='password_edit.html', success_url=reverse_lazy('library:signout')),
         name='password_edit'),

    path('loans/', views.loans, name='loans'),
    path('comments/', views.comments, name='comments'),

    path('deletecomment/<int:comment_comno>/', views.deletecomment, name='deletecomment'),

    path('loan/<int:storage_stono>/', views.loan, name='loan'),
    path('return/<int:loan_loanno>/', views.return_book, name='return_book'),

    path('addbook/', views.addbook, name='addbook'),
    path('deletebook/<int:storage_stono>/', views.deletebook, name='deletebook'),

    path('loans/renew/<int:loan_loanno>/', views.renew, name='renew'),
    path('reserves/', views.reserves, name='reserves'),
    path('reserves/<int:storage_stono>/', views.reservebook, name='reservebook'),
    path('reserves/<int:reserve_reno>/confirm/', views.confirmreserve, name='confirmreserve'),
]
