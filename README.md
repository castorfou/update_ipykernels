# update_ipykernels

using [Urwid](http://urwid.org/)


Create an interactive command application which proposes

2 panels :

- on left : list conda environnement (a nice way to display `conda env list`) (informative)
- on right : jupyter kernels list (interactive)
  - display with checkboxes all environnement
  - auto-check the existing kernels (from `jupyter kernelspec list`)
  - when I check, it creates the kernel (`python -m ipykernel install --user --name=<kernel_name>`)
  - when I uncheck, it removes the kernel (`jupyter kernelspec remove <kernel_name>`)

And Ctrl-C or 'q' to quit



# Turn update_ipykernels into an app

```bash
#from base environment
pip install pyinstaller urwid
pyinstaller update_ipykernels.py --onefile --collect-all urwid
pip uninstall pyinstaller urwid

#or directly from cli environment
pyinstaller update_ipykernels.py --onefile --collect-all urwid

#then
mkdir ~/Applications/update_ipykernels/
cp dist/update_ipykernels ~/Applications/update_ipykernels/
# and add ~/Applications/update_ipykernels/ in PATH
```

and then we can run `update_ipykernels`

