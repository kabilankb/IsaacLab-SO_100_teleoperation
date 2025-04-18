# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents

##
# Register Gym environments.
##


gym.register(
    id="Template-So-100-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        # Updated entry point for SO100 config
        "env_cfg_entry_point": f"{__name__}.joint_pos_env_cfg:SO100CubeLiftEnvCfg",
        # Keeping agent configs, assuming they are compatible or placeholders
        "skrl_cfg_entry_point": f"{agents.__name__}:skrl_ppo_cfg.yaml",
    },
    disable_env_checker=True,
)