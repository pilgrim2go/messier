# -*- coding: utf-8 -*-
class AnsibleHandler(object):

    def __init__(self):
        pass


    def parse_playbook(self, args):
        playbook = open(args['--playbook'], 'r')
        y = yaml.load(playbook)
        return [play['name'] for play in y]


    def parse_messier_config(self, args):
        playbook = open(args['--playbook'], 'r')
        y = yaml.load(playbook)
        return [play['name'] for play in y]

