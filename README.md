# SO-100 Robot Cube Lifting Environment

## Overview

This project is an external project for Isaac Lab that implements a cube lifting task using the SO-100 robot arm. For more information about external projects in Isaac Lab, see the [documentation](https://isaac-sim.github.io/IsaacLab/main/source/overview/developer-guide/template.html).

## Installation

1. Install Isaac Lab by following the [installation guide](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html).
   We recommend using conda installation as it simplifies calling Python scripts from the terminal.

2. Install this project in editable mode:
   ```bash
   python -m pip install -e source/SO_100
   ```

## Usage
(Ensure your Isaac Lab conda environment is activated before running these commands)

### List Available Tasks
Verify that the SO-100 environment is registered:
```bash
python scripts/list_envs.py
```
You should see `Template-So-100-CubeLift-v0` in the output.

### Train the Agent

To watch training with a small number of environments:
```bash
# Training with visual feedback (32 environments)
python scripts/skrl/train.py --task Template-So-100-CubeLift-v0 --num_envs 32
```

To accelerate training (more environments, no graphical interface):
```bash
# Headless training with more environments
python scripts/skrl/train.py --task Template-So-100-CubeLift-v0 --num_envs 4096 --headless
```

Training logs and checkpoints are saved under the `logs/skrl/SO100_lift/trained/` directory.

### Play/Evaluate the Agent

Run the best-performing policy found during training:
```bash
python scripts/skrl/play.py --task Template-So-100-CubeLift-v0 --checkpoint logs/skrl/SO100_lift/trained/checkpoints/best_agent.pt
```

> **Note**: Make sure to add `logs/skrl/SO100_lift/trained/` to your `.gitignore` file to avoid committing large training files.

## Building Your Own Project or Task

Traditionally, building new projects that utilize Isaac Lab's features required creating your own extensions within the Isaac Lab repository. However, this approach can obscure project visibility and complicate updates from one version of Isaac Lab to another. To circumvent these challenges, we now provide a command-line tool (template generator) for creating Isaac Lab-based projects and tasks.

The template generator enables you to create:

### External project (recommended)
An isolated project that is not part of the Isaac Lab repository. This approach works outside of the core Isaac Lab repository, ensuring that your development efforts remain self-contained. Also, it allows your code to be run as an extension in Omniverse.

> **Hint**: For the external project, the template generator will initialize a new Git repository in the specified directory. You can push the generated content to your own remote repository (e.g. GitHub) and share it with others.

### Internal task
A task that is part of the Isaac Lab repository. This approach should only be used to create new tasks within the Isaac Lab repository in order to contribute to it.

## Installation Guide

### Prerequisites
1. Install Isaac Lab by following the [installation guide](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html).
   We recommend using conda installation as it simplifies calling Python scripts from the terminal.

### Running the Template Generator

Run the following command to generate a new external project or internal task:

**Linux**:
```bash
./isaaclab.sh --new  # or "./isaaclab.sh -n"
```

**Windows**:
```bash
isaaclab.bat --new  # or "isaaclab.bat -n"
```

The generator will guide you in setting up the project/task by asking about:
- Type of project/task (external or internal)
- Project/task path or names
- Isaac Lab workflows
- Reinforcement learning libraries and algorithms

### External Project Usage

Once the external project is generated:

1. Install the project in editable mode:
   ```bash
   # Linux/Windows
   python -m pip install -e source/<given-project-name>
   ```

2. List available tasks:
   ```bash
   # Linux/Windows
   python scripts/list_envs.py
   ```
   > **Note**: If task names change, update the search pattern "Template-" in scripts/list_envs.py

3. Run a task:
   ```bash
   # Linux/Windows
   python scripts/<specific-rl-library>/train.py --task=<Task-Name>
   ```

### Internal Task Usage

For internal tasks, once generated:

1. List available tasks:
   ```bash
   # Linux/Windows
   python scripts/environments/list_envs.py
   ```

2. Run a task:
   ```bash
   # Linux/Windows
   python scripts/reinforcement_learning/<specific-rl-library>/train.py --task=<Task-Name>
   ```

3. Run with dummy agents (useful for environment configuration testing):
   
   Zero-action agent:
   ```bash
   # Linux/Windows
   python scripts/zero_agent.py --task=<Task-Name>
   ```

   Random-action agent:
   ```bash
   # Linux/Windows
   python scripts/random_agent.py --task=<Task-Name>
   ```

> **Note**: If Isaac Lab is not installed in a conda environment or in a (virtual) Python environment, use `FULL_PATH_TO_ISAACLAB/isaaclab.sh -p` (Linux) or `FULL_PATH_TO_ISAACLAB\isaaclab.bat -p` (Windows) instead of `python` for the commands above.

## Keywords

**Keywords:** extension, template, isaaclab

### Set up IDE (Optional)

To setup the IDE, please follow these instructions:

- Run VSCode Tasks, by pressing `Ctrl+Shift+P`, selecting `Tasks: Run Task` and running the `setup_python_env` in the drop down menu.
  When running this task, you will be prompted to add the absolute path to your Isaac Sim installation.

If everything executes correctly, it should create a file .python.env in the `.vscode` directory.
The file contains the python paths to all the extensions provided by Isaac Sim and Omniverse.
This helps in indexing all the python modules for intelligent suggestions while writing code.

### Setup as Omniverse Extension (Optional)

We provide an example UI extension that will load upon enabling your extension defined in `source/SO_100/SO_100/ui_extension_example.py`.

To enable your extension, follow these steps:

1. **Add the search path of this project/repository** to the extension manager:
    - Navigate to the extension manager using `Window` -> `Extensions`.
    - Click on the **Hamburger Icon**, then go to `Settings`.
    - In the `Extension Search Paths`, enter the absolute path to the `source` directory of this project/repository.
    - If not already present, in the `Extension Search Paths`, enter the path that leads to Isaac Lab's extension directory directory (`IsaacLab/source`)
    - Click on the **Hamburger Icon**, then click `Refresh`.

2. **Search and enable your extension**:
    - Find your extension under the `Third Party` category.
    - Toggle it to enable your extension.

## Code formatting

We have a pre-commit template to automatically format your code.
To install pre-commit:

```bash
pip install pre-commit
```

Then you can run pre-commit with:

```bash
pre-commit run --all-files
```

## Troubleshooting

### Pylance Missing Indexing of Extensions

In some VsCode versions, the indexing of part of the extensions is missing.
In this case, add the path to your extension in `.vscode/settings.json` under the key `"python.analysis.extraPaths"`.

```json
{
    "python.analysis.extraPaths": [
        "<path-to-ext-repo>/source/SO_100"
    ]
}
```

### Pylance Crash

If you encounter a crash in `pylance`, it is probable that too many files are indexed and you run out of memory.
A possible solution is to exclude some of omniverse packages that are not used in your project.
To do so, modify `.vscode/settings.json` and comment out packages under the key `"python.analysis.extraPaths"`
Some examples of packages that can likely be excluded are:

```json
"<path-to-isaac-sim>/extscache/omni.anim.*"         // Animation packages
"<path-to-isaac-sim>/extscache/omni.kit.*"          // Kit UI tools
"<path-to-isaac-sim>/extscache/omni.graph.*"        // Graph UI tools
"<path-to-isaac-sim>/extscache/omni.services.*"     // Services tools
...
```