# Generating the site

To generate your Flourish website, use the `flourish` command line tool:

  * `flourish generate` — to generate the entire site
  * `flourish generate [path ...]` — to generate only a part of the site,
    specify a path or paths. Appending a question mark `?` makes it a wildcard
    match to generate anything that starts with this path (eg. `/2020/?`).
  * `flourish preview` — to preview the generated site
  * `flourish preview --generate` — to preview the site, regenerating pages
    as you request them in your browser

Unlike some static site generators, Flourish will not generate any output
without being told explicitly what to generate. First you need to create a
file `generate.py` within your source directory, which is python source code
that the `flourish` command line script reads. Start the file with:

```python
from flourish.generators import (
    IndexGenerator,
    PageGenerator,
)
```

This file then needs [some URLs added](/adding-urls/), and these will need
code that says how to [generate the HTML](/generating-html/).
