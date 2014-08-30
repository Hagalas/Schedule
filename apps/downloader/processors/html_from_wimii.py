# coding=utf-8
import sys
import re
from bs4 import BeautifulSoup
from html_from_wimii_tables import table_2, table_17
from regexes import get_teacher
from main.models import Consultations, DayTime, Faculty, Group, Room, Schedule, Subject, Teacher


class HtmlFromWimiiProcessor(object):
    """
    Processor which gets or creates a list of groups and their schedules on University
    from html file downloaded from University's website.
    """
    tables_codenames = {
        'table_2': table_2,
        # 'table_17': table_17
    }

    @staticmethod
    def run_through_tables(dct, html_doc):
        for k, v in dct.iteritems():
            v.run(html_doc)

    def process(self, file_obj):
        file_content = str(file_obj.file.file)
        with open(file_content) as html_doc:
            self.run_through_tables(self.tables_codenames, html_doc)

    def process2(self, file_obj):
        file_content = str(file_obj.file.file)
        with open(file_content) as html_doc:
            try:
                soup = BeautifulSoup(html_doc)
                teachers_pattern = \
                    re.compile\
                    (r'^(\w*-{0,1}\w+)\s{1}(\w+.?)\s{1,2}(\w+.?\s*\w*.?\s{0,1}\w*.?\s*\w*.?\s*\w*.?\s*\w*.?\s*\w*.?)\s*/{1}(\w*)/{1}$',
                     re.UNICODE)

                group_name = soup.find('a', href='#table_17_DETAILED').text
                id = soup.find('a', href='#table_17_DETAILED').get('href').strip('#')
                table = soup.find(id=id).find('tbody')
                trs = table.findAll('tr', recursive=False)[:-1]
                hours = {}
                for key in DayTime.HOUR_CHOICES:
                    hours[key[1]] = trs[key[0]]
                    days = hours[key[1]].findAll('td', attrs={"class": None})
                    if len(days) != 0:
                        more_than_one_td_helper_list = []
                        only_one_td_helper_list = []
                        for day_index, day in enumerate(days):
                            detailed_table = day.find('table', {"class": "detailed"})
                            if detailed_table:
                                for el in detailed_table.findAll('tr'):
                                    if len(el.findAll('td')) > 1:
                                        more_than_one_td_helper_list.append(el.findAll('td'))
                                    else:
                                        only_one_td_helper_list.append(el.findAll('td'))
                                if len(more_than_one_td_helper_list) != 0:
                                    for each in zip(*more_than_one_td_helper_list):
                                        day_time = DayTime.objects.get_or_create(
                                            day=day_index, hour=int(key[0])
                                        )[0]
                                        day_time.save()
                                        subject = Subject.objects.get_or_create(
                                            name="%s %s" % (each[1].text, each[0].text)
                                        )[0]
                                        subject.save()
                                        group = Group.objects.get_or_create(
                                            group_name=group_name
                                        )[0]
                                        group.save()
                                        single_teacher = re.findall(teachers_pattern, each[2].text)[0]
                                        teacher = Teacher.objects.get_or_create(
                                            name=single_teacher[1],
                                            surname=single_teacher[0],
                                            degree=single_teacher[2],
                                            faculty=Faculty.objects.get_or_create(
                                                name=single_teacher[3]
                                            )[0]
                                        )[0]
                                        teacher.save()
                                        room = Room.objects.get_or_create(
                                            room_number=each[3].text, faculty=Faculty.objects.get(id=1)
                                        )[0]
                                        room.save()
                                        schedule = Schedule.objects.get_or_create(
                                            day_time=day_time,
                                            subject=subject,
                                            group=group,
                                            teacher=teacher,
                                            room=room,
                                        )[0]
                                        schedule.save()

                                if len(only_one_td_helper_list) != 0:
                                    for each in zip(*only_one_td_helper_list):
                                        day_time = DayTime.objects.get_or_create(
                                            day=day_index, hour=int(key[0])
                                        )[0]
                                        day_time.save()
                                        subject = Subject.objects.get_or_create(
                                            name="%s %s" % (each[1].text, each[0].text)
                                        )[0]
                                        subject.save()
                                        group = Group.objects.get_or_create(
                                            group_name=group_name
                                        )[0]
                                        group.save()
                                        multi_teacher = each[2].text.split(',')
                                        teachers = []
                                        for t in multi_teacher:
                                            if len(re.findall(teachers_pattern, t.strip())) > 0:
                                                single_teacher = re.findall(teachers_pattern, t.strip())[0]
                                                print single_teacher
                                                teacher = Teacher.objects.get_or_create(
                                                    name=single_teacher[1],
                                                    surname=single_teacher[0],
                                                    degree=single_teacher[2],
                                                    faculty=Faculty.objects.get_or_create(
                                                        name=single_teacher[3]
                                                    )[0]
                                                )[0]
                                                teacher.save()
                                                teachers.append(teacher)
                                        print teachers
                                        room = Room.objects.get_or_create(
                                            room_number=each[3].text, faculty=Faculty.objects.get(id=1)
                                        )[0]
                                        room.save()
                                        schedule = Schedule.objects.get_or_create(
                                            day_time=day_time,
                                            subject=subject,
                                            group=group,
                                            room=room,
                                        )[0]

                                        schedule.save()

                            elif day.get('rowspan'):
                                rowspan_counter = int(day.get('rowspan'))
                                for hour in range(rowspan_counter):
                                    day_time = DayTime.objects.get_or_create(
                                        day=day_index, hour=int(key[0])+hour
                                    )[0]
                                    day_time.save()
                                    subject_name = day.getText()
                                    subject = Subject.objects.get_or_create(
                                        name=subject_name
                                    )[0]
                                    subject.save()
                                    group = Group.objects.get_or_create(
                                        group_name=group_name
                                    )[0]
                                    group.save()
                                    room = Room.objects.get_or_create(
                                        room_number='1', faculty=Faculty.objects.get(id=1)
                                    )[0]
                                    room.save()
                                    schedule = Schedule.objects.get_or_create(
                                        day_time=day_time,
                                        subject=subject,
                                        group=group,
                                        teacher=Teacher.objects.all()[0],
                                        room=room,
                                    )[0]
                                    schedule.save()
                            elif day.text:
                                day_time = DayTime.objects.get_or_create(
                                    day=day_index, hour=int(key[0])
                                )[0]
                                day_time.save()
                                subject_name = day.getText()
                                subject = Subject.objects.get_or_create(
                                    name=subject_name
                                )[0]
                                subject.save()
                                group = Group.objects.get_or_create(
                                    group_name=group_name,
                                )[0]
                                group.save()
                                room = Room.objects.get_or_create(
                                    room_number='1', faculty=Faculty.objects.get(id=1)
                                )[0]
                                room.save()
                                schedule = Schedule(
                                    day_time=day_time,
                                    subject=subject,
                                    group=group,
                                    teacher=Teacher.objects.all()[0],
                                    room=room,
                                )
                                schedule.save()

                # for i in soup.findAll('a', href=re.compile(r'^(?!#top)')):
                #     id_of_table = i.get('href').strip('#')
                #     table = soup.find(id=id_of_table)
                #     group_name = i.getText()
                #     group = Group.objects.get_or_create(group_name=group_name)[0]
                #     group.save()
            except:
                print sys.exc_info()
                return False
            return True


def deli():
    from main.models import *
    Subject.objects.all().delete()
    Schedule.objects.all().delete()
    Room.objects.all().delete()
    DayTime.objects.all().delete()
    Group.objects.all().delete()
