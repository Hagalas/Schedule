from django.core.management.base import BaseCommand, CommandError
from downloader.models import File, FileCategory
from tasks import run_processors


class Command(BaseCommand):
    help = 'Populates DB.'

    def add_arguments(self, parser):
        parser.add_argument('file_id', nargs='+', type=int)

    def handle(self, *args, **options):
        file_obj = File.objects.get_or_create(
            file_name='teachers.txt',
            file_url='http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_nauczyciel.html',
            category=FileCategory.objects.get_or_create(
                name='teachers',
                code_name='teachers_html_from_wimii',
            )[0],
        )[0]
        file_obj.save()
        run_processors(file_obj)
        self.stdout.write('Successfully added file "%s"' % file_obj.file_name)

        file_obj = File.objects.get_or_create(
            file_name='schedule.txt',
            file_url='http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_grupy.html',
            category=FileCategory.objects.get_or_create(
                name='schedule',
                code_name='html_from_wimii',
            )[0],
        )[0]
        file_obj.save()
        self.stdout.write('Successfully added file "%s"' % file_obj.file_name)
