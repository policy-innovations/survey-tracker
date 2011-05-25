"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from main.models import Role


class RoleTreeTest(TestCase):
    def setUp(self):
        #create_base_tree()
        ## Use initial_data.json for setup instead
        pass

    def test_base(self):
        #Getting the root persons
        head = Role.tree.root_nodes()
        subs = head[0].get_descendants()
        ##Find out the leaf nodes of the tree
        leaf_nodes = head[0].get_leafnodes()
        print leaf_nodes
        self.assertEqual(leaf_nodes.count(), 7)
