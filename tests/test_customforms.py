""" Tests for customforms """
from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.test import TestCase

from customforms.models import Form, Question, Choice
from customforms.forms import DynamicForm


class DynamicFormTests(TestCase):
    """ Tests for customforms """

    def test_form(self):
        """ Test form with questions and choices """

        form = Form.objects.create(id=1, title='Sample Form')

        question = Question.objects.create(
            title='Question', question_type='S', form=form, position=0)

        Choice.objects.create(title='Yes', question=question, position=0)
        Choice.objects.create(title='No', question=question, position=1)

        form = DynamicForm(1)
        self.assertFalse(form.is_valid())

        form_data = {'1': '1'}
        form = DynamicForm(1, data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('Question'), 'Yes')
        self.assertEqual(form.errors, {})
        self.assertTrue(isinstance(form.extended_cleaned_data[0][0], Question))
        self.assertTrue(isinstance(form.extended_cleaned_data[0][1], Choice))

        form_data = {'1': '2'}
        form = DynamicForm(1, data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('Question'), 'No')
        self.assertEqual(form.errors, {})
        self.assertTrue(isinstance(form.extended_cleaned_data[0][0], Question))
        self.assertTrue(isinstance(form.extended_cleaned_data[0][1], Choice))

        form_data = {'1': '3'}
        form = DynamicForm(1, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('1' in form._errors)
        self.assertEqual(
            OrderedDict([(u'Question', u'None')]), form.cleaned_data)

    def test_view(self):
        form = Form.objects.create(id=1, title='Sample Form')

        question = Question.objects.create(
            title='Question', question_type='C', form=form, position=0)

        Choice.objects.create(title='Yes', question=question, position=0)
        Choice.objects.create(title='No', question=question, position=1)

        url = reverse('customforms.views.view_form', kwargs={'formid': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {'1': ['1', '2']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderedDict([(u'Question', u'[Yes, No]')]),
                         response.context.get('data'))
