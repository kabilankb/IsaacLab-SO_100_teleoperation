# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for the SO100 5-DOF robot arm.

The following configurations are available:

* :obj:`SO100_CFG`: SO100 robot arm configuration.

"""

import os
import math

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

# Note: Use forward slashes for paths even on Windows
# Construct the absolute path to the USD file relative to this script's location
_THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SO100_USD_PATH = os.path.join(_THIS_SCRIPT_DIR, "asset", "SO-100-Final.usd")
##
# Configuration
##

SO100_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=SO100_USD_PATH,
        activate_contact_sensors=False,  # Adjust based on need
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,  # Default to False, adjust if needed
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "Shoulder_Rotation": 0.0,
            "Shoulder_Pitch": 0.0,
            "Elbow": 0.0,
            "Wrist_Pitch": 0.0,
            "Wrist_Roll": 0.0,
            "Gripper": 0.3, # Assuming 0 is a reasonable start (e.g., closed or open based on limits)
        },
        # Set initial joint velocities to zero
        joint_vel={".*": 0.0},
    ),
    actuators={
        # Grouping arm joints, adjust limits as needed
        "shoulder_rotation": ImplicitActuatorCfg(
            joint_names_expr=["Shoulder_Rotation"],
            effort_limit=87,
            velocity_limit=0, 
            stiffness=80.0,
            damping=400.0,
        ),
        "shoulder_pitch": ImplicitActuatorCfg(
            joint_names_expr=["Shoulder_Pitch"],
            effort_limit=87,
            velocity_limit=0, 
            stiffness=80.0,
            damping=400.0,
        ),
        "elbow": ImplicitActuatorCfg(
            joint_names_expr=["Elbow"],
            effort_limit=87,
            velocity_limit=0, 
            stiffness=80.0,
            damping=400.0,
        ),
        "wrist_pitch": ImplicitActuatorCfg(
            joint_names_expr=["Wrist_Pitch"],
            effort_limit=87,
            velocity_limit=0, 
            stiffness=80.0,
            damping=400.0,
        ),
        "wrist_roll": ImplicitActuatorCfg(
            joint_names_expr=["Wrist_Roll"],
            effort_limit=87,
            velocity_limit=0, 
            stiffness=80.0,
            damping=400.0,
        ),
        # Gripper actuator - assuming angular drive
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["Gripper"],
            effort_limit=87,
            velocity_limit=0, 
            stiffness=80.0,
            damping=400.0,
        ),
    },
    # Using default soft limits
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of SO100 robot arm."""
# Removed FRANKA_PANDA_HIGH_PD_CFG as it's not applicable
