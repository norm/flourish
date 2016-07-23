[TOC]

# Flourish API: `flourish.paginator`

On pages which have been [paginated](/api-flourish-generators-paginatedindex/),
Flourish provides the template context with a `Paginator` object.

## Paginator methods

  * `paginator.count` — the number of objects (not pages) that were paginated
  * `paginator.num_pages` — the number of pages in this paginated collection,
    as a single integer
  * `paginator.page_range` — the pages in this paginated collection, as a
    list (eg. [1, 2, 3])
  * `paginator.page` — returns a [`Page`](#page) object representing a single
    page of this paginated collection
  * `paginator.pages` — returns a list of [`Page`](#page) objects, one for
    each page of this paginated collection

## Page methods

  * `page.has_next` — `True` if there is a page after this one in the
    collection, otherwise `False`
  * `page.next_page_number` — the number of the next page in the collection
  * `page.has_previous` — `True` if there is a page before this one in the
    collection, otherwise `False`
  * `page.previous_page_number` — the number of the previous page in the
    collection
  * `page.has_other_pages` — `True` if there is more than one page in this
    collection
  * `start_index` — the index within the entire paginated collection of the
    first item in this page (eg. with 10 items per page, the third page
    would have a `start_index` of 21)
  * `end_index` — the index within the entire paginated collection of the
    last item in this page (eg. with 10 items per page, the third page
    would have an `end_index` of 30)
  * `url` — the URL of this page, made by appending `page-N` to the base URL
    of the entire collection
