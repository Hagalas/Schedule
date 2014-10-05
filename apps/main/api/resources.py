# -*- coding: utf-8
from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from main.models import Room
from main.models import Subject
from main.models import Faculty
from main.models import Group
from main.models import Teacher
from main.models import Schedule


class RoomResource(ModelResource):
    class Meta:
        resource_name = 'room'
        queryset = Room.objects.all()


class SubjectResource(ModelResource):
    class Meta:
        resource_name = 'subject'
        queryset = Subject.objects.all()


class FacultyResource(ModelResource):
    class Meta:
        resource_name = 'faculty'
        queryset = Faculty.objects.all()


class GroupResource(ModelResource):
    class Meta:
        resource_name = 'group'
        queryset = Group.objects.all()


class TeacherResource(ModelResource):

    #schedule = fields.ToOneField('main.api.resources.ScheduleResource', 'teacher')

    class Meta:
        resource_name = 'teacher'
        queryset = Teacher.objects.all()


class ScheduleResource(ModelResource):

    room = fields.ForeignKey(RoomResource, 'room')
    subject = fields.ForeignKey(SubjectResource, 'subject')
    #faculty = fields.ForeignKey(FacultyResource, 'faculty')
    teachers = fields.ToManyField('main.api.resources.TeacherResource', attribute='teachers')
    group = fields.ForeignKey(GroupResource, 'group')

    class Meta:
        resource_name = 'schedule'
        queryset = Schedule.objects.all()
        allowed_methods = ['get']
        include_resource_uri = True
        limit = 50