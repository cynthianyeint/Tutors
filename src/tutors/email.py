from django.core.urlresolvers import reverse

__author__ = 'lian'

from django.core.mail import EmailMessage
from tuition import settings


EMAIL_IS_LIVE = False
SEND_EMAIL = False


class TutorEmail(EmailMessage):
    def send(self, fail_silently=False):
        if not EMAIL_IS_LIVE:
            if self.to:
                self.body = '[This email is going to ' + ', '.join(self.to) + ']' + "\n\n" + self.body
                self.to = ['lian.hui.lui@gmail.com']

        if SEND_EMAIL:
            super(TutorEmail, self).send(fail_silently=fail_silently)


def send_tutor_mail(email_subject, email_body, from_email, to_email_list, fail_silently=False):
    mail = TutorEmail()
    mail.subject = email_subject
    mail.body = email_body
    mail.from_email = from_email
    mail.to = to_email_list
    mail.send(fail_silently)


def send_user_account_activation_email(user, key):
    if user and user.email:
        email = user.email
        email_subject = "Account confirmation"

        confirm_link = reverse('user_activated_confirm', kwargs={'activation_key': key})
        full_link = settings.SITE_NAME + confirm_link

        email_body = "Hello! Thanks for signing up. To activate your account, click this link " + full_link

        send_tutor_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=True)
