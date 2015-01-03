""" Tests for customforms """
from django.core.urlresolvers import reverse
from django.test import TestCase

from customforms.models import Form, Question, Choice
from customforms.forms import DynamicForm


class DynamicFormTests(TestCase):
    """ Tests for customforms """

    def test_form(self):
        """ Test form with questions and choices """

        form = Form.objects.create(id=1, title='Sample Form')

        question = Question.objects.create(title='Question',
                                     question_type='S',
                                     form=form,
                                     position=0)

        choice1 = Choice.objects.create(title='Yes', question=question, position=0)
        choice2 = Choice.objects.create(title='No', question=question, position=1)

        form = DynamicForm([question, ])
        self.assertFalse(form.is_valid())

        form_data = {'1': '1'}
        form = DynamicForm([question, ], data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get(str(question.id)), choice1)
        self.assertEqual(form.errors, {})

        form_data = {'1': '2'}
        form = DynamicForm([question, ], data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get(str(question.id)), choice2)
        self.assertEqual(form.errors, {})

        form_data = {'1': '3'}
        form = DynamicForm([question, ], data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form._errors.has_key('1'))
        self.assertEqual(form.cleaned_data, {})

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
        self.assertEqual("{u'Question': u'[Yes, No]'}", response.content)
