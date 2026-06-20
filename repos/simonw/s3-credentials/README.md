# s3-credentials

[![PyPI](https://img.shields.io/pypi/v/s3-credentials.svg)](https://pypi.org/project/s3-credentials/)
[![Changelog](https://img.shields.io/github/v/release/simonw/s3-credentials?include_prereleases&label=changelog)](https://github.com/simonw/s3-credentials/releases)
[![Tests](https://github.com/simonw/s3-credentials/workflows/Test/badge.svg)](https://github.com/simonw/s3-credentials/actions?query=workflow%3ATest)
[![Documentation Status](https://readthedocs.org/projects/s3-credentials/badge/?version=latest)](https://s3-credentials.readthedocs.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/s3-credentials/blob/master/LICENSE)

A tool for creating credentials for accessing S3 buckets

For project background, see [s3-credentials: a tool for creating credentials for S3 buckets](https://simonwillison.net/2021/Nov/3/s3-credentials/) on my blog.

## Installation

    pip install s3-credentials

## Basic usage

To create a new S3 bucket and output credentials that can be used with only that bucket:
```
% s3-credentials create my-new-s3-bucket --create-bucket
Created bucket:  my-new-s3-bucket
Created user: s3.read-write.my-new-s3-bucket with permissions boundary: arn:aws:iam::aws:policy/AmazonS3FullAccess
Attached policy s3.read-write.my-new-s3-bucket to user s3.read-write.my-new-s3-bucket
Created access key for user: s3.read-write.my-new-s3-bucket
{
    "UserName": "s3.read-write.my-new-s3-bucket",
    "AccessKeyId": "AKIAWXFXAIOZOYLZAEW5",
    "Status": "Active",
    "SecretAccessKey": "...",
    "CreateDate": "2021-11-03 01:38:24+00:00"
}
```
The tool can do a lot more than this. See the [documentation](https://s3-credentials.readthedocs.io/) for details.

## Documentation

- [Full documentation](https://s3-credentials.readthedocs.io/)
- [Command help reference](https://s3-credentials.readthedocs.io/en/stable/help.html)
- [Release notes](https://github.com/simonw/s3-credentials/releases)
