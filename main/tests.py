"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from main.models import Person

def create_base_tree():
    superhead = Person.objects.create(name='A')
    s1 = Person.objects.create(name='B', head=superhead)
    s2 = Person.objects.create(name='C', head=superhead)
    ss1 = Person.objects.create(name='D', head=s1)
    ss2 = Person.objects.create(name='E', head=s1)
    ss3 = Person.objects.create(name='F', head=s1)
    ss4 = Person.objects.create(name='G', head=s2)
    sss1 = Person.objects.create(name='H', head=ss1)
    sss2 = Person.objects.create(name='I', head=ss3)
    sss3 = Person.objects.create(name='J', head=ss4)
    sss4 = Person.objects.create(name='K', head=ss4)

class PersonTreeTest(TestCase):
    def setUp(self):
        #create_base_tree()
        ## Use initial_data.json for setup instead
        pass

    def test_base(self):
        #Getting the root persons
        head = Person.tree.root_nodes()
        subs = head[0].get_descendants()
        ##Find out the leaf nodes of the tree
        leaf_nodes = head[0].get_leafnodes()
        print leaf_nodes
        self.assertEqual(leaf_nodes.count(), 7)
