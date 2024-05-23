import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional

avatars = {
    "AP Processor": "avatars/approcessor.png",
    "Director of Accounts Payable": "avatars/directorofap.png",
    "System Administrator": "avatars/systemadmin.png",
    "Product Manager": "avatars/productmanager.png",
    "assistant": "avatars/assistant.png"
}

class MyCustomHandler(BaseCallbackHandler):

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""

        #chat_interface.send(inputs['input'], user="Assistant", respond=False)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
    
        #chat_interface.send(outputs['output'], user=self.agent_name, avatar=avatars[self.agent_name], respond=False)





















