# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import copy
import dataclasses

from isaaclab.assets import RigidObjectCfg, ArticulationCfg, AssetBaseCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
import isaaclab.sim as sim_utils  # For the debug visualization
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab_tasks.manager_based.manipulation.lift import mdp

from .so_100_base_env_cfg import SO100LiftEnvCfg
from .so_100_robot_cfg import SO100_CFG  # isort: skip

##
# Pre-defined configs
##
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip
# from .SO100 import SO100_CFG  # Corrected import # isort: skip


@configclass
class SO100CubeLiftEnvCfg(SO100LiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set SO100 as robot
        _robot_cfg = dataclasses.replace(SO100_CFG, prim_path="{ENV_REGEX_NS}/Robot")
        # Set initial rotation if needed
        if _robot_cfg.init_state is None:
            _robot_cfg.init_state = ArticulationCfg.InitialStateCfg()
        _robot_cfg.init_state = dataclasses.replace(_robot_cfg.init_state, rot=(0.7071068, 0.0, 0.0, 0.7071068))
        self.scene.robot = _robot_cfg

        # Set actions for the specific robot type (SO100)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["Shoulder_Rotation", "Shoulder_Pitch", "Elbow", "Wrist_Pitch", "Wrist_Roll"],
            scale=0.5,
            use_default_offset=True
        )
        
        # self.actions.gripper_action = mdp.JointPositionActionCfg(
        #     asset_name="robot",
        #     joint_names=["Gripper"],
        #     scale=2,
        #     use_default_offset=True
        # )

        # Set gripper action with wider range for better visibility
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["Gripper"],
            open_command_expr={"Gripper": 0.5},  # Fully open
            close_command_expr={"Gripper": 0.0}  # flly closed
        )
        
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "Fixed_Gripper"
        # Disable debug visualization for the target pose command
        self.commands.object_pose.debug_vis = False

        # Set Cube as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(pos=(0.2, 0.0, 0.015), rot=(1.0, 0.0, 0.0, 0.0)),
            spawn=UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/DexCube/dex_cube_instanceable.usd",
                scale=(0.3, 0.3, 0.3),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=16,
                    solver_velocity_iteration_count=1,
                    max_angular_velocity=1000.0,
                    max_linear_velocity=1000.0,
                    max_depenetration_velocity=5.0,
                    disable_gravity=False,
                ),
            ),
        )

        # Configure end-effector marker
        marker_cfg = copy.deepcopy(FRAME_MARKER_CFG)
        # Properly replace the frame marker configuration
        marker_cfg.markers = {
            "frame": sim_utils.UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/UIElements/frame_prim.usd",
                scale=(0.05, 0.05, 0.05),
            )
        }
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        
        # Updated FrameTransformerCfg for alternate USD structure
        self.scene.ee_frame = FrameTransformerCfg(
            # Original path in comments for reference
            # prim_path="{ENV_REGEX_NS}/Robot/SO_100/SO_5DOF_ARM100_05d_SLDASM/Base",
            # Updated path for the new USD structure
            prim_path="{ENV_REGEX_NS}/Robot/Base",
            debug_vis=True,  # Enable visualization
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    # Original path in comments for reference
                    # prim_path="{ENV_REGEX_NS}/Robot/SO_100/SO_5DOF_ARM100_05d_SLDASM/Fixed_Gripper",
                    # Updated path for the new USD structure
                    prim_path="{ENV_REGEX_NS}/Robot/Fixed_Gripper",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=(0.01, -0.0, 0.1),
                    ),
                ),
            ],
        )

        # Configure cube marker with different color and path
        cube_marker_cfg = copy.deepcopy(FRAME_MARKER_CFG)
        cube_marker_cfg.markers = {
            "frame": sim_utils.UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/UIElements/frame_prim.usd",
                scale=(0.05, 0.05, 0.05),
                visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
            )
        }
        cube_marker_cfg.prim_path = "/Visuals/CubeFrameMarker"
        
        self.scene.cube_marker = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            debug_vis=True,
            visualizer_cfg=cube_marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Object",
                    name="cube",
                    offset=OffsetCfg(
                        pos=(0.0, 0.0, 0.0),
                    ),
                ),
            ],
        )


@configclass
class SO100CubeLiftEnvCfg_PLAY(SO100CubeLiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
