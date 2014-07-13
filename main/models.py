# coding=utf-8
from django.db import models


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
    day = models.IntegerField(choices=DAY_CHOICES)
    hour = models.IntegerField(choices=HOUR_CHOICES)
    ordering = ['id']

    class Meta:
        verbose_name = 'Day time'
        verbose_name_plural = 'Day times'

    def __unicode__(self):
        return unicode(self.DAY_CHOICES[self.day][1])+" "+unicode(self.HOUR_CHOICES[self.hour][1])


class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = (
        (1, 'Labs'),
        (2, 'Classes'),
        (3, 'Lectures'),
        (4, 'E-Learning')
    )

    name = models.CharField(max_length=100)
    ects = models.IntegerField(null=True, blank=True)
    exam = models.BooleanField(blank=True)
    type = models.IntegerField(choices=SUBJECT_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __unicode__(self):
        return self.name


class Group(models.Model):
    group_nr = models.IntegerField(blank=True, null=True)
    semester = models.IntegerField(blank=True)
    field_of_study = models.CharField(max_length=50, blank=True, null=True)
    degree = models.IntegerField(blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __unicode__(self):
        return "%s spec:%s st:%d sem:%d gr:%d" \
               % (self.field_of_study, self.specialization, self.degree, self.semester, self.group_nr)


class Faculty(models.Model):
    name = models.CharField(max_length=45, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __unicode__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=5, null=True, blank=True, default='0')
    faculty = models.ForeignKey('Faculty')

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __unicode__(self):
        return unicode(self.faculty)+" "+self.room_number


class Teacher(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    degree = models.CharField(max_length=45)
    room = models.ForeignKey('Room', null=True, blank=True)
    faculty = models.ForeignKey('Faculty')
    email = models.CharField(max_length=45, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __unicode__(self):
        return self.name+" "+self.surname


class Consultations(models.Model):
    teacher = models.ForeignKey('Teacher')
    hour = models.ForeignKey('DayTime')
    faculty = models.ForeignKey('Faculty')

    class Meta:
        verbose_name = 'Consultations'
        verbose_name_plural = 'Consultations'

    def __unicode__(self):
        return self.teacher.name+" "+self.teacher.surname+" "+unicode(self.hour)


class Schedule(models.Model):
    subject = models.ForeignKey('Subject')
    day_time = models.ForeignKey('DayTime')
    group = models.ForeignKey('Group')
    teacher = models.ForeignKey('Teacher')
    room = models.ForeignKey('Room')

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __unicode__(self):
        return self.subject.name