# -*- coding: utf-8
import sys
import re
import urllib2
from bs4 import BeautifulSoup
from main.models import Group, DayTime, Subject, Schedule, Teacher, Room, Faculty


class GroupsHtmlFromWimiiProcessor(object):
    """
    Processor which gets or creates a list of groups on University
    from html file downloaded from University's website.
    """
    def process(self, file_obj):
        file_content = str(file_obj.file.file)
        with open(file_content) as html_doc:
            try:
                teachers_pattern = \
                    re.compile\
                    (r'^(\w*-{0,1}\w+)\s{1}(\w+.?)\s{1,2}(\w+.?\s*\w*.?\s{0,1}\w*.?\s*\w*.?\s*\w*.?\s*\w*.?\s*\w*.?)\s*/{1}(\w*)/{1}$',
                     re.UNICODE)
                #teachers_pattern = re.compile(r'^', re.UNICODE)

                soup = BeautifulSoup(html_doc)
                links = [link for link in soup.find_all('a') if link.get_text() != ''][:-1]
                # last ahref is an advertisement

                groups = []
                for link in links:
                    #print link
                    group_name = link.getText().strip()
                    group = Group.objects.get_or_create(
                        group_name=group_name
                    )[0]
                    group.save()
                    groups.append(group)
#
                    html = urllib2.urlopen('http://wimii.pcz.pl/download/plan_stacjonarny/%s' % link.get('href')).read()
                    html = BeautifulSoup(html)
                    trs = html.findAll('tr')[1:]
                    hours = {}
                    for key in DayTime.HOUR_CHOICES:
                        hours[key[1]] = trs[key[0]]
                        days = hours[key[1]].findAll('td', attrs={"class": None})[1:]
                        for day_index, day in enumerate(days):
                            day_time = DayTime.objects.get_or_create(
                                day=day_index, hour=int(key[0])
                            )[0]
                            day_time.save()
                            if len(day.text) > 1:
                                is_subject = False
                                is_teacher = False
                                is_room = False
                                subject_name = ''
                                teachers = []
                                room_number = ''
                                day_split = str(day).split('<br>')

                                # if len(day_split) > 4:
                                #     subject_name = str(day).split('<br>')[0].strip('<td>')
                                #     if len(subject_name) > 0: is_subject = True
                                #     teachers = str(day).split('<br>')[1:-1]
                                #     if len(teachers) > 0:
                                #         if len(teachers[0]) > 0 \
                                #                 and teachers[0] != 'zielone' \
                                #                 and teachers[0] != 'fioletowe'\
                                #                 and teachers[0] != 'czerwone':
                                #             print teachers[0]
                                #             is_teacher = True
                                #     room_number = \
                                #         str(day).split('<br>')[-1].split('/')[0].strip('<br>')
                                #     if len(room_number) > 0: is_room = True

                                if len(day_split) >= 3:
                                    subject_name = str(day).split('<br>')[0].strip('<td>')
                                    if len(subject_name) > 0: is_subject = True
                                    test = str(day).split('<br>')[1]
                                    teachers.append(test)
                                    if len(teachers) > 0:
                                        if len(teachers[0]) > 0 \
                                                and teachers[0] != 'zielone' \
                                                and teachers[0] != 'fioletowe'\
                                                and teachers[0] != 'czerwone'\
                                                and teachers[0] != 'czarne'\
                                                and teachers[0] != "1 lab odbędą się 3.10.2014 na /WIPiTM/":
                                            print teachers[0]
                                            is_teacher = True
                                    room_number = \
                                        str(day).split('<br>')[2].split('/')[0].strip('<br>')
                                    if len(room_number) > 0: is_room = True

                                elif len(day_split) == 2:
                                    subject_name = str(day).split('<br>')[0].strip('<td>')
                                    is_subject = True
                                    room_number = \
                                        str(day).split('<br>')[1].split('/')[0].strip('<br>')
                                    is_room = True

                                elif len(day_split) == 1:
                                    pass

                                if is_subject:
                                    subject = Subject.objects.get_or_create(
                                        name=subject_name
                                    )[0]
                                    subject.save()

                                if is_room:
                                    room = Room.objects.get_or_create(
                                        room_number=room_number
                                    )[0]
                                    room.save()

                                if is_room and is_subject:
                                    schedule = Schedule.objects.get_or_create(
                                        day_time=day_time,
                                        subject=subject,
                                        group=group,
                                        room=room,
                                    )[0]
                                    schedule.save()

                                if is_teacher:
                                    for teacher in teachers:
                                        single_teacher = teacher.split()  # re.findall(teachers_pattern, teachers)[0]
                                        teacher = Teacher.objects.get_or_create(
                                            name=single_teacher[1],
                                            surname=single_teacher[0],
                                            degree=' '.join(single_teacher[2:-1]),
                                            faculty=Faculty.objects.get_or_create(
                                                name=single_teacher[-1]
                                            )[0]
                                        )[0]
                                        teacher.save()
                                        schedule.teachers.add(teacher)
                                        schedule.save()
#
            except:
                print sys.exc_info()
                return False
            return True