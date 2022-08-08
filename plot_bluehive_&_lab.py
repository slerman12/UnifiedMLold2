# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import getpass
import os
from pathlib import Path
from cryptography.fernet import Fernet

from pexpect import spawn

import numpy as np

from Plot import plot

from sweeps_and_plots import runs


plot_group = 'UML_Paper'
plot_specs = runs[plot_group]['Classify+RL']

experiments = set().union(*plot_specs.plots)


# SFTP experiment results
if plot_specs.sftp:
    username = 'slerman'

    # Get password, encrypt, and save for reuse
    if os.path.exists('pass'):
        with open('pass', 'r') as file:
            key, encoded = file.readlines()
            password = Fernet(key).decrypt(bytes(encoded, 'utf-8'))
    else:
        password, key = getpass.getpass(), Fernet.generate_key()
        encoded = Fernet(key).encrypt(bytes(password, 'utf-8'))
        with open('pass', 'w') as file:
            file.writelines([key.decode('utf-8') + '\n', encoded.decode('utf-8')])

    conda = 'source /scratch/slerman/miniconda/bin/activate agi'

    cwd = os.getcwd()
    local_path = f"./Benchmarking"

    Path(local_path).mkdir(parents=True, exist_ok=True)
    os.chdir(local_path)

    if plot_specs.bluehive:
        # Connect VPN
        try:
            p = spawn('/opt/cisco/anyconnect/bin/vpn connect vpnconnect.rochester.edu')
            p.expect('Username: ')
            p.sendline('')
            p.expect('Password: ')
            p.sendline(password)
            p.expect('Second Password: ')
            p.sendline('push')
            p.expect('VPN>')
        except Exception:
            pass

        # SFTP

        print(f'SFTP\'ing: {", ".join(experiments)}')
        if len(plot_specs.tasks):
            print(f'plotting for tasks: {", ".join(plot_specs.tasks)}')
        if plot_specs.steps:
            print(f'up to steps: {plot_specs.steps:.0f}')

        print('\nConnecting to Bluehive', end=" ")
        p = spawn(f'sftp {username}@bluehive.circ.rochester.edu')
        p.expect('Password: ', timeout=None)
        p.sendline(password)
        p.expect('sftp> ', timeout=None)
        print('- Connected! ✓\n')
        p.sendline(f"lcd {local_path}")
        p.expect('sftp> ', timeout=None)
        p.sendline(f"cd /scratch/{username}/UnifiedML")
        p.expect('sftp> ', timeout=None)
        for i, experiment in enumerate(experiments):
            print(f'{i + 1}/{len(experiments)} [bluehive] SFTP\'ing "{experiment}"')
            p.sendline(f"get -r ./Benchmarking/{experiment.replace('.*', '*')}")  # Some regex compatibility
            p.expect('sftp> ', timeout=None)
        print()

    print('Connecting to lab', end=" ")
    p = spawn(f'sftp cornea')
    p.expect('sftp> ')
    print('- Connected! ✓\n')
    p.sendline(f"lcd {local_path}")
    p.expect('sftp> ')
    p.sendline("cd UnifiedML")
    p.expect('sftp> ')
    for i, experiment in enumerate(experiments):
        if experiment not in plot_specs.bluehive_only:
            print(f'{i + 1}/{len(experiments)} [lab] SFTP\'ing "{experiment}"')
            p.sendline(f"get -r ./Benchmarking/{experiment.replace('.*', '*')}")  # Some regex compatibility
            p.expect('sftp> ', timeout=None)

    print('\nPlotting results...')

    os.chdir(cwd)

# Generate each plot
for plot_train in [False, True]:

    print(f'\n Plotting {"train" if plot_train else "eval"}...')

    for plot_experiments in plot_specs.plots:

        plot(path=f"./Benchmarking/{plot_group + '/' if plot_group else ''}{'_'.join(plot_experiments)}/Plots/",
             plot_experiments=plot_experiments if len(plot_experiments) else None,
             plot_agents=plot_specs.agents if len(plot_specs.agents) else None,
             plot_suites=plot_specs.suites if len(plot_specs.suites) else None,
             plot_tasks=plot_specs.tasks if len(plot_specs.tasks) else None,
             steps=plot_specs.steps if plot_specs.steps else np.inf, write_tabular=False, plot_train=plot_train,
             title=plot_specs.title, x_axis=plot_specs.x_axis,
             verbose=True
             )
