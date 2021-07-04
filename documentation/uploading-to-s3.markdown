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

## CloudFront invalidations

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

The `--max-invalidations` option controls how many paths are requested to be
invalidated, as more than 1,000 paths across an account in a month starts to
be charged.

```bash
flourish upload --invalidate --max-invalidations 50
```

The default is 100 paths. If more than the maximum paths need to
be invalidated, multiple paths with a common root will be invalidated as a
whole. Multiple paths such as `/tags/a`, `/tags/b`, etc would result in
`/tags/*` being invalidated, which may result in unchanged paths being
invalidated. In most low- to medium-traffic sites, the cost of invalidating
thousands of paths is more than content having to be recached from S3.


[aws]: https://aws.amazon.com
[creds]: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html