#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin

from customforms.models import Form, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    fields = ('title', 'position', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('form', 'title', 'position')
    list_filter = ('form', )
    inlines = [ChoiceInline]
    save_on_top = True
    fields = ('title', 'form', 'help_text', 'question_type', 'required')


class FormAdmin(admin.ModelAdmin):
    list_display = ('title', )


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
