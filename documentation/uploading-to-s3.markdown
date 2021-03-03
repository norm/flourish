# Uploading your site to Amazon S3

Flourish can upload your generated site to Amazon's S3 service. This can be
used simply to keep a backup, or to host your website.

After [signing up][aws] to Amazon Web Services, and [setting up your
credentials][creds] for using the AWS Command Line Interface, you can
upload your website to S3 with one command:

```bash
flourish upload <bucketname>
```

Or, if you prefer, you can keep the bucket name in the
[site configuration](/site-configuration) like so:

```python
bucket = "<bucketname>"
```

then you need only run:

```bash
flourish upload
```

If you have put the S3 bucket behind a CloudFront distribution, you can
issue a targetted invalidation when new files are uploaded:

```bash
flourish upload --invalidate <bucketname> <cloudfront ID>
```

Again, you can keep the bucket and distribution ID in the site configuration:

```python
bucket = "<bucketname>"
cloudfront_id = "<cloudfront ID>"
```

and then you need only run:

```bash
flourish upload --invalidate
```


[aws]: https://aws.amazon.com
[creds]: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html