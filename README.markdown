flourish
========

A static site generator, built around two basic premises:

1.  **Many small commands composed together is better than one big one**

    Whilst it is tempting to create a tool that builds sites the way I want,
    there is a reason I don't like jekyll, hyde, hugo, et al. They are one
    program that works in a certain way. 

    I prefer the Unix idea of tools that do one thing well, and I
    think that "turn Markdown into HTML" is an example of One Thing,
    not "turn Markdown into a website".

    There should be a command to extract partial HTML from the original
    content (be it Markdown or something else).  There should be a second
    command to build a page from a template given this partial content. 
    There should be a different command to build index pages using summaries.
    And so on.

2.  **Make already exists**

    Unix has had a tool to rebuild files based on changed dependencies for 
    decades. I shouldn't need to recreate that in my code.


How a build will work
---------------------

1.  Scan the content source directory, building up a list of all content
    and its metadata. Use this to create a Makefile include that describes
    the dependencies, and a file of all site metadata.

2.  Create partials from all source in whatever forms are declared (eg
    post summaries, image thumbnails, etc).

3.  Create pages from partials.

Steps 2 and 3 are done by Make so rebuilds should only regenerate the pages
affected when content changes or is added. And we can use Make's ability to
run things in parallel.
