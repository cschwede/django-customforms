#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.db import models


class Form(models.Model):
    title = models.CharField(_("Title"), max_length=255)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ('title', )

    def get_absolute_url(self):
        return reverse('customforms.views.view_form', args=[str(self.id)])


class Question(models.Model):
    form = models.ForeignKey(Form)
    title = models.CharField(
        _("Title"), max_length=255, default=_("Question Title"))
    help_text = models.TextField(blank=True, null=True)
    CHOICES = [
        ('C', _('Checkbox')),
        ('R', _('Radio')),
        ('S', _('Select')),
        ('T', _('Text')),
        ]
    question_type = models.CharField(
        max_length=1, choices=CHOICES, default="T")
    required = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s' % (self.title, )

    class Meta:
        ordering = ('form', 'position', )

    def get_absolute_url(self):
        return reverse('customforms.views.view_form', args=[str(self.form.id)])


class Choice(models.Model):
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=200,)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('position', )

    def __unicode__(self):
        return u'%s' % (self.title, )

    def __repr__(self):
        return u'%s' % (self.title, )
