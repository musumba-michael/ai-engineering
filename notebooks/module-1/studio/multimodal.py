"""08-multimodal-messages.ipynb — an agent that accepts text and image content blocks.

Send a message whose content is a list of blocks, e.g.

    [{"type": "text", "text": "Tell me about this capital"},
     {"type": "image", "base64": "<...>", "mime_type": "image/png"}]
"""

from langchain.agents import create_agent

graph = create_agent(
    model="gpt-5-nano",
    system_prompt=(
        "You are a science fiction writer. Create a capital city at the user's request, "
        "and describe any image you are given as if it were that city."
    ),
)
