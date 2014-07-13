from django.contrib import admin
from main.models import Subject, DayTime, Group, Room, Faculty, Teacher, Schedule, Consultations


class TeacherAdmin(admin.ModelAdmin):
    fields = (('name', 'surname'), ('degree', 'faculty'))
    list_display_links = ['surname', 'name']
    list_display = ['degree', 'name', 'surname', 'faculty']
    ordering = ['surname']
    search_fields = ['surname']
    list_filter = ['faculty']
    list_per_page = 250


class GroupAdmin(admin.ModelAdmin):
    fields = (('field_of_study', 'specialization'), ('degree', 'group_nr', 'semester'))
    list_display = ['field_of_study', 'degree', 'semester', 'group_nr', 'specialization']
    ordering = ['field_of_study']
    search_fields = ['field_of_study', 'degree', 'semester', 'group_nr', 'specialization']
    list_filter = ('field_of_study', 'degree', 'semester', 'group_nr', 'specialization')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'day_time', 'teacher', 'group', 'room']
    ordering = ['id']


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number']
    ordering = ['id']


class ConsultationsAdmin(admin.ModelAdmin):
    ordering = ['teacher']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'room_number']
    ordering = ['faculty', 'room_number']

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Subject)
admin.site.register(Room, RoomAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(DayTime)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Consultations, ConsultationsAdmin)

