# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for the SO100 5-DOF robot arm for livestream.

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
SO100_USD_PATH = os.path.join(_THIS_SCRIPT_DIR, "asset", "so_100.usd")
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
            "Shoulder_Rotation": 0.1,
            "Shoulder_Pitch": 0.5,
            "Elbow": 0.0,
            "Wrist_Pitch": 0.0,
            "Wrist_Roll": 0.0,
            "Gripper": 0.3,  # Change from 0.5 to 0.3 (middle position) to make movement more apparent
        },
        # Set initial joint velocities to zero
        joint_vel={".*": 0.0},
    ),
    actuators={
        # Grouping arm joints, adjust limits as needed
        # Shoulder rotation moves: ALL mass (~0.8kg total)
        "shoulder_rotation": ImplicitActuatorCfg(
            joint_names_expr=["Shoulder_Rotation"],
            effort_limit=1.9,
            velocity_limit_sim=1.5,
            stiffness=200.0,    # Highest - moves all mass
            damping=80.0,
        ),
        # Shoulder pitch moves: Everything except base (~0.65kg)
        "shoulder_pitch": ImplicitActuatorCfg(
            joint_names_expr=["Shoulder_Pitch"],
            effort_limit=1.9,
            velocity_limit_sim=1.5,
            stiffness=170.0,    # Slightly less than rotation
            damping=65.0,
        ),
        # Elbow moves: Lower arm, wrist, gripper (~0.38kg)
        "elbow": ImplicitActuatorCfg(
            joint_names_expr=["Elbow"],
            effort_limit=1.9,
            velocity_limit_sim=1.5,
            stiffness=120.0,    # Reduced based on less mass
            damping=45.0,
        ),
        # Wrist pitch moves: Wrist and gripper (~0.24kg)
        "wrist_pitch": ImplicitActuatorCfg(
            joint_names_expr=["Wrist_Pitch"],
            effort_limit=1.9,
            velocity_limit_sim=1.5,
            stiffness=80.0,     # Reduced for less mass
            damping=30.0,
        ),
        # Wrist roll moves: Gripper assembly (~0.14kg)
        "wrist_roll": ImplicitActuatorCfg(
            joint_names_expr=["Wrist_Roll"],
            effort_limit=1.9,
            velocity_limit_sim=1.5,
            stiffness=50.0,     # Low mass to move
            damping=20.0,
        ),
        # Gripper moves: Only moving jaw (~0.034kg)
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["Gripper"],
            effort_limit=2.5,    # Increased from 1.9 to 2.5 for stronger grip
            velocity_limit_sim=1.5,
            stiffness=60.0,     # Increased from 25.0 to 60.0 for more reliable closing
            damping=20.0,       # Increased from 10.0 to 20.0 for stability
        ),
    },
    # Using default soft limits
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of SO100 robot arm."""
# Removed FRANKA_PANDA_HIGH_PD_CFG as it's not applicable
