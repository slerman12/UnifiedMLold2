# Copyright (c) AGI.__init__. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# MIT_LICENSE file in the root directory of this source tree.


def deepPolicyGradient(actor, critic, obs, action, step, logs=None):

    if not action.requires_grad:  # If not differentiable
        action = actor(obs, step).mean  # Differentiable action ensemble

    Qs = critic(obs, action)

    # Pessimistic Q-values per action
    q, _ = Qs.min(1)  # Min-reduced critic ensemble

    if critic.binary:  # When Sigmoid-activated
        q = q.log()  # (Log-space is more numerically stable)

    policy_loss = -q.mean()  # Policy gradient ascent

    if logs is not None:
        logs['policy_loss'] = policy_loss

    return policy_loss
