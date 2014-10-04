from processors import html_from_wimii, teachers_html_from_wimii, groups_from_wimii


def run_processors(file_obj):
    """
    Method runs processors for specific category of the file.
    To add new, append category to processors dict like below.
    """
    processors = {
        'html_from_wimii': html_from_wimii.HtmlFromWimiiProcessor,
        'teachers_html_from_wimii': teachers_html_from_wimii.TeachersHtmlFromWimiiProcessor,
        'groups_from_wimii': groups_from_wimii.GroupsHtmlFromWimiiProcessor
    }

    processor = processors.get(file_obj.category.code_name, None)
    if processor:
        obj = processor()
        obj.process(file_obj)