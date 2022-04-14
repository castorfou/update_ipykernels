# update_ipykernels

using [PyInquirer](https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df#PyInquirer)

or [Blessed](https://pypi.org/project/blessed/)

or [Urwid](http://urwid.org/)


Create an interactive command application which proposes

2 panels :

- on left : list conda environnement (a nice way to display `conda env list`) (informative)
- on right : jupyter kernels list (interactive)
  - display with checkboxes all environnement
  - auto-check the existing kernels (from `jupyter kernelspec list`)
  - when I check, it creates the kernel (`python -m ipykernel install --user --name=<kernel_name>`)
  - when I uncheck, it removes the kernel (`jupyter kernelspec remove <kernel_name>`)

And Ctrl-C or 'q' to quit