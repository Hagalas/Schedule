__author__ = 'oskarmarszalek'

import re


def get_teacher():
    teachers_pattern = re.compile(
        r'^(\w*-{0,1}\w+)\s{1}(\w+.?)\s{1,2}(\w+.?\s*\w*.?\s{0,1}\w*.?\s*\w*.?\s*\w*.?\s*\w*.?\s*\w*.?)\s*/{1}(\w*)/{1}$',
        re.UNICODE
    )
