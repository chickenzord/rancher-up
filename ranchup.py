#!/usr/bin/env python

import click
from rancher.config import Config
from rancher.api import Api

# tagged echo helper
def techo(tag, message):
    click.secho("[%s]" % tag, bold=True, nl=False)
    click.echo(" %s" % message)

def before(ctx):
    config = ctx.obj['config']
    if ctx.obj['show_config'] or config.not_valid():
        techo('config', "RANCHER_URL: %s" % config.RANCHER_URL)
        techo('config', "RANCHER_ACCESS_KEY: %s" % config.RANCHER_ACCESS_KEY)
        techo('config', "RANCHER_SECRET_KEY: ***")

    if config.not_valid():
        raise Exception("Invalid config")

@click.group()
@click.pass_context
@click.option('--env-file', type=click.Path(exists=True), help='Alternate env file to load')
@click.option('--show-config', is_flag=True, default=True, help='Print Rancher config to stdout')
def main(ctx, env_file, show_config):
    if env_file:
        ctx.obj['config'] = Config(env_file=env_file)
    else:
        ctx.obj['config'] = Config()

    ctx.obj['show_config'] = show_config

@main.command()
@click.pass_context
@click.argument('service-fullname')
@click.option('--always-pull', is_flag=True, default=False, help="Always pull before upgrade")
@click.option('--image', type=str, help="Change docker image")
@click.option('--wait/--no-wait', default=False, help="Wait upgrade to finish before exit")
def upgrade(ctx, service_fullname, always_pull, image, wait):
    before(ctx)

    api = Api(ctx.obj['config'])

    service = api.get_service_by_fullname(service_fullname)
    service_id = service['id']

    if service['state'] == 'upgraded':
        techo(service_fullname, "service is already upgraded, confirming...")
        api.service_confirm(service_id)

        techo(service_fullname, "waiting for service to active...")
        api.service_wait_state(service_id, 'active')

    from rancher.launch_config import from_service
    if image is None: always_pull = True # no image implies re-pull
    launch_config = from_service(service, always_pull=always_pull, image=image)

    techo(service_fullname, "upgrading service using image '%s'..." % launch_config['imageUuid'])
    upgrade = api.service_upgrade(service_id, launch_config)

    if wait:
        techo(service_fullname, "waiting for upgrade to finish...")
        api.service_wait_state(service_id, 'upgraded')
        techo(service_fullname, "upgrade finished")

if __name__ == '__main__':
    main(obj={})
