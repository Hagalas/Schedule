from django.db import models
from optparse import _
import sys
import os
import urllib2
from django.core.files.base import ContentFile
from django.conf import settings
from urlparse import urlparse


class FileCategory(models.Model):
    code_name = models.CharField(verbose_name=_('Code name'), max_length=255, blank=False)
    is_active = models.BooleanField(_('Is active'), default=True)

    class Meta:
        verbose_name = _('File category')
        verbose_name_plural = _('File categories')

    def __unicode__(self):
        return self.code_name


class File(models.Model):
    file_name = models.CharField(verbose_name=_('File name'), max_length=255)
    file_url = models.URLField(verbose_name=_('URL'), default='http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_nauczyciel.html')
    file = models.FileField(verbose_name=_('File'), upload_to='uploads/schedules/%Y-%m/', blank=True, null=True)
    addition_time = models.DateTimeField(verbose_name=_('Addition time'), auto_now_add=True)
    category = models.ForeignKey(FileCategory, verbose_name=_('Category'),
                                 null=True, blank=True)

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    #latest_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/latest')
    #archive_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/archive')

    def save(self, *args, **kwargs):
        if not self.file:
            download_content_from_site(self)
            # if os.path.exists(os.path.join(self.latest_dir, self.file_name)):
            #     import shutil
            #     import datetime
            #     new_file_name = \
            #         os.path.join(self.archive_dir, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")+self.file_name)
            #     shutil.move(os.path.join(self.latest_dir, self.file_name), new_file_name)
            #     download_content_from_site(self)
            # else:
            #     download_content_from_site(self)
        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(File, self).delete(*args, **kwargs)
        storage.delete(path)

    def extra_options(self):
        if self.file:
            new_name = self.file_name.replace('.', '-')
            return "<a href='/download/%s-%s'>Download</a>" % (new_name, self.id)
            #return "<a href='%s'>Download</a>" % (self.file.url,)
        else:
            return "No attachment"

    extra_options.allow_tags = True
    extra_options.short_description = "Options"

    def uptime(self):
        return self.addition_time.strftime("%d %b %Y %H:%M:%S")

    uptime.short_description = 'Date'

    def __unicode__(self):
        return self.file_name


def download_content_from_site(self):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    req = urllib2.Request(self.file_url, headers=headers)
    content = urllib2.urlopen(req).read()
    self.file.save(self.file_name, ContentFile(content), save=True)