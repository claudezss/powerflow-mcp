# Powerflow MCP

A Model-Centric Programming (MCP) interface for running powerflow analysis and analyzing results using pandapower and fastmcp.

## Overview

This project provides a simple and intuitive interface for running powerflow analysis on various network models using the pandapower library. The MCP (Model-Centric Programming) approach, powered by fastmcp, allows users to easily:

- Select from a variety of pre-defined network models
- Run powerflow analysis with different algorithms
- Retrieve and analyze the results in a structured format
- Get summaries of voltage profiles, line loading, and power flow
- Access the API through FastMCP's web interface and OpenAPI documentation

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/powerflow-mcp.git
   cd powerflow-mcp
   ```

2. Install the package and its dependencies:
   ```
   pip install -e .
   ```

## Dependencies

- pandapower
- numpy
- matplotlib
- fastmcp

## Usage

### Basic Usage

```python
from powerflow_mcp.pandapower import PandapowerMCP

# Create an instance of the MCP
mcp = PandapowerMCP()

# List available networks
networks = mcp.list_available_networks()
print("Available networks:", networks)

# Load a network
network_name = "case14"  # IEEE 14-bus test case
result = mcp.load_network(network_name)

# Run powerflow analysis
pf_result = mcp.run_powerflow()

# Get voltage profile
voltage_profile = mcp.get_voltage_profile()
print(f"Min voltage: {voltage_profile['min_voltage_pu']:.4f} pu")
print(f"Max voltage: {voltage_profile['max_voltage_pu']:.4f} pu")

# Get line loading
line_loading = mcp.get_line_loading()
print(f"Max loading: {line_loading['max_loading_percent']:.2f}%")
print(f"Overloaded lines: {line_loading['overloaded_lines']}")

# Get power flow summary
summary = mcp.get_power_flow_summary()
print(f"Total losses: {summary['total_losses_mw']:.2f} MW")
```

### Interactive Example

Run the included example script for an interactive demonstration:

```
python example_pandapower_mcp.py
```

This script will:
1. Show a list of available networks
2. Let you choose a network to analyze
3. Run powerflow analysis
4. Display the results in a user-friendly format

## Available Networks

The MCP includes access to all standard pandapower test networks, including:
- IEEE test cases (case9, case14, case30, etc.)
- PEGASE cases
- RTE cases
- And more

## API Reference

### PandapowerMCP Class

The main class providing the MCP interface.

#### Methods:

- `list_available_networks()`: Returns a list of available network models
- `load_network(network_name)`: Loads a specific network by name
- `run_powerflow(algorithm="nr")`: Runs powerflow analysis with the specified algorithm
- `get_voltage_profile()`: Returns voltage profile information
- `get_line_loading()`: Returns line loading information
- `get_power_flow_summary()`: Returns a summary of the power flow results

### FastMCP API

This project uses the FastMCP framework, which provides additional features:

#### Web Interface

You can start the FastMCP web server with:

```python
from powerflow_mcp.pandapower import pandapower_mcp

# Start the FastMCP server
pandapower_mcp.run(host="0.0.0.0", port=8000)
```

Then access the web interface at http://localhost:8000 to:
- View the API documentation
- Test the API endpoints interactively
- Execute powerflow analysis through the web interface

#### Direct API Access

You can also access the FastMCP API directly:

```python
from powerflow_mcp.pandapower import pandapower_mcp

# Get the model
model = pandapower_mcp.model

# List available networks
networks = model.list_available_networks()

# Load a network
from powerflow_mcp.pandapower.fastmcp_impl import LoadNetworkInput
result = model.load_network(LoadNetworkInput(network_name="case14"))

# Run powerflow
from powerflow_mcp.pandapower.fastmcp_impl import RunPowerflowInput
pf_result = model.run_powerflow(RunPowerflowInput(algorithm="nr"))
```

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set up the pre-commit hooks:

```
pip install pre-commit
pre-commit install
```

## License

This project is licensed under the terms of the LICENSE file included in the repository.
