import subprocess
from collections import OrderedDict

def get_conda_env(conda_environnement):
    '''
    retourne un tuple 
    - dictionnaire avec comme key, les environnements et comme value le chemin
    - la key de l'environnement par défaut
    '''
    dict_envs={}
    key_active_env=''
    for num, ligne in enumerate(conda_environnement.splitlines()):
        ligne = ligne.strip()
        if (ligne != '\n') and (not ligne.startswith('#')) and (ligne != ''):
            ligne_splittee = ligne.split()
            dict_envs[ligne_splittee[0]]=ligne_splittee[-1]
            if (len(ligne_splittee))>2:
                key_active_env = ligne_splittee[0]
    return (OrderedDict(sorted(dict_envs.items())), key_active_env)

def get_jupyter_kernels(jupyterkernel_list):
    '''
    retourne un dictionnaire avec
    - key: le nom du kernelspec
    - value: le chemin
    '''
    dict_kernels={}
    for num, ligne in enumerate(jupyterkernel_list.splitlines()):
        ligne = ligne.strip()
        if (ligne != '\n') and (not ligne.startswith('Available')) and (ligne != ''):
            ligne_splittee = ligne.split()
            dict_kernels[ligne_splittee[0]]=ligne_splittee[-1]
    return OrderedDict(sorted(dict_kernels.items()))

def get_consolidated_jupyter_kernels(dict_envs, dict_kernels):
    possible_kernels = {key:value for (key,value) in dict_envs.items() if key.lower() not in list(dict_kernels.keys())+['base']}

    # kernels_cumules =  {**dict_envs, **dict_kernels}
    return OrderedDict(sorted(possible_kernels.items()))

def get_all_env():
    '''retourne le text affiché par `conda env list`
    '''
    return subprocess.check_output("conda env list", shell=True, encoding='utf-8')

def get_installed_possible_kernels():
    dict_envs, main_env = get_conda_env(get_all_env())
    dict_kernels = get_jupyter_kernels(subprocess.check_output("jupyter kernelspec list", shell=True, encoding='utf-8'))
    dict_possible = get_consolidated_jupyter_kernels(dict_envs, dict_kernels)
    return dict_kernels, dict_possible

affichage_conda = get_all_env()
affichage_installed_kernels, affichage_potentiel_kernels = get_installed_possible_kernels()

print(f'all condas\n{affichage_conda}')
print(f'installed kernels \n{affichage_installed_kernels}')
print(f'potentiel kernels \n{affichage_potentiel_kernels}')
