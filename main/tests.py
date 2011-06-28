"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.utils.functional import curry
from django.test import TestCase
from django.forms.formsets import formset_factory


from main.models import Role
from main.forms import ErrorForm, UIDCompleteForm


class RoleTreeTest(TestCase):
    def setUp(self):
        #create_base_tree()
        ## Use initial_data.json for setup instead
        pass

    def test_base(self):
        # Getting the root persons
        head = Role.tree.root_nodes()
        head[0].get_descendants()
        # Find out the leaf nodes of the tree
        leaf_nodes = head[0].get_leafnodes()
        self.assertEqual(leaf_nodes.count(), 5)

class UIDCompleteFormTest(TestCase):
    def setUp(self):
        self.role = Role.objects.get(user__username='test')

    def test_empty_form(self):
        form = UIDCompleteForm(self.role)
        self.assertEqual(not not form, True)

    def test_form_valiadtion(self):
        uid_id = 4
        data = {
            'completer': 4,
            'uid': uid_id,
            'child_age': 2,
        }
        form = UIDCompleteForm(self.role, data)
        self.assertEqual(form.is_valid(), True)
        uid = form.save()

        self.assertEqual(uid_id, uid.id)
        self.assertEqual(uid.uidquestion_set.count(), 1)

    def test_formset(self):
        UIDCompleteFormset = formset_factory(UIDCompleteForm, extra=2)
        UIDCompleteFormset.form = staticmethod(curry(UIDCompleteForm, self.role))
        formset = UIDCompleteFormset()
        for form in formset.forms:
            print form

class ErrorTest(TestCase):
    def test_error_form(self):
        role = Role.objects.get(pk=1)
        f = ErrorForm(role, {'etype':1, 'uid_status':1})
        # Wrong uid_status
        self.assertEqual(f.is_valid(), False)
        # Wrong error type
        f = ErrorForm(role, {'etype':1, 'uid_status':3})
        self.assertEqual(f.is_valid(), False)
