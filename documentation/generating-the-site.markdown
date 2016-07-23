# Generating the site

To generate your Flourish website, use the `flourish` command line tool:

  * `flourish generate` — to generate the site
  * `flourish preview` — to preview the generated site
  * `flourish --rebuild preview` — to preview the site, regenerating it as you
    change things

However, unlike some static site generators, Flourish will not generate any
output without being told explicitly what to do.

To start generating output, first you need to create a file `generate.py`
within your source directory, which is python source code that the `flourish`
command line script reads. Start the file with:

```python
from flourish.generators import (
    IndexGenerator,
    PageGenerator,
)
```

This file then needs [some URLs added](/adding-urls/), and these will need
code that says how to [generate the HTML](/generating-html/).
