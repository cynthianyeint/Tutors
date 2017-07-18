from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from notifications.models import Notification
from swingtime.models import Event, Occurrence

TITLE_CHOICES = (
    ('mr.', 'Mr.'),
    ('ms.', 'Ms.'),
    # ('mrs.', 'Mrs.'),
    # ('dr.', 'Dr.'),
    # ('prof.', 'Prof.'),
)


class Teacher(models.Model):
    title = models.CharField(max_length=20, null=True, blank=False, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    nickname = models.CharField(max_length=100, blank=True, null=False, default='')
    dob = models.DateField(blank=False, null=True)
    private_birthyear = models.BooleanField(blank=False, null=False, default=False)
    website = models.CharField(max_length=200, blank=True, null=False, default='')
    user = models.ForeignKey(User, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{6,15}$', message="Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)
    home_phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)
    biography = models.TextField(blank=True, null=False, default='')

    @property
    def avatar(self):
        if self.user and self.user.userprofile_set.count() > 0:
            return self.user.userprofile_set.first().avatar
        return None

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return None

    @property
    def title_text(self):
        for (k, v) in TITLE_CHOICES:
            if k == self.title:
                return v

        return ""

    def __unicode__(self):
        return ("%s %s %s" % (self.title_text, self.first_name, self.last_name if self.last_name else "")).strip()

    @property
    def user_activated(self):
        return self.user.useractivation_set.last().is_activated

    @property
    def get_phone_number(self):
        if self.home_phone_number and self.mobile_number:
            return "%s , %s" % (self.home_phone_number, self.mobile_number)
        elif self.home_phone_number:
            return self.home_phone_number
        elif self.mobile_number:
            return self.mobile_number
        else:
            return "-"

    @property
    def get_website(self):
        return self.website if self.website else "-"

    @property
    def email(self):
        return self.user.email if self.user and self.user.email else "-"

    @property
    def username(self):
        return self.user.username if self.user and self.user.username else "-"

    @property
    def get_nickname(self):
        return self.nickname if self.nickname else "-"

    @property
    def get_pending_applications(self):
        return Application.objects.filter(teacher=self, status="Pending")

    @property
    def get_teacher_name_with_tile(self):
        return ("%s %s %s" % (self.title_text, self.first_name, self.last_name if self.last_name else "")).strip()


class ClassCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __unicode__(self):
        return self.name


class AllCourseManager(models.Manager):
    def get_queryset(self):
        queryset = super(AllCourseManager, self).get_queryset().exclude(enabled=False).exclude(published=False)
        return queryset


class EnabledCourseManager(models.Manager):
    def get_queryset(self):
        queryset = super(EnabledCourseManager, self).get_queryset().exclude(enabled=False)
        return queryset


class Class(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(ClassCategory)
    teacher = models.ForeignKey(Teacher)
    description = models.TextField(blank=True, null=False, default='')
    published = models.BooleanField(default=True, blank=True)
    enabled = models.NullBooleanField(default=True, blank=True)
    student = models.ManyToManyField('Student', blank=True, related_name='student')
    objects = AllCourseManager()
    enabled_objects = EnabledCourseManager()
    class_event = models.OneToOneField(Event, default="", null=True, blank=True)
    recommendation = models.ManyToManyField('Student', blank=True, related_name='recommendation')
    # youtube_regex = RegexValidator(regex=r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$', message="Please enter valid youtube link.")
    youtube_regex = RegexValidator(regex=r'^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$', message="Please enter valid youtube link.")
    youtube_link = models.CharField(max_length=100, validators=[youtube_regex], blank=True, null=True)

    def __unicode__(self):
        return self.title

    @property
    def get_class_schedule(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        result = []
        for o in occurrence:
            row = {
                'start_time': o.start_time,
                'end_time': o.end_time
            }
            result.append(row)
        return result

    @property
    def weekly_class_event(self):
        return Event.objects.filter(id=self.class_event_id,event_type__label="Weekly").exists()

    # @property
    # def get_class_schedule(self):
    #     time_slot = TimeSlot.objects.filter(schedule__cls=self)
    #     result = []
    #     for t in time_slot:
    #         row = {
    #             'date': t.day,
    #             'from_time': t.from_time,
    #             'to_time': t.to_time
    #         }
    #         result.append(row)
    #     return result

    @property
    def day_mon(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Monday":
                return True

    @property
    def day_tue(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Tuesday":
                return True

    @property
    def day_wed(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Wednesday":
                return True

    @property
    def day_thu(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Thursday":
                return True

    @property
    def day_fri(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Friday":
                return True

    @property
    def day_sat(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Saturday":
                return True

    @property
    def day_sun(self):
        occurrence = Occurrence.objects.filter(event=self.class_event)
        for o in occurrence:
            if o.start_time.date().strftime("%A") == "Sunday":
                return True

    # @property
    # def day_mon(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=1).exists()
    #
    # @property
    # def day_tue(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=2).exists()
    #
    # @property
    # def day_wed(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=3).exists()
    #
    # @property
    # def day_thu(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=4).exists()
    #
    # @property
    # def day_fri(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=5).exists()
    #
    # @property
    # def day_sat(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=6).exists()
    #
    # @property
    # def day_sun(self):
    #     return TimeSlot.objects.filter(schedule__cls=self, int_day=7).exists()

    @property
    def total_no_of_students(self):
        return self.student.count

    @property
    def get_pending_applications(self):
        return Application.objects.filter(course=self, status="Pending")


class ClassSchedule(models.Model):
    cls = models.ForeignKey(Class, null=False)


DAY_CHOICES = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)


class DayField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = DAY_CHOICES
        super(DayField, self).__init__(*args, **kwargs)


class TimeSlot(models.Model):
    schedule = models.ForeignKey(ClassSchedule, null=False, blank=False)
    int_day = DayField(null=False, blank=False)
    from_time = models.TimeField(null=False, blank=False)
    to_time = models.TimeField(null=False, blank=False)

    @property
    def day(self):
        for (k, v) in DAY_CHOICES:
            if k == self.int_day:
                return v
        return ''


class UserActivation(models.Model):
    user = models.ForeignKey(User)
    activation_key = models.CharField(max_length=50, blank=True, null=True)
    activation_date = models.DateTimeField(blank=True, null=True)
    is_activated = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.__str__()


def upload_to(instance, filename):
    img_path = "user_profile_images/%s" % (filename)
    return img_path


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    avatar = models.ImageField('Profile Image', upload_to=upload_to, null=True, blank=True)

    def __unicode__(self):
        return self.avatar


class Student(models.Model):
    title = models.CharField(max_length=20, null=True, blank=False, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    dob = models.DateField(blank=False, null=True)
    user = models.ForeignKey(User, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{6,15}$', message="Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)
    home_phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)

    def __unicode__(self):
        return ("%s %s %s" % (self.title_text, self.first_name, self.last_name if self.last_name else "")).strip()

    @property
    def user_activated(self):
        return self.user.useractivation_set.last().is_activated

    @property
    def title_text(self):
        for (k, v) in TITLE_CHOICES:
            if k == self.title:
                return v

        return ""

    @property
    def avatar(self):
        if self.user and self.user.userprofile_set.count() > 0:
            return self.user.userprofile_set.first().avatar
        return None

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url


    @property
    def get_phone_number(self):
        if self.home_phone_number and self.mobile_number:
            return "%s , %s" % (self.home_phone_number, self.mobile_number)
        elif self.home_phone_number:
            return self.home_phone_number
        elif self.mobile_number:
            return self.mobile_number
        else:
            return "-"

    @property
    def email(self):
        return self.user.email if self.user and self.user.email else "-"

    @property
    def username(self):
        return self.user.username if self.user and self.user.username else "-"

    @property
    def course(self):
        return self.student.all()

    @property
    def get_pending_applications(self):
        return Application.objects.filter(student=self, status="Pending")


class Application(models.Model):
    course = models.ForeignKey(Class, null=False)
    student = models.ForeignKey(Student, null=False)
    teacher = models.ForeignKey(Teacher, null=False)
    status = models.CharField(max_length=100, null=True, blank=True)

    @property
    def pending_app_noti(self):
        return Notification.objects.filter(recipient=self.teacher.user).exists()

    @property
    def confirm_app_noti(self):
        return Notification.objects.filter(recipient=self.student.user).exists()


def course_upload_to(instance, filename):
    img_path = "course_images/%s" % filename
    return img_path


class CourseImageUpload(models.Model):
    class_obj = models.ForeignKey(Class)
    images = models.ImageField('Course Images', upload_to=course_upload_to, null=True, blank=True)

    def __unicode__(self):
        return self.images
