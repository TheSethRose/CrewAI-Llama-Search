from crewai.tools import BaseTool
from typing import Dict

class CustomTool(BaseTool):
    name: str = "custom_tool"
    description: str = "Custom tool template"

    def _run(self, input_data: str) -> str:
        return "Tool execution result"

class HelloWorldTool(BaseTool):
    name: str = "hello_world"
    description: str = "A simple tool that returns 'Hello, World!'"

    def _run(self, input_data: str = "") -> str:
        return "Hello, World!"
