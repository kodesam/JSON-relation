# JSON Relation

## Overview
This repository is focused on managing JSON data interactions using Python and Jinja. Below is a summary of the files and their descriptions.

## Repository Contents

### Python Scripts
- **`upgrade/timeline.py`**: Generates a calendar with nodes listed for each date.
- **`upgrade/timeline-v2.py`**: Schedules upgrades with additional functionality.
- **`netbox-gen/netbox-gen.py`**: Generates NetBox YAML output using Jinja2 templates.

### Data and Template Files
- **`upgrade/node_data.txt`**: Contains node and type information.
- **`netbox-gen/server_hardware_template.j2`**: Jinja2 template for server hardware data.
- **`netbox-gen/server_hardware_data.yaml`**: YAML data for server hardware.
- **`netbox-gen/netbox_output.yaml`**: Generated NetBox YAML output.

### Configuration Files
- **`.devcontainer/devcontainer.json`**: Configuration file for VS Code's dev container setup.

## Language Composition
- **Python**: 77.3%
- **Jinja**: 22.7%

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/kodesam/JSON-relation.git
   cd JSON-relation
