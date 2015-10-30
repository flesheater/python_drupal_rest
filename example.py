#! /usr/bin/python

from drupal import DrupalRest

d = DrupalRest('http://localhost/drupal_sandbox/', 'rest/', 'admin', 'admin')
d.drupalLogin()


#node = d.retrieveNode(69)
#print node['title']


#new_node_array = {'title': 'testtest', 'type': 'article'}
#new_node = d.createNode(new_node_array)

#print new_node

base64 = open('cat.jpg').read(10000).encode('base64')
file_cat = {'filename': 'cat.jpg', 'file': base64}

file = d.createFile(file_cat)

#print file
