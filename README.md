[![PyPI release](https://img.shields.io/pypi/v/efb-notice-middleware.svg)](https://pypi.org/project/efb-notice-middleware/)
[![Downloads](https://pepy.tech/badge/efb-notice-middleware/month)](https://pypi.org/project/efb-notice-middleware/)

# NoticeMiddleware: A middleware for EFB 

## Notice

**Middleware ID**: `notice.NoticeMiddleware`

**NoticeMiddleware** is a middleware for EFB, to notice by @ in muted telegram group.  

Be aware that this is a very early develop version. Please let me know if you found any problem.

You need to use **NoticeMiddleware** on top of [EFB](https://ehforwarderbot.readthedocs.io). Please check the document and install EFB first.

## Dependense

* Python >=3.6
* EFB >=2.0.0
* PyYaml

## Install

* Install

```bash
pip3 install efb-notice-middleware
```

* Register to EFB
Following [this document](https://ehforwarderbot.readthedocs.io/en/latest/getting-started.html) to edit the config file. The config file by default is `~/.ehforwarderbot/profiles/default`. It should look like:

```yaml
master_channel: foo.demo_master
slave_channels:
- foo.demo_slave
- bar.dummy
middlewares:
- foo.other_middlewares
- notice.NoticeMiddleware
```

You only need to add the last line to your config file.

* Restart EFB.

## Usage

Create config file `config.yaml` in `~/.ehforwarderbot/profiles/default/notice.NoticeMiddleware`

```yaml
notices:
- 取件通知
- 超期提醒
- 取出通知
- 取件成功通知

tags:
- 取件通知
- 超期提醒:取件通知
```
