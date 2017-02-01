
def from_service(service, always_pull=None, image=None):
    config = service['launchConfig']

    if 'labels' not in config:
        config['labels'] = {}

    if always_pull:
        config['labels']['io.rancher.container.pull_image'] = 'always'

    if image:
        config['imageUuid'] = "docker:" + image

    return config
