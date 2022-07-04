# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.
import os
from collections import deque

from dm_env import StepType

import numpy as np


# Access a dict with attribute or key (purely for aesthetic reasons)
class AttrDict(dict):
    def __init__(self, _dict):
        super(AttrDict, self).__init__()
        self.__dict__ = self
        self.update(_dict)


class Env:
    """
    A general-purpose environment.

    Must accept: (task, seed, **kwargs) as init args.

    Must have:

    (1) a "step" function, action -> exp
    (2) "reset" function, -> exp
    (3) "render" function, -> image
    (4) "discrete" attribute
    (5) "episode_done" attribute
    (6) "obs_spec" attribute which includes:
        - "name" ('obs'), "shape", "mean", "stddev", "low", "high" (the last 4 can be None)
    (7) "action-spec" attribute which includes:
        - "name" ('action'), "shape", "num_actions" (should be None if not discrete),
          "low", "high" (these last 2 should be None if discrete, can be None if not discrete)

    An "exp" (experience) is an AttrDict consisting of "obs", "action", "reward", "label", "step"
    numpy values which can be NaN. "obs" must include a batch dim.

    Can optionally include a frame_stack method.

    """
    def __init__(self, task='cheetah_run', seed=0, frame_stack=1, **kwargs):
        self.discrete = False
        self.episode_done = False

        # Make env

        # Import DM Control here to avoid glfw warnings

        try:
            # Try EGL rendering (faster)
            os.environ['MUJOCO_GL'] = 'egl'
            from dm_control import manipulation, suite
        except ImportError:
            del os.environ['MUJOCO_GL']  # Otherwise GLFW
            from dm_control import manipulation, suite

        from dm_control.suite.wrappers import action_scale, pixels

        domain, task = task.split('_', 1)

        # Load task
        if (domain, task) in suite.ALL_TASKS:
            self.env = suite.load('ball_in_cup' if domain == 'cup' else domain,  # Overwrite cup to ball_in_cup
                                  task,
                                  task_kwargs={'random': seed},
                                  visualize_reward=False)  # Don't visualize reward
            self.key = 'pixels'
        else:
            task = f'{domain}_{task}_vision'
            self.env = manipulation.load(task, seed=seed)
            self.key = 'front_close'

        # Rescale actions to range [-1, 1]
        self.env = action_scale.Wrapper(self.env, minimum=-1.0, maximum=+1.0)

        # Add rendering for classical tasks
        if (domain, task) in suite.ALL_TASKS:
            # Zoom in camera for quadruped
            camera_id = dict(quadruped=2).get(domain, 0)
            render_kwargs = dict(height=84, width=84, camera_id=camera_id)
            self.env = pixels.Wrapper(self.env,
                                      pixels_only=True,  # No proprioception (key <- 'position')
                                      render_kwargs=render_kwargs)

        # Channel-first
        obs_shape = self.env.observation_spec()[self.key].shape
        if len(obs_shape) == 3:
            obs_shape = [obs_shape[-1], *obs_shape[:-1]]

        # Frame stack
        obs_shape[0] *= frame_stack

        self.obs_spec = {'name': 'obs',
                         'shape': obs_shape,
                         'mean': None,
                         'stddev': None,
                         'low': 0,
                         'high': 255}

        self.action_spec = {'name': 'action',
                            'shape': self.env.action_spec().shape,
                            'num_actions': None,
                            'low': -1,
                            'high': 1}

        self.frames = deque([], frame_stack or 1)

    def step(self, action):
        # To float
        action = action.astype(np.float32)
        # Remove batch dim
        action = action.squeeze(0)

        # Step env
        time_step = self.env.step(action)

        # Create experience
        exp = {'obs': time_step.observation[self.key], 'action': action, 'reward': time_step.reward,
               'label': None, 'step': None}
        # Add batch dim
        exp['obs'] = np.expand_dims(exp['obs'], 0)
        # Channel-first
        exp['obs'] = exp['obs'].transpose(0, 3, 1, 2)

        # Scalars/NaN to numpy
        for key in exp:
            if np.isscalar(exp[key]) or exp[key] is None or type(exp[key]) == bool or  exp[key].shape == ():
                exp[key] = np.full([1, 1], exp[key], 'float32')

        if time_step.step_type == StepType.LAST:
            self.episode_done = True

        return AttrDict(exp)

    def frame_stack(self, obs):
        for _ in range(self.frames.maxlen - len(self.frames) + 1):
            self.frames.append(obs)

        return np.concatenate(list(self.frames), axis=1)

    def reset(self):
        time_step = self.env.reset()
        self.episode_done = False

        # Create experience
        exp = {'obs': time_step.observation[self.key], 'action': None, 'reward': time_step.reward,
               'label': None, 'step': None}
        # Add batch dim
        exp['obs'] = np.expand_dims(exp['obs'], 0)
        # Channel-first
        exp['obs'] = exp['obs'].transpose(0, 3, 1, 2)

        # Scalars/NaN to numpy
        for key in exp:
            if np.isscalar(exp[key]) or exp[key] is None or type(exp[key]) == bool or exp[key].shape == ():
                exp[key] = np.full([1, 1], exp[key], 'float32')

        # Clear frame stack
        self.frames.clear()

        return AttrDict(exp)

    def render(self):
        return self.env.physics.render(height=256, width=256, camera_id=0)
