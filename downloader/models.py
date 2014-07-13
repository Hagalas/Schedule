from django.db import models
from optparse import _
from django.contrib.auth.models import User
import sys
import os
import urllib2
from django.core.files.base import ContentFile
from django.conf import settings
from urlparse import urlparse


class FileCategory(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255, blank=False)
    code_name = models.CharField(verbose_name=_('Code name'), max_length=255, blank=False)
    is_active = models.BooleanField(_('Is active'), default=True)

    class Meta:
        verbose_name = _('File category')
        verbose_name_plural = _('File categories')

    def __unicode__(self):
        return self.code_name


class File(models.Model):
    #user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True)
    file_name = models.CharField(verbose_name=_('File name'), max_length=255)
    file_url = models.URLField(verbose_name=_('URL'), default='http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_nauczyciel.html')
    file = models.FileField(verbose_name=_('File'), upload_to='uploads/schedules/%Y-%m/', blank=True, null=True)
    addition_time = models.DateTimeField(verbose_name=_('Addition time'), auto_now_add=True)
    category = models.ForeignKey(FileCategory, verbose_name=_('Category'),
                                 null=True, blank=True)

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def save(self, *args, **kwargs):
        if not self.file:
            download_content_from_site(self)
        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
            super(File, self).delete(*args, **kwargs)
            storage.delete(path)

    def extra_options(self):
        if self.file:
            return "<a href='/download/%s'>Download</a><br>" \
                   "<a href='/parse/%s'>Parse</a>" \
                   % (self.id, self.id)
        else:
            return "No attachment"

    extra_options.allow_tags = True
    extra_options.short_description = "Options"

    def uptime(self):
        return self.addition_time.strftime("%d %b %Y %H:%M:%S")

    uptime.short_description = 'Date'
    uptime.admin_order_field = 'addition_time'

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


from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    instance.file.delete(False)