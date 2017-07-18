# from __future__ import unicode_literals

# from django.conf.urls import patterns, include, url
# from django.conf.urls.i18n import i18n_patterns
# from django.contrib import admin
# from django.core.urlresolvers import reverse_lazy

# from mezzanine.core.views import direct_to_template
# from mezzanine.conf import settings
# # from tutors.views import index
# import swingtime
# from tutors import views

# admin.autodiscover()

# # Add the urlpatterns for any custom Django applications here.
# # You can also change the ``home`` view to add your own functionality
# # to the project's homepage.

# urlpatterns = i18n_patterns("",
#     # Change the admin prefix here to use an alternate URL for the
#     # admin interface, which would be marginally more secure.
#     ("^superadmin/", include(admin.site.urls)),
# )

# if settings.USE_MODELTRANSLATION:
#     urlpatterns += patterns('',
#         url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
#     )

# urlpatterns += patterns('',
#     # We don't want to presume how your homepage works, so here are a
#     # few patterns you can use to set it up.

#     # HOMEPAGE AS STATIC TEMPLATE
#     # ---------------------------
#     # This pattern simply loads the index.html template. It isn't
#     # commented out like the others, so it's the default. You only need
#     # one homepage pattern, so if you use a different one, comment this
#     # one out.

#     # url("^$", direct_to_template, {"template": "index.html"}, name="home"),

#     url("^$", views.CoursesListView.as_view(), name="home"),
#     url("^learning/?$", views.index, name="learning"),
#     url("^course/(?P<pk>\d+)$", views.CoursesDetailView.as_view(), name="courses-detail"),
#     url("^about-us/?$", views.about_us, name="about_us"),

#     # ajax
#     url(r'^ajax_calls/classdata/', views.get_class_data),
#     url(r'^ajax/apply/check', views.course_apply_check),
#     url(r'^ajax/application', views.application_process),
#     url(r'^ajax/withdraw_course', views.withdraw_course),
#     url(r'^ajax/recommend_course', views.recommend_course),

#     # user register
#     url("^register/?$", views.user_register, name="register"),
#     url("^register/teacher/?$", views.teacher_register_form, name="teacher-user-register"),
#     url("^register/student/?$", views.student_register_form, name="student-register"),

#     # user login/logout
#     url("^login/?$", views.user_login, name="user-login"),
#     url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="user_logout"),
#     url("^social/login/group/(?P<string>[\w\-]+)/?$", views.social_login_group, name="social-login-group"),
#     url("^social_login/?$", views.social_login, name="social-user-login"),
#     url("^social_logout/?$", views.social_logout, name="social-user-logout"),

#     # add/edit/delete course
#     url("^add/course/?$", views.create_course, name="add-course"),
#     url("^course/edit/(?P<id>\d+)/?$", views.create_course, name="edit-course"),
#     # url("^course/delete/(?P<pk>\d+)/?$", views.Course_DeleteView.as_view(), name="delete-course"),
#     url("^course/delete/(?P<id>\d+)/?$", views.delete_course, name="delete-course"),
#     # django social login
#     url('', include('social.apps.django_app.urls', namespace='social')),

#     # teacher-dashboard
#     url("^teacher/home/?$", views.teacher_dashboard, name="teacher_dashboard"),
#     url("^teacher/profile/edit/(?P<teacher_id>\d+)/?$", views.teacher_register_form, name="teacher-profile-edit"),
#     url("^teacher/password/edit/(?P<user_id>\d+)/?$", views.user_edit_password, name="teacher-password-edit"),
#     url("^teacher/course-detail/(?P<course_id>\d+)/?$", views.course_details, name="course-details"),
#     url("^teacher/pending_applications/?$", views.pending_applications, name="teacher_pending_applications"),

#     # password reset
#     url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect': reverse_lazy('user_password_reset_done'), 'template_name': 'tutors/user_login/password_reset/password_reset_form.html', 'email_template_name': 'tutors/user_login/password_reset/password_reset_email.html'},
#         name="user_password_reset"),
#     url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'tutors/user_login/password_reset/password_reset_done.html'}, name="user_password_reset_done"),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': reverse_lazy('user_password_reset_complete'), 'template_name': 'tutors/user_login/password_reset/password_reset_confirm.html'}, name="user_password_confirm"),
#     url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'tutors/user_login/password_reset/password_reset_complete.html'}, name="user_password_reset_complete"),

#     # user account activation
#     url(r'^user/resendactivation/(?P<user_id>\d+)', views.resend_activation, name="resend-activation"),
#     url(r'^user/activation_sent', views.activation_sent, name="activation-sent"),
#     url(r'^user/confirm/(?P<activation_key>\w+)/', views.user_activated_confirm, name="user_activated_confirm"),

#     # search
#     url(r'^tutor/search/?$', views.SearchList.as_view(), name="search-list"),

#     # student_dashboard
#     url("^student/home/?$", views.student_dashboard, name='student_dashboard'),
#     url("^student/profile/edit/(?P<student_id>\d+)/?$", views.student_register_form, name="student-profile-edit"),
#     url("^student/password/edit(?P<user_id>\d+)/?$", views.user_edit_password, name="student-password-edit"),
#     url("^student/pending_applications/?$", views.pending_applications, name="student_pending_applications"),
#     url("^student/course-detail/(?P<course_id>\d+)/?$", views.course_details, name="student-course-details"),

#     #notification
#     url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),
#     #course-application
#     url("course/application/(?P<id>\d+)/?$", views.course_application, name="course-application"),

#     #calendar swingtime
#     url(r'^swingtime/', include('swingtime.urls')),
#     url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/monthly/calendar/(?P<year>\d+)/(?P<month>\d+)/?$', views.course_month_view, name='monthly-calendar'),
#     url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/daily/calendar/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/?$', views.day_view, name='daily-calendar'),
#     url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/add/?$', views.add_course_schedule, name='add-course-schedule'),
#     url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/view/(?P<event_id>\d+)/$',views.schedule_view, name='course-schedule_view'),
#     url(r'teacher/course-details/schedule/edit/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$', views.occurrence_view, name='swingtime-occurrence'),

#     url("^course/teacher/profile/(?P<pk>\d+)/?$", views.teacher_view, name="teacher-view"),
#     url("^course/student/profile/(?P<pk>\d+)/?$", views.student_view, name="student-view"),

#     # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
#     # ---------------------------------------------
#     # This pattern gives us a normal ``Page`` object, so that your
#     # homepage can be managed via the page tree in the admin. If you
#     # use this pattern, you'll need to create a page in the page tree,
#     # and specify its URL (in the Meta Data section) as "/", which
#     # is the value used below in the ``{"slug": "/"}`` part.
#     # Also note that the normal rule of adding a custom
#     # template per page with the template name using the page's slug
#     # doesn't apply here, since we can't have a template called
#     # "/.html" - so for this case, the template "pages/index.html"
#     # should be used if you want to customize the homepage's template.

#     # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

#     # HOMEPAGE FOR A BLOG-ONLY SITE
#     # -----------------------------
#     # This pattern points the homepage to the blog post listing page,
#     # and is useful for sites that are primarily blogs. If you use this
#     # pattern, you'll also need to set BLOG_SLUG = "" in your
#     # ``settings.py`` module, and delete the blog page object from the
#     # page tree in the admin if it was installed.

#     # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

#     # MEZZANINE'S URLS
#     # ----------------
#     # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
#     # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
#     # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
#     # WILL NEVER BE MATCHED!

#     # If you'd like more granular control over the patterns in
#     # ``mezzanine.urls``, go right ahead and take the parts you want
#     # from it, and use them directly below instead of using
#     # ``mezzanine.urls``.
#     ("^", include("mezzanine.urls")),

#     # MOUNTING MEZZANINE UNDER A PREFIX
#     # ---------------------------------
#     # You can also mount all of Mezzanine's urlpatterns under a
#     # URL prefix if desired. When doing this, you need to define the
#     # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
#     # SITE_PREFIX = "my/site/prefix"
#     # For convenience, and to avoid repeating the prefix, use the
#     # commented out pattern below (commenting out the one above of course)
#     # which will make use of the ``SITE_PREFIX`` setting. Make sure to
#     # add the import ``from django.conf import settings`` to the top
#     # of this file as well.
#     # Note that for any of the various homepage patterns above, you'll
#     # need to use the ``SITE_PREFIX`` setting as well.

#     # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

# )

# # Adds ``STATIC_URL`` to the context of error pages, so that error
# # pages can use JS, CSS and images.
# handler404 = "mezzanine.core.views.page_not_found"
# handler500 = "mezzanine.core.views.server_error"


from django.conf.urls import url,include
from django.contrib import admin
# from tutors.views import index
import swingtime
from tutors import views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url("^$", views.CoursesListView.as_view(), name="home"),
    url("^learning/?$", views.index, name="learning"),
    url("^course/(?P<pk>\d+)$", views.CoursesDetailView.as_view(), name="courses-detail"),
    url("^about-us/?$", views.about_us, name="about_us"),

    # ajax
    url(r'^ajax_calls/classdata/', views.get_class_data),
    url(r'^ajax/apply/check', views.course_apply_check),
    url(r'^ajax/application', views.application_process),
    url(r'^ajax/withdraw_course', views.withdraw_course),
    url(r'^ajax/recommend_course', views.recommend_course),

    # user register
    url("^register/?$", views.user_register, name="register"),
    url("^register/teacher/?$", views.teacher_register_form, name="teacher-user-register"),
    url("^register/student/?$", views.student_register_form, name="student-register"),

    # user login/logout
    url("^login/?$", views.user_login, name="user-login"),
    url("^logout/?$", views.user_logout, name="user_logout"),
    #url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="user_logout"),
    url("^social/login/group/(?P<string>[\w\-]+)/?$", views.social_login_group, name="social-login-group"),
    url("^social_login/?$", views.social_login, name="social-user-login"),
    url("^social_logout/?$", views.social_logout, name="social-user-logout"),

    # add/edit/delete course
    url("^add/course/?$", views.create_course, name="add-course"),
    url("^course/edit/(?P<id>\d+)/?$", views.create_course, name="edit-course"),
    # url("^course/delete/(?P<pk>\d+)/?$", views.Course_DeleteView.as_view(), name="delete-course"),
    url("^course/delete/(?P<id>\d+)/?$", views.delete_course, name="delete-course"),
    # django social login
    # url('', include('social.apps.django_app.urls', namespace='social')),

    # teacher-dashboard
    url("^teacher/home/?$", views.teacher_dashboard, name="teacher_dashboard"),

    url("^teacher/profile/edit/(?P<teacher_id>\d+)/?$", views.teacher_register_form, name="teacher-profile-edit"),
    url("^teacher/password/edit/(?P<user_id>\d+)/?$", views.user_edit_password, name="teacher-password-edit"),
    url("^teacher/course-detail/(?P<course_id>\d+)/?$", views.course_details, name="course-details"),
    url("^teacher/pending_applications/?$", views.pending_applications, name="teacher_pending_applications"),

    # password reset
    # url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect': reverse_lazy('user_password_reset_done'), 'template_name': 'tutors/user_login/password_reset/password_reset_form.html', 'email_template_name': 'tutors/user_login/password_reset/password_reset_email.html'},
    #     name="user_password_reset"),
    # url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'tutors/user_login/password_reset/password_reset_done.html'}, name="user_password_reset_done"),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': reverse_lazy('user_password_reset_complete'), 'template_name': 'tutors/user_login/password_reset/password_reset_confirm.html'}, name="user_password_confirm"),
    # url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'tutors/user_login/password_reset/password_reset_complete.html'}, name="user_password_reset_complete"),

    # user account activation
    url(r'^user/resendactivation/(?P<user_id>\d+)', views.resend_activation, name="resend-activation"),
    url(r'^user/activation_sent', views.activation_sent, name="activation-sent"),
    url(r'^user/confirm/(?P<activation_key>\w+)/', views.user_activated_confirm, name="user_activated_confirm"),

    # search
    url(r'^tutor/search/?$', views.SearchList.as_view(), name="search-list"),

    # student_dashboard
    url("^student/home/?$", views.student_dashboard, name='student_dashboard'),
    url("^student/profile/edit/(?P<student_id>\d+)/?$", views.student_register_form, name="student-profile-edit"),
    url("^student/password/edit(?P<user_id>\d+)/?$", views.user_edit_password, name="student-password-edit"),
    url("^student/pending_applications/?$", views.pending_applications, name="student_pending_applications"),
    url("^student/course-detail/(?P<course_id>\d+)/?$", views.course_details, name="student-course-details"),

    #notification
    url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    #course-application
    url("course/application/(?P<id>\d+)/?$", views.course_application, name="course-application"),

    #calendar swingtime
    url(r'^swingtime/', include('swingtime.urls')),
    url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/monthly/calendar/(?P<year>\d+)/(?P<month>\d+)/?$', views.course_month_view, name='monthly-calendar'),
    url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/daily/calendar/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/?$', views.day_view, name='daily-calendar'),
    url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/add/?$', views.add_course_schedule, name='add-course-schedule'),
    url(r'teacher/course-detail/(?P<course_id>\d+)/schedule/view/(?P<event_id>\d+)/$',views.schedule_view, name='course-schedule_view'),
    url(r'teacher/course-details/schedule/edit/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$', views.occurrence_view, name='swingtime-occurrence'),

    url("^course/teacher/profile/(?P<pk>\d+)/?$", views.teacher_view, name="teacher-view"),
    url("^course/student/profile/(?P<pk>\d+)/?$", views.student_view, name="student-view"),


]
