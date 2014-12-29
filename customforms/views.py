#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from customforms.models import Form, Question
from customforms.forms import DynamicForm


def view_form(request, formid):
    db_form = Form.objects.get(id=formid)
    questions = db_form.question_set.all()
    form = DynamicForm(questions)

    if request.method == 'POST':
        form = DynamicForm(questions, request.POST)
        if form.is_valid():
            data = {}
            for question_id, answer in form.cleaned_data.items():
                question = Question.objects.get(id=question_id)
                data[question.title] = answer.title
            return HttpResponse(str(data))

    return render_to_response('sample_form.html', {
        'form': form,
        }, context_instance=RequestContext(request))
