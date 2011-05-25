"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from main.models import Person

def create_base_tree():
    head = Person.objects.create(name='A')
    s1 = Person.objects.create(name='B', supervisor=head)
    s2 = Person.objects.create(name='C', supervisor=head)
    ss1 = Person.objects.create(name='D', supervisor=s1)
    ss2 = Person.objects.create(name='E', supervisor=s1)
    ss3 = Person.objects.create(name='F', supervisor=s1)
    ss4 = Person.objects.create(name='G', supervisor=s2)
    sss1 = Person.objects.create(name='H', supervisor=ss1)
    sss2 = Person.objects.create(name='I', supervisor=ss3)
    sss3 = Person.objects.create(name='J', supervisor=ss4)
    sss4 = Person.objects.create(name='K', supervisor=ss4)

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
        #lowest_children = subs.objects.filter()
        self.assertEqual(subs.count(), 10)
