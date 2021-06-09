from importlib.resources import files

this = files('flourish.blueprint')
toolbar = this.joinpath('blueprint_toolbar.html').read_text()
template = this.joinpath('blueprint_template.html').read_text()
