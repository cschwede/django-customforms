#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response

from customforms.forms import DynamicForm


def view_form(request, formid):
    form = DynamicForm(formid)
    if request.method == 'POST':
        form = DynamicForm(formid, request.POST)
        if form.is_valid():
            return render_to_response(
                'sample_form.html', {'data': form.cleaned_data})

    return render_to_response('sample_form.html', {
        'form': form,
        }, context_instance=RequestContext(request))
