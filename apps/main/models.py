# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GetOrNoneManager(models.Manager):
    """
    Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class DayTime(models.Model):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    DAY_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )
    HOUR_CHOICES = (
        (0, '8-9'),
        (1, '9-10'),
        (2, '10-11'),
        (3, '11-12'),
        (4, '12-13'),
        (5, '13-14'),
        (6, '14-15'),
        (7, '15-16'),
        (8, '16-17'),
        (9, '17-18'),
        (10, '18-19'),
        (11, '19-20'),

    )
    day = models.IntegerField(_('Day'), choices=DAY_CHOICES)
    hour = models.IntegerField(_('Hour'), choices=HOUR_CHOICES)

    class Meta:
        verbose_name = _('Day time')
        verbose_name_plural = _('Day times')
        ordering = ['day', 'hour']

    def __unicode__(self):
        return unicode(self.DAY_CHOICES[self.day][1])+" "+unicode(self.HOUR_CHOICES[self.hour][1])


class Subject(models.Model):
    LABS = 1
    CLASSES = 2
    LECTURES = 3
    E_LEARNING = 4

    SUBJECT_TYPE_CHOICES = (
        (LABS, 'Labs'),
        (CLASSES, 'Classes'),
        (LECTURES, 'Lectures'),
        (E_LEARNING, 'E-Learning')
    )

    name = models.CharField(_('Name'), max_length=255)
    ects = models.IntegerField(_('ECTS'), null=True, blank=True)
    exam = models.BooleanField(_('Exam'))
    type = models.IntegerField(_('Type'), choices=SUBJECT_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __unicode__(self):
        return self.name


class Group(models.Model):
    group_name = models.CharField(_('Group name'), max_length=255, blank=True, null=True)
    group_nr = models.IntegerField(_('Group number'), blank=True, null=True)
    degree = models.IntegerField(_('Degree'), blank=True, null=True)
    field_of_study = models.CharField(_('Field of study'), max_length=50, blank=True)
    semester = models.IntegerField(_('Semester'), blank=True, null=True)
    specialization = models.CharField(_('Specialization'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __unicode__(self):
        return self.group_name  # "%s spec:%s st:%s sem:%s gr:%s" \
               # % (self.field_of_study, self.specialization, self.degree, self.semester, self.group_nr)


class Faculty(models.Model):
    name = models.CharField(_('Name'), max_length=45, blank=True)
    full_name = models.CharField(_('Full name'), max_length=255, blank=True)
    address = models.CharField(_('Address'), max_length=100, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=12, blank=True)

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    def __unicode__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(_('Room number'), max_length=255, blank=True, default='0')
    faculty = models.ForeignKey('Faculty', verbose_name=_('Faculty'), null=True, blank=True)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __unicode__(self):
        return "%s" % self.room_number


class Teacher(models.Model):
    name = models.CharField(_('Name'), max_length=45, help_text=_('Maximum 45 characters.'))
    surname = models.CharField(_('Surname'), max_length=45, help_text=_('Maximum 45 characters.'))
    degree = models.CharField(_('Degree'), max_length=45)
    email = models.CharField(_('Email'), max_length=45, blank=True)
    faculty = models.ForeignKey('Faculty', verbose_name=_('Faculty'))
    phone_number = models.CharField(_('Phone number'), max_length=12, blank=True)
    room = models.ForeignKey('Room', verbose_name=_('Room'), null=True, blank=True)

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    def faculty_link(self):
        return "<a href='/admin/main/faculty/%s'>%s</a>" % (self.faculty.id, self.faculty)

    faculty_link.allow_tags = True
    faculty_link.short_description = "Faculty"
    faculty_link.admin_order_field = 'faculty'

    def __unicode__(self):
        return self.surname+" "+self.name


class Consultations(models.Model):
    teacher = models.ForeignKey('Teacher', verbose_name=_('Teacher'))
    faculty = models.ForeignKey('Faculty', verbose_name=_('Faculty'))
    hour = models.ForeignKey('DayTime', verbose_name=_('Hour'))

    class Meta:
        verbose_name = _('Consultations')
        verbose_name_plural = _('Consultations')

    def __unicode__(self):
        return self.teacher.surname+" "+self.teacher.name+" "+unicode(self.hour)


class Schedule(models.Model):
    subject = models.ForeignKey('Subject', verbose_name=_('Subject'), null=True, blank=True)
    day_time = models.ForeignKey('DayTime', verbose_name=_('Day time'), null=True, blank=True)
    group = models.ForeignKey('Group', verbose_name=_('Group'), null=True, blank=True)
    room = models.ForeignKey('Room', verbose_name=_('Room'), null=True, blank=True)
    teachers = models.ManyToManyField(                                                  # todo one to many or foreign key
        Teacher, related_name='Teachers', verbose_name=_('Teachers'), null=True, blank=True
    )

    class Meta:
        verbose_name = _('Schedule Entry')
        verbose_name_plural = _('Schedule')

    def teacher_names(self):
        return ' , '.join(
            ["<a href='/admin/main/teacher/%s'>" % t.id + unicode(t) + "</a>" for t in self.teachers.all()]
        )

    teacher_names.allow_tags = True
    teacher_names.short_description = _('Teachers')

    def group_name(self):
        return "<a href='/admin/main/group/%s'>%s</a>" % (self.group.id, self.group)

    group_name.allow_tags = True
    group_name.short_description = _('Group')

    def __unicode__(self):
        return str(self.day_time)+" "+self.subject.name