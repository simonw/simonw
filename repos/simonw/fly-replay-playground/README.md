# fly-replay-playground

Example apps for experiments with the `fly-replay` header.

## The apps

This repo contains two apps, `replay-from` and `replay-to`. They are deployed here:

- https://replay-from.fly.dev
- https://replay-to.fly.dev

All hits to https://replay-from.fly.dev should return an invisible `fly-replay: app=reflay-to` header, which will cause the request to be replayed against the other instance.

Submitting the form on https://replay-from.fly.dev will show slightly different debug headers than if you submit it on https://replay-to.fly.dev - otherwise the two should appear identical.

## Deployment

To deploy, first run this if it has not been run before:
```bash
fly apps create replay-from
fly apps create replay-to
```
Optionally add `-o orgname` to create them in an organization.

Then run:
```bash
(cd replay-from && fly deploy)
(cd replay-to && fly deploy)
```
