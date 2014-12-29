#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from django import forms


class DynamicForm(forms.BaseForm):
    def __init__(self, questions, *args, **kwargs):
        fields = OrderedDict()
        for question in questions:
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
