# ranchup

simple rancher command line utilities

## requirements

* python version: 3 (tested on 3.5.2)
* environment variables (can be put in `.env` file):
  * `RANCHER_URL`
  * `RANCHER_ACCESS_KEY`
  * `RANCHER_SECRET_KEY`

## howto

```sh
pip install requirements.txt
./rancherup.py --help
./rancherup.py upgrade stack_name/service_name
```
