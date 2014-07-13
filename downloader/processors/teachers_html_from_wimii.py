import sys
import re
from bs4 import BeautifulSoup
from main.models import Teacher, Faculty


class TeachersHtmlFromWimiiProcessor(object):
    """
    Processor which gets or creates a list of teachers on University
    from html file downloaded from University's website.
    """
    def process(self, file_obj):
        teachers_pattern_results = []
        teachers_list = []
        text = []
        file_content = str(file_obj.file.file)
        with open(file_content) as html_doc:
            try:
                soup = BeautifulSoup(html_doc)
                teachers_pattern = \
                    re.compile\
                    (r'^(\w*-{0,1}\w+)\s{1}(\w+.?)\s{1,2}(\w+.?\s*\w*.?\s{0,1}\w*.?\s*\w*.?\s*\w*.?\s*\w*.?\s*\w*.?)\s*/{1}(\w*)/{1}$',
                     re.UNICODE)

                a_hrefs = [link for link in soup.find_all('a') if link.get_text() != '']

                for link in a_hrefs:
                    text.append(link.get_text())
                    teachers_list.append(Teacher())

                for index, t in enumerate(text):
                    single_teacher = re.findall(teachers_pattern, text[index])
                    if single_teacher:
                        teachers_pattern_results.append(single_teacher)

                for index, t in enumerate(teachers_list):
                    name = teachers_pattern_results[index][0][1].strip()
                    surname = teachers_pattern_results[index][0][0].strip()
                    degree = teachers_pattern_results[index][0][2].strip()
                    faculty = teachers_pattern_results[index][0][3].strip()

                    faculty_result, created = Faculty.objects.get_or_create(name=faculty)

                    teachers = Teacher.objects.get_or_create(
                        name=name,
                        surname=surname,
                        degree=degree,
                        faculty=Faculty.objects.get(name=faculty_result)
                    )
            except:
                print sys.exc_info()
                return False
            return True
