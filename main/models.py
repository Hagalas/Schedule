# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DayTime(models.Model):
    DAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    HOUR_CHOICES = (
        (0, '8-9'),
        (1, '9-10'),
        (2, '9-10'),
        (3, '10-11'),
        (4, '11-12'),
        (5, '12-13'),
        (6, '13-14'),
        (7, '14-15'),
        (8, '15-16'),
        (9, '16-17'),
        (10, '17-18'),
        (11, '18-19'),
        (12, '19-20'),

    )
    day = models.IntegerField(_('Day'), choices=DAY_CHOICES)
    hour = models.IntegerField(_('Hour'), choices=HOUR_CHOICES)
    ordering = ['id']

    class Meta:
        verbose_name = _('Day time')
        verbose_name_plural = _('Day times')

    def __unicode__(self):
        return unicode(self.DAY_CHOICES[self.day][1])+" "+unicode(self.HOUR_CHOICES[self.hour][1])


class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = (
        (1, 'Labs'),
        (2, 'Classes'),
        (3, 'Lectures'),
        (4, 'E-Learning')
    )

    name = models.CharField(_('Name'), max_length=100)
    ects = models.IntegerField(_('ECTS'), null=True, blank=True)
    exam = models.BooleanField(_('Exam'), blank=True)
    type = models.IntegerField(_('Type'), choices=SUBJECT_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __unicode__(self):
        return self.name


class Group(models.Model):
    group_nr = models.IntegerField(_('Group number'), blank=True, null=True)
    semester = models.IntegerField(_('Semester'), blank=True)
    field_of_study = models.CharField(_('Field of study'), max_length=50, blank=True, null=True)
    degree = models.IntegerField(_('Degree'), blank=True)
    specialization = models.CharField(_('Specialization'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __unicode__(self):
        return "%s spec:%s st:%d sem:%d gr:%d" \
               % (self.field_of_study, self.specialization, self.degree, self.semester, self.group_nr)


class Faculty(models.Model):
    name = models.CharField(_('Name'), max_length=45, null=True, blank=True)
    address = models.CharField(_('Address'), max_length=100, null=True, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    def __unicode__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(_('Room number'), max_length=5, null=True, blank=True, default='0')
    faculty = models.ForeignKey('Faculty', verbose_name=_('Faculty'))

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __unicode__(self):
        return unicode(self.faculty)+" "+self.room_number


class Teacher(models.Model):
    name = models.CharField(_('Name'), max_length=45)
    surname = models.CharField(_('Surname'), max_length=45)
    degree = models.CharField(_('Degree'), max_length=45)
    room = models.ForeignKey('Room', verbose_name=_('Room'), null=True, blank=True)
    faculty = models.ForeignKey('Faculty', verbose_name=_('Faculty'))
    email = models.CharField(_('Email'), max_length=45, null=True, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    def __unicode__(self):
        return self.name+" "+self.surname


class Consultations(models.Model):
    teacher = models.ForeignKey('Teacher', verbose_name=_('Teacher'))
    hour = models.ForeignKey('DayTime', verbose_name=_('Hour'))
    faculty = models.ForeignKey('Faculty', verbose_name=_('Faculty'))

    class Meta:
        verbose_name = _('Consultations')
        verbose_name_plural = _('Consultations')

    def __unicode__(self):
        return self.teacher.name+" "+self.teacher.surname+" "+unicode(self.hour)


class Schedule(models.Model):
    subject = models.ForeignKey('Subject', verbose_name=_('Subject'))
    day_time = models.ForeignKey('DayTime', verbose_name=_('Day time'))
    group = models.ForeignKey('Group', verbose_name=_('Group'))
    teacher = models.ForeignKey('Teacher', verbose_name=_('Teacher'))
    room = models.ForeignKey('Room', verbose_name=_('Room'))

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

    def __unicode__(self):
        return self.subject.name