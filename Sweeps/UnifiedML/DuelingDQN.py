# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
from Sweeps.Templates import template, atari


def join(atari_tasks):
    return f'atari/{",atari/".join([a.lower() for a in atari_tasks])}'


runs = template('UnifiedML')

runs.UnifiedML.sweep = [
    # Less Exploration
    f"""
    task={join(atari)}
    train_steps=1000000
    save_per_steps=200000
    replay.save=true
    'stddev_schedule="linear(1.0,0.1,20000)"'
    Agent=Agents.DuelingDQNAgent
    experiment=Atari26-LessExplore
    time="5-00:00:00"
    mem=50
    reservation_id=20221217
    """,  # Note: Manually set "pseudonym" to task_name in sbatch.yaml
]  # Replay capacity is  1000000


runs.UnifiedML.plots = [
    ['Atari26-.*Explore']
]

# runs.UnifiedML.agents = ['DuelingDQNAgent']

runs.UnifiedML.sftp = True
runs.UnifiedML.lab = False
runs.UnifiedML.title = 'The Atari 26-Games Benchmark, 1 Million env steps'
runs.UnifiedML.steps = 1e6
runs.UnifiedML.write_tabular = True
