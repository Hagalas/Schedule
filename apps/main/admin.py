from django.contrib import admin
from main.models import Subject, DayTime, Group, Room, Faculty, Teacher, Schedule, Consultations


class ConsultationsAdmin(admin.ModelAdmin):
    ordering = ['teacher']


class DayTimeAdmin(admin.ModelAdmin):
    ordering = ['day', 'hour']


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'address', 'phone_number']
    ordering = ['id']


class GroupAdmin(admin.ModelAdmin):
    fields = (('field_of_study', 'specialization'), ('degree', 'group_nr', 'semester'))
    list_display = ['group_name', 'field_of_study', 'degree', 'semester', 'group_nr', 'specialization']
    ordering = ['group_name']
    search_fields = ['field_of_study', 'degree', 'semester', 'group_nr', 'specialization']
    list_filter = ('field_of_study', 'degree', 'semester', 'group_nr', 'specialization')


class RoomAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'room_number']
    ordering = ['faculty', 'room_number']


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['subject', 'day_time', 'teacher_names', 'group', 'room']
    list_display_links = ['subject']
    ordering = ['group__group_name']
    list_filter = ['group__group_name', 'teachers', 'day_time__day', 'day_time__hour']
    search_fields = ['group', 'teachers', 'day_time']
    list_per_page = 250
    filter_horizontal = ['teachers']


class TeacherAdmin(admin.ModelAdmin):
    fields = (('surname', 'name'), ('degree', 'faculty'))
    list_display_links = ['surname', 'name']
    list_display = ['degree', 'surname', 'name', 'faculty_link']
    ordering = ['surname']
    search_fields = ['surname']
    list_filter = ['faculty']
    list_per_page = 250


admin.site.register(Consultations, ConsultationsAdmin)
admin.site.register(DayTime, DayTimeAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)

