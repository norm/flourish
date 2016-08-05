# Adding assets to your site

Assets, such as images, CSS, and JavaScript, are also commonly known as
"static files". This means they don't change even if your HTML does. 

(In dynamically generated sites, calling these files "static" makes sense.
However, Flourish is a static site generator — meaning it creates websites
that do not change dependent on the users viewing the site. All files are
"static" in Flourish generated sites, so they are referred to as assets.)

When generating the site (eg running `flourish generate`), any files in
the source directory that aren't seen as [source files](/adding-sources/)
(ie. files that aren't TOML, JSON or Markdown sources or attachments)
are copied to the output directory without changing the filename, directory
the file is in, or the contents.

For example, a file `logo.png` in the source directory, would be output
to `logo.png` when the site is generated. Similarly, a file `css/screen.png`
would be output to `css/screen.png` when the site is generated.
