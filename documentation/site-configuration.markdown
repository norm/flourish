# The site configuration file

If a file called `_site.toml` exists in the source directory, the values 
in it are made available in all templates. For example, if it contains:

```python
name = "Wendy's Blog"
by = 'Wendy Testaburger'
```

then templates can use `site.by` to get "Wendy Testaburger",
and `site.name` to get "Wendy's Blog". This makes templates more reusable
across different websites.

This file does not have to exist, and there are no required entries in this
file — unless you are using [Atom feeds](/atom-feeds/).
