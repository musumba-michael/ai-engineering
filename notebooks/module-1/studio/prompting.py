"""08-prompting.ipynb — a system prompt with few-shot examples and structured output."""

from langchain.agents import create_agent
from pydantic import BaseModel

SYSTEM_PROMPT = """

You are a science fiction writer, create a space capital city at the users request.

User: What is the capital of mars?
Scifi Writer: Marsialis

User: What is the capital of Venus?
Scifi Writer: Venusovia

"""


class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str


graph = create_agent(
    model="gpt-5-nano",
    system_prompt=SYSTEM_PROMPT,
    response_format=CapitalInfo,
)
