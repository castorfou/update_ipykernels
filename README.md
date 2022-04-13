# update_ipykernels

using [PyInquirer](https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df#PyInquirer)



Create an interactive command application which proposes



2 options :

- list conda environnement (a nice way to display `conda env list`)
- update jupyter kernels list 
  - display with checkboxes all environnement
  - auto-check the existing kernels (from `jupyter kernelspec list`)
  - when I check, it creates the kernel (`python -m ipykernel install --user --name=<kernel_name>`)
  - when I uncheck, it removes the kernel (`jupyter kernelspec remove <kernel_name>`)

And Ctrl-C to quit