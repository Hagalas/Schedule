import re
import sys
from bs4 import BeautifulSoup
from main.models import Consultations, DayTime, Faculty, Group, Room, Schedule, Subject, Teacher
debug = 1


def del_items():
    Subject.objects.all().delete()
    Schedule.objects.all().delete()
    Room.objects.all().delete()
    DayTime.objects.all().delete()
    Group.objects.all().delete()


def run(html_doc):
    if debug is 1:
        del_items()
    try:
        soup = BeautifulSoup(html_doc)
        group_name = soup.find('a', href='#table_2_DETAILED').text
        id = soup.find('a', href='#table_2_DETAILED').get('href').strip('#')
        table = soup.find(id=id).find('tbody')
        trs = table.findAll('tr', recursive=False)[:-1]
        hours = {}
        for key in DayTime.HOUR_CHOICES:
            hours[key[1]] = trs[key[0]]
            days = hours[key[1]].findAll('td', attrs={"class": None})
            if days:
                for day_index, day in enumerate(days):
                    room_match = re.findall(r'(s\.\s*\w*)', day.text)
                    string_match = str(day).split("<br/>")
                    teacher_surnames = []
                    teacher_name_first_letters = []
                    subject_name = string_match[0].split('>')[1]
                    teachers = []
                    if len(string_match) > 2:
                        teachers = string_match[1].split(',')
                        for t in teachers:
                            teacher_surnames.append(t.split()[0])
                            teacher_name_first_letters.append(t.split()[1][0])
                    if day.text:
                        day_time = DayTime.objects.get_or_create(
                            day=day_index, hour=int(key[0])
                        )[0]
                        day_time.save()
                        subject = Subject.objects.get_or_create(
                            name=subject_name
                        )[0]
                        subject.save()
                        group = Group.objects.get_or_create(
                            group_name=group_name,
                        )[0]
                        group.save()
                        room_number = 'None'
                        if room_match:
                            room_number = room_match[0].replace(" ", "")
                        room = Room.objects.get_or_create(
                            room_number=room_number,
                        )[0]
                        room.save()
                        schedule = Schedule.objects.create(
                            day_time=day_time,
                            subject=subject,
                            group=group,
                            room=room,
                        )
                        for i, t in enumerate(teachers):
                            teacher = Teacher.objects.filter(
                                surname=teacher_surnames[i], name__startswith=teacher_name_first_letters[i]
                            )
                            if teacher.exists():
                                schedule.teachers.add(teacher[0])
                        schedule.save()

                    if day.get('rowspan'):
                        rowspan_counter = int(day.get('rowspan'))
                        for hour in range(rowspan_counter):
                            day_time = DayTime.objects.get_or_create(
                                day=day_index, hour=int(key[0])+hour
                            )[0]
                            day_time.save()
                            subject = Subject.objects.get_or_create(
                                name=subject_name
                            )[0]
                            subject.save()
                            group = Group.objects.get_or_create(
                                group_name=group_name
                            )[0]
                            group.save()
                            room_number = 'None'
                            if room_match:
                                room_number = room_match[0].replace(" ", "")
                            room = Room.objects.get_or_create(
                                room_number=room_number,
                            )[0]
                            room.save()
                            schedule = Schedule.objects.get_or_create(
                                day_time=day_time,
                                subject=subject,
                                group=group,
                                room=room,
                            )[0]
                            for i, t in enumerate(teachers):
                                teacher = Teacher.objects.filter(
                                    surname=teacher_surnames[i], name__startswith=teacher_name_first_letters[i]
                                )
                                if teacher.exists():
                                    schedule.teachers.add(teacher[0])
                            schedule.save()
    except:
        print sys.exc_info()
        return False
    return True
