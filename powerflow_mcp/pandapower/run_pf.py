from io import BytesIO

from mcp.server.fastmcp import FastMCP, Context, Image
from pandapower import networks as pn
import pandapower as pp
from pathlib import Path
from pandapower import to_pickle
import pandapower.topology as top
import networkx as nx
import matplotlib.pyplot as plt

tmep_folder = Path(__file__).parent / "tmp"

tmep_folder.mkdir(exist_ok=True, parents=True)

mcp = FastMCP("run_pandapower_pf")

NETWORKS = {
    "case9": pn.case9,
    "case14": pn.case14,
    "case30": pn.case30,
    "ieee30": pn.case_ieee30,
    "cigre_mv": pn.create_cigre_network_mv,
    "case118": pn.case118,
    "case300": pn.case300,
    "case1888": pn.case1888rte,
    "case2848": pn.case2848rte,
    "case3120": pn.case3120sp,
    "case6470": pn.case6470rte,
    "case6515": pn.case6515rte,
    "case9241": pn.case9241pegase,
}


@mcp.tool()
async def get_available_networks() -> list[str]:
    """
    Get list of pandapower network name from `NETWORKS` keys.
    """

    return list(NETWORKS.keys())


@mcp.tool()
async def run_pf(network: str, ctx: Context) -> str:
    """
    Run powerflow on user-selected pandapower network.

    Args:
        network: Name of pandapower network.
    """

    await ctx.info(f"Initializing network: {network}...")

    try:
        net = NETWORKS[network]()
    except Exception:
        return "Network not found."

    await ctx.info(f"Network {network} initialized successfully.")

    await ctx.info(f"Running powerflow on network {network}..")

    pp.runpp(net)

    await ctx.info(f"Powerflow on network {network} completed successfully.")

    net_path = str((tmep_folder / f"{network}.p").absolute())

    to_pickle(net, net_path)

    await ctx.info(f"Network {network} saved to {net_path}")

    return f"Powerflow completed successfully and network saved to {net_path}."


@mcp.tool()
async def analysis_pf_result(network: str) -> Image:
    """
    Analysis powerflow result on user-selected pandapower network.

    Args:
        network: Name of pandapower network.
    """

    net = pp.from_pickle(open(str((tmep_folder / f"{network}.p").absolute()), "rb"))

    # Find the reference (slack) bus
    slack_bus_idx = net.ext_grid.bus.iloc[0]

    # Create the graph of the network
    graph = top.create_nxgraph(net, respect_switches=True)

    # Compute shortest path lengths (distance in number of branches) from slack bus
    distances = nx.single_source_shortest_path_length(graph, slack_bus_idx)

    # Prepare data for plotting
    bus_voltages = net.res_bus.vm_pu
    x = [distances[bus] for bus in net.bus.index]
    y = [bus_voltages.at[bus] for bus in net.bus.index]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color="blue")
    ax.set_xlabel("Distance from Slack Bus")
    ax.set_ylabel("Bus Voltage (p.u.)")
    ax.set_title("Bus Voltage Profile vs Distance")
    ax.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    # Convert to PIL Image
    return Image(data=buf.getvalue(), format="png")


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
