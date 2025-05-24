# 🚀 Teaching the SO-100 to Lift: Human Teleoperation in Isaac Lab

**Isaac Lab** allows developers to simulate and train robotic behaviors efficiently. In this post, we’ll show how to use **keyboard teleoperation** to control the **SO-100 robotic arm** for a cube-lifting task. These expert demos can be used to train imitation learning policies.

> 👉 **Follow this blog for full environment setup:**
> [Training SO-100 Robot for Cube Lifting in Isaac Lab](https://medium.com/@kabilankb2003/training-so-100-robot-for-cube-lifting-in-isaac-lab-from-simulation-to-intelligent-control-with-9e81f94c6d6e)

---

![Image](https://github.com/user-attachments/assets/cfffa2d1-c61a-4b8e-ba0e-650fb46cdc9f)

## 🧠 Why Teleoperate?

* Collect training data for imitation learning
* Prototype and debug new tasks
* Safe and repeatable in simulation

---

## 🛠️ Run the Teleoperation Script

```bash
python environments/teleoperation/teleop_se3_agent.py \
  --task Template-So-100-CubeLift-v0 \
  --num_envs 10 \
  --teleop_device keyboard
```

---

## 🎮 Keyboard Controls

| Action         | Keys                  |
| -------------- | --------------------- |
| Move XYZ       | W / A / S / D / Q / E |
| Rotate Axes    | Z / X / T / G / C / V |
| Toggle Gripper | K                     |
| Reset          | R                     |

---

## 💾 What Gets Recorded?

Saved to `datasets/`:

* RGB-D camera data
* Joint & gripper states
* End-effector 6-DoF actions

Ready for use in:

* Behavioral Cloning
* DAgger
* Offline RL

---

## ✅ Summary

Use teleoperation in Isaac Lab to collect expert demonstrations and kickstart policy training — all within a scalable simulation framework.

---
