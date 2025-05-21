from qwen_agent.agents import Assistant

from qwen_agent.gui import WebUI

llm_cfg = {
    "model": "qwen3:32b",
    "model_server": "http://localhost:11434/v1/",
    "api_key": "",
    "generate_cfg": {"top_p": 0.8},
}

system_instruction = """You are a expert in power system.
"""

tools = [
    {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "D:\\Dev\\repo\\powerflow-mcp\\powerflow_mcp\\pandapower",
                ],
            },
            "pandapower": {
                "command": "uv",
                "args": [
                    "--directory",
                    "D:\\Dev\\repo\\powerflow-mcp\\powerflow_mcp\\pandapower",
                    "run",
                    "run_pf.py",
                ],
            },
        }
    },
    "code_interpreter",
]

files = []

bot = Assistant(
    llm=llm_cfg, system_message=system_instruction, function_list=tools, files=files
)

WebUI(bot).run()
