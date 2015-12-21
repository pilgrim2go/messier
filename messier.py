#!/usr/bin/env python
"""Messier.

Usage:
  messier.py <command> [--provider <provider>] [<vms> ...]

Examples:
  messier.py create server
  messier.py converge
  messier.py verify
  messier.py test
  messier.py list
  messier.py (-h | --help)
  messier.py --version

Options:
  -h --help                Show this screen.
  --provider PROVIDER      Backend provider [default: virtualbox].
  --wait <seconds>         Time to sleep after destroying [default: 10].
  --pristine               Destroy VMs prior to run.
  --reboot                 Reboot hosts prior to running Serverspec tests.

"""
from docopt import docopt

# command line options: test, provision, destroy, etc
# in general, Vagrant commands should be honored. Depend on Vagrant
# to manage provisioning regardless of backend. Greatly simplifies scope
# of `messier`.

import vagrant
import subprocess


v = vagrant.Vagrant(quiet_stdout=False)


def available_vms(args):
    wanted_vms = [vm for vm in v.status()]
    if args['<vms>']:
        wanted_vms = [vm for vm in wanted_vms if vm in args['<vms>']]
    return wanted_vms


def provision_vms(args):
    for vm in args['vms']:
        v.provision(vm_name=vm.name)


def reload_vms(args):
    for vm in args['vms']:
        v.reload(vm_name=vm.name)


def destroy_vms(args):
    for vm in args['vms']:
        v.destroy(vm_name=vm.name)


def create_vms(args):
    for vm in args['vms']:
        v.up(vm_name=vm.name, provider=args['--provider'], no_provision=True)


def verify_vms(args):
    subprocess.call(["bundle", "exec", "rake", "serverspec:default"])


if __name__ == "__main__":
    args = docopt(__doc__, version='0.1')
    print(args)

    args['vms'] = available_vms(args)

    if args['<command>'] == 'create':
        create_vms(args)

    elif args['<command>'] == 'destroy':
        destroy_vms(args)

    elif args['<command>'] == 'verify':
        verify_vms(args)

    elif args['<command>'] == 'test':
        destroy_vms(args)
        create_vms(args)
        provision_vms(args)
        reload_vms(args)
        verify_vms(args)

