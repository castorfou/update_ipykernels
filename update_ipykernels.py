import subprocess
import urwid
from collections import OrderedDict


def get_conda_env(conda_environnement):
    '''
    retourne un tuple
    - dictionnaire avec comme key, les environnements et comme value le chemin
    - la key de l'environnement par défaut
    '''
    dict_envs = {}
    key_active_env = ''
    for num, ligne in enumerate(conda_environnement.splitlines()):
        ligne = ligne.strip()
        if (ligne != '\n') and (not ligne.startswith('#')) and (ligne != ''):
            ligne_splittee = ligne.split()
            dict_envs[ligne_splittee[0]] = ligne_splittee[-1]
            if (len(ligne_splittee)) > 2:
                key_active_env = ligne_splittee[0]
    return (OrderedDict(sorted(dict_envs.items())), key_active_env)


def get_jupyter_kernels(jupyterkernel_list):
    '''
    retourne un dictionnaire avec
    - key: le nom du kernelspec
    - value: le chemin
    '''
    dict_kernels = {}
    for num, ligne in enumerate(jupyterkernel_list.splitlines()):
        ligne = ligne.strip()
        if (ligne != '\n') and (not ligne.startswith('Available')) and (ligne != ''):
            ligne_splittee = ligne.split()
            dict_kernels[ligne_splittee[0]] = ligne_splittee[-1]
    return OrderedDict(sorted(dict_kernels.items()))


def get_consolidated_jupyter_kernels(dict_envs, dict_kernels):
    possible_kernels = {key: value for (key, value) in dict_envs.items(
    ) if key.lower() not in list(dict_kernels.keys())+['base']}

    # kernels_cumules =  {**dict_envs, **dict_kernels}
    return OrderedDict(sorted(possible_kernels.items()))


def get_all_env():
    '''retourne le text affiché par `conda env list`
    '''
    return subprocess.check_output("conda env list", shell=True, encoding='utf-8')


def get_installed_possible_kernels():
    dict_envs, main_env = get_conda_env(get_all_env())
    commands='''
    base_env=`conda info | grep -i 'base environment' | cut -d':' -f2| cut -d'(' -f1`
    base_env=`echo $base_env | sed 's/ *$//g'`
    source "$base_env"/etc/profile.d/conda.sh
    conda activate base
    jupyter kernelspec list |grep -i '.local'
    '''
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands.encode('utf-8'))
    dict_kernels = get_jupyter_kernels(out.decode('utf-8'))
    dict_possible = get_consolidated_jupyter_kernels(dict_envs, dict_kernels)
    return dict_kernels, dict_possible


def return_affichage_dict(diction):
    affichage = ''
    for (key, value) in diction.items():
        affichage += key+' - '+value+'\n'
    return affichage


def return_list_dict(diction):
    return return_affichage_dict(diction).split('\n')[:-1]


affichage_conda = get_all_env()
affichage_installed_kernels, affichage_potentiel_kernels = get_installed_possible_kernels()

# print(f'all condas\n{affichage_conda}')
# print(f'installed kernels \n{affichage_installed_kernels}')
# print(f'potentiel kernels \n{affichage_potentiel_kernels}')

actions_installation=[]
actions_desinstallation=[]
message=''

def main():

    def update_actions_lists(checkbox, state, value):
        if (state):
            actions_installation.append(value)
        else:
            actions_desinstallation.append(value)
    
    def apply_actions_before_exit():
        global message
        for env in actions_installation:
            commands='''\
            base_env=`conda info | grep -i 'base environment' | cut -d':' -f2| cut -d'(' -f1`
            base_env=`echo $base_env | sed 's/ *$//g'`
            source "$base_env"/etc/profile.d/conda.sh
            conda activate base
            python -m ipykernel install --user --name={env}\
            '''.format(env=env)
            process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
            out, err = process.communicate(commands.encode('utf-8'))

            # process = subprocess.Popen(['jupyter', 'kernelspec', 'remove', env],
            #          stdout=subprocess.PIPE, 
            #          stderr=subprocess.PIPE)
            # stdout, stderr = process.communicate() 
            if (out is not None):
                message+=out.decode("utf-8") 
            if (err is not None):
                message+=err.decode("utf-8") 

        for env in actions_desinstallation:

            commands='''\
            base_env=`conda info | grep -i 'base environment' | cut -d':' -f2| cut -d'(' -f1`
            base_env=`echo $base_env | sed 's/ *$//g'`
            source "$base_env"/etc/profile.d/conda.sh
            conda activate base
            jupyter kernelspec remove -f {env}\
            '''.format(env=env)
            process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
            out, err = process.communicate(commands.encode('utf-8'))

            # process = subprocess.Popen(['jupyter', 'kernelspec', 'remove', env],
            #          stdout=subprocess.PIPE, 
            #          stderr=subprocess.PIPE)
            # stdout, stderr = process.communicate() 
            if (out is not None):
                message+=out.decode("utf-8") 
            if (err is not None):
                message+=err.decode("utf-8") 

    def action_on_keypress(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if key in ('a', 'A'):
            apply_actions_before_exit()

    conda_env = urwid.Text(affichage_conda, align='left')
    jupyter_installed_kernels = urwid.Text(
        return_affichage_dict(affichage_installed_kernels), align='left')
    jupyter_installed_kernels = urwid.Padding(urwid.Pile(
        [urwid.AttrWrap(urwid.CheckBox(txt, True, on_state_change=update_actions_lists, user_data=txt.split()[0]), 'buttn', 'buttnf')
         for txt in return_list_dict(affichage_installed_kernels)]),
        left=4, right=3, min_width=10)

    jupyter_potentiel_kernels = urwid.Text(
        return_affichage_dict(affichage_potentiel_kernels), align='left')
    jupyter_potentiel_kernels = urwid.Padding(urwid.Pile(
        [urwid.AttrWrap(urwid.CheckBox(txt, False, on_state_change=update_actions_lists, user_data=txt.split()[0]), 'buttn', 'buttnf')
         for txt in return_list_dict(affichage_potentiel_kernels)]),
        left=4, right=3, min_width=10)
    blank = urwid.Divider()
    jupyter_env = urwid.Pile([urwid.Text('Jupyter kernels - installables', align='left'), blank, jupyter_potentiel_kernels, blank,blank,
                             urwid.Text('Jupyter kernels - installés', align='left'), blank, jupyter_installed_kernels])
    colonnes = urwid.Columns([conda_env, jupyter_env])
    listbox_content = [
        blank,
        urwid.AttrWrap(colonnes, 'bright'),
    ]

    header = urwid.AttrWrap(urwid.Text(
        "Gestion des environnements conda, 'q' pour sortir, 'a' pour appliquer"), 'header')
    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)

    palette = [
        ('body', 'black', 'black', 'standout'),
        ('header', 'white', 'dark red', 'bold'),
    ]
    urwid.MainLoop(frame, palette, unhandled_input=action_on_keypress).run()


if __name__ == '__main__':
    main()
    print(f'à desinstaller - {actions_desinstallation}')
    print(f'à installer - {actions_installation}')
    print(f'{message}')
