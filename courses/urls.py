from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from courses.views.details import CourseDetailPage, CategoryDetailPage, StudentRoomPage
from courses.views.authentication import SignUpView, LogInView, LogOutView, ActivateView
from courses.views.views import IndexPage, CoursesPage, ContactPage, AboutPage, BaseIndexPage, AddComment, \
    DeleteComment, GettingCourses

urlpatterns = [  # index
                  path('home/', IndexPage.as_view(), name='index'),
                  path('', CoursesPage.as_view(), name='course'),
                  path('', BaseIndexPage.as_view(), name='base'),
                  path('add_comment/<slug:slug>/', AddComment.as_view(), name='add_comment'),
                  path('del_comment/<slug:slug>/', DeleteComment.as_view(), name='del_comment_course'),
                  path('course/<slug:slug>/', CourseDetailPage.as_view(), name='c_detail'),
                  path('order-course/', GettingCourses.as_view(), name='ordering'),
                  path('category/<slug:slug>/', CategoryDetailPage.as_view(), name='cg_detail'),
                  path('student-page/', StudentRoomPage.as_view(), name='student_room'),
                  path('contact/', ContactPage.as_view(), name='contact'),
                  path('about/', AboutPage.as_view(), name='about'),

                  # auth
                  path('sign-in/', LogInView.as_view(), name='sign_in'),
                  path('log-out/', LogOutView.as_view(), name='log_out'),
                  path('sign-up/', SignUpView.as_view(), name='sign_up'),
                  path('activate/<str:token>/', ActivateView.as_view(), name='activate'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
