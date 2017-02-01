#!/usr/bin/env python

import click
from rancher.config import Config
from rancher.api import Api

config = Config()
api = Api(config)

# tagged echo helper
def techo(tag, message):
    click.secho("[%s]" % tag, bold=True, nl=False)
    click.echo(" %s" % message)

def before(ctx):
    if ctx.obj['show_config']:
        techo('config', "RANCHER_URL: %s" % config.RANCHER_URL)
        techo('config', "RANCHER_ACCESS_KEY: %s" % config.RANCHER_ACCESS_KEY)
        techo('config', "RANCHER_SECRET_KEY: ***")

@click.group()
@click.pass_context
@click.option('--show-config', is_flag=True, default=True, help='Print Rancher config to stdout?')
def main(ctx, show_config):
    ctx.obj['show_config'] = show_config

@main.command()
@click.pass_context
@click.argument('service-fullname')
def upgrade(ctx, service_fullname):
    before(ctx)

    service = api.get_service_by_fullname(service_fullname)
    service_id = service['id']
    launch_config = service['launchConfig']

    if service['state'] == 'upgraded':
        techo(service_fullname, "service is already upgraded, confirming...")
        api.service_confirm(service_id)

        techo(service_fullname, "waiting for service to active...")
        api.service_wait_state(service_id, 'active')

    techo(service_fullname, "upgrading service...")
    upgrade = api.service_upgrade(service_id, launch_config)

if __name__ == '__main__':
    main(obj={})
