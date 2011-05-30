"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from main.models import Role, ErrorType, Project, UIDStatus
from main.forms import ErrorForm


class RoleTreeTest(TestCase):
    def setUp(self):
        #create_base_tree()
        ## Use initial_data.json for setup instead
        pass

    def test_base(self):
        # Getting the root persons
        head = Role.tree.root_nodes()
        subs = head[0].get_descendants()
        # Find out the leaf nodes of the tree
        leaf_nodes = head[0].get_leafnodes()
        self.assertEqual(leaf_nodes.count(), 5)

class ErrorTest(TestCase):
    def test_error_form(self):
        role = Role.objects.get(pk=1)
        f = ErrorForm(role, {'etype':1, 'uid_status':1})
        # Wrong uid_status
        self.assertEqual(f.is_valid(), False)
        # Wrong error type
        f = ErrorForm(role, {'etype':1, 'uid_status':3})
        self.assertEqual(f.is_valid(), False)
        f = ErrorForm(role, {'etype':3, 'uid_status':3})
        self.assertEqual(f.is_valid(), True)
