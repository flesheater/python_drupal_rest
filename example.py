#! /usr/bin/python

from drupal import DrupalRest

d = DrupalRest('http://localhost/drupal_sandbox/', 'rest/', 'user', 'pass')
d.drupalLogin()
node = d.retrieveNode(66)
print node['title']
