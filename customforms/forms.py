#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from django import forms

from customforms.models import Form


class DynamicForm(forms.BaseForm):
    def __init__(self, formid, *args, **kwargs):
        db_form = Form.objects.get(id=formid)
        self.questions = db_form.question_set.all()
        fields = OrderedDict()
        for question in self.questions:
            fields[str(question.id)] = self._get_field(question)
        self.base_fields = fields
        super(DynamicForm, self).__init__(*args, **kwargs)

    def _get_field(self, question):
        default_kwargs = {
            'label': question.title,
            'required': question.required,
            'help_text': question.help_text
        }

        lookup = {
            'T': (forms.CharField, {}),

            'C': (forms.ModelMultipleChoiceField, {
                'queryset': question.choice_set.all(),
                'widget': forms.CheckboxSelectMultiple()}),

            'R': (forms.ModelChoiceField, {
                'queryset': question.choice_set.all(),
                'widget': forms.RadioSelect()}),

            'S': (forms.ModelChoiceField, {
                'queryset': question.choice_set.all()}),
            }

        formfield_class, optional_kwargs = lookup.get(question.question_type)
        kwargs = dict(default_kwargs.items() + optional_kwargs.items())
        return formfield_class(**kwargs)
