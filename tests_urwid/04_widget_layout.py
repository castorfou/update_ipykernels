import urwid


def main():

    def unhandled(key):
        if key in ['q', 'Q']:
            raise urwid.ExitMainLoop()

    conda_env = urwid.Text('conda envs seront ici', align='left')
    jupyter_kernels = urwid.Text('jupyter kernels seront ici', align='left')
    colonnes = urwid.Columns([conda_env, jupyter_kernels])
    blank = urwid.Divider()
    listbox_content = [
        blank,
        urwid.AttrWrap(colonnes, 'bright'),
        ]

    header = urwid.AttrWrap(urwid.Text("Gestion des environnements conda, 'q' pour sortir"), 'header')
    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)

    palette = [
        ('body','black','light gray', 'standout'),
        ('reverse','light gray','black'),q
        ('header','white','dark red', 'bold'),
        ('important','dark blue','light gray',('standout','underline')),
        ('editfc','white', 'dark blue', 'bold'),
        ('editbx','light gray', 'dark blue'),
        ('editcp','black','light gray', 'standout'),
        ('bright','dark gray','light gray', ('bold','standout')),
        ('buttn','black','dark cyan'),
        ('buttnf','white','dark blue','bold'),
        ]


    urwid.MainLoop(frame, palette, unhandled_input=unhandled).run()

if __name__ == '__main__':
    main()
