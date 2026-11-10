
from __future__ import annotations

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from typing import Any

# Import logic từ chat.py
from chat import (
    ROOT,
    ARTIFACTS_DIR,
    now_iso,
    safe_slug,
    trim_history,
    run_model_tool_loop,
    write_transcript,
)

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


# =====================================
# CONFIG
# =====================================

load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent Playground",
    page_icon="🤖",
    layout="wide"
)

TRANSCRIPTS_DIR = ROOT / "transcripts"
SYSTEM_PROMPT = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_FILE = ARTIFACTS_DIR / "tools.yaml"


# =====================================
# INITIALIZE AGENT
# =====================================

@st.cache_resource
def initialize_agent(provider_name, model_name, version):

    provider = make_provider(provider_name)

    selected_model = (
        model_name
        or getattr(provider, "default_model", None)
    )

    system_prompt = SYSTEM_PROMPT.read_text(
        encoding="utf-8"
    )

    declarations = load_tool_declarations(TOOLS_FILE)
    openai_tools = to_openai_tools(declarations)

    artifact_version = build_artifact_version(
        version,
        SYSTEM_PROMPT,
        TOOLS_FILE
    )

    return {
        "provider": provider,
        "model": selected_model,
        "system_prompt": system_prompt,
        "tools": openai_tools,
        "artifact_version": artifact_version
    }


# =====================================
# SESSION INITIALIZATION
# =====================================

def initialize_session():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "history" not in st.session_state:
        st.session_state.history = []

    if "turns" not in st.session_state:
        st.session_state.turns = []

    if "transcript" not in st.session_state:

        timestamp = datetime.now().strftime(
            "%Y%m%dT%H%M%S%f"
        )

        transcript_id = (
            f"v0_openrouter_{timestamp}"
        )

        artifact_version = st.session_state.agent[
            "artifact_version"
        ]

        st.session_state.transcript = {
            "transcript_id": transcript_id,
            **artifact_version_dict(artifact_version),
            "provider": st.session_state.provider_name,
            "model": st.session_state.agent["model"],
            "system_prompt": str(SYSTEM_PROMPT),
            "tools": str(TOOLS_FILE),
            "history_window": 5,
            "max_tool_rounds": 4,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": []
        }

        st.session_state.transcript_path = (
            TRANSCRIPTS_DIR
            / f"{transcript_id}.transcript.json"
        )

        write_transcript(
            st.session_state.transcript_path,
            st.session_state.transcript
        )


# =====================================
# SAVE TRANSCRIPT
# =====================================

def save_turn(turn_record):

    st.session_state.turns.append(turn_record)

    st.session_state.transcript["turns"] = (
        st.session_state.turns
    )

    write_transcript(
        st.session_state.transcript_path,
        st.session_state.transcript
    )


# =====================================
# PROCESS USER QUERY
# =====================================

def process_query(query):

    agent = st.session_state.agent

    messages = [
        {
            "role": "system",
            "content": agent["system_prompt"]
        },
        *trim_history(
            st.session_state.history,
            5
        ),
        {
            "role": "user",
            "content": query
        }
    ]

    turn_index = len(st.session_state.turns) + 1

    turn_record = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": query,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": []
    }

    try:

        result = run_model_tool_loop(
            provider=agent["provider"],
            messages=messages,
            tools=agent["tools"],
            model=agent["model"],
            max_tool_rounds=4
        )

        turn_record.update(result)

        assistant_text = result["assistant_text"]

        # Maintain conversation history
        st.session_state.history.append({
            "role": "user",
            "content": query
        })

        st.session_state.history.append({
            "role": "assistant",
            "content": assistant_text
        })

    except Exception as exc:

        assistant_text = (
            f"Agent error: {type(exc).__name__}: {exc}"
        )

        turn_record.update({
            "status": "provider_error",
            "error": assistant_text
        })

    turn_record["ended_at"] = now_iso()

    save_turn(turn_record)

    return assistant_text, turn_record


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🤖 Agent Configuration")

provider_name = st.sidebar.selectbox(
    "Provider",
    ["openrouter", "openai", "anthropic", "gemini", "ollama"],
    index=0
)

model_name = st.sidebar.text_input(
    "Model (optional)",
    value=""
)

version = st.sidebar.selectbox(
    "Artifact Version",
    ["v0", "v1", "v2"]
)

history_window = st.sidebar.slider(
    "History Window",
    min_value=1,
    max_value=10,
    value=5
)

max_tool_rounds = st.sidebar.slider(
    "Max Tool Rounds",
    min_value=1,
    max_value=10,
    value=4
)

if st.sidebar.button("Initialize / Reset Agent"):

    for key in [
        "agent", "messages", "history",
        "turns", "transcript", "transcript_path"
    ]:
        st.session_state.pop(key, None)

    st.session_state.provider_name = provider_name

    st.session_state.agent = initialize_agent(
        provider_name,
        model_name.strip() or None,
        version
    )

    st.rerun()


# =====================================
# INITIALIZE FIRST TIME
# =====================================

if "agent" not in st.session_state:

    st.session_state.provider_name = provider_name

    try:
        st.session_state.agent = initialize_agent(
            provider_name,
            model_name.strip() or None,
            version
        )

        initialize_session()

    except Exception as exc:
        st.error(f"Agent initialization failed: {exc}")
        st.stop()

elif "transcript" not in st.session_state:

    initialize_session()


# =====================================
# MAIN UI
# =====================================

st.title("🤖 Research Agent Playground")

st.caption(
    "Live Chat | Tool Calling | Transcript Logging"
)

tab_chat, tab_transcript, tab_info = st.tabs([
    "💬 Live Chat",
    "📄 Transcript",
    "⚙️ Agent Information"
])


# =====================================
# TAB 1: LIVE CHAT
# =====================================

with tab_chat:

    st.subheader("Chat with Research Agent")

    st.caption(
        f"Provider: {st.session_state.provider_name} "
        f"| Model: {st.session_state.agent['model']}"
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message.get("tool_events"):

                with st.expander("Tool Calls & Results"):

                    st.json(message["tool_events"])

            if message.get("status"):

                st.caption(
                    f"Status: {message['status']}"
                )

    query = st.chat_input(
        "Ask your Research Agent..."
    )

    if query:

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):

            with st.spinner("Agent is thinking..."):

                # Update configuration from sidebar
                result_text, turn_record = process_query(query)

            st.markdown(result_text)

            if turn_record.get("tool_events"):

                with st.expander("Tool Calls & Results"):

                    st.json(turn_record["tool_events"])

            st.caption(
                f"Status: {turn_record.get('status')}"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": result_text,
            "tool_events": turn_record.get(
                "tool_events", []
            ),
            "status": turn_record.get("status")
        })


# =====================================
# TAB 2: TRANSCRIPT
# =====================================

with tab_transcript:

    st.subheader("Conversation Transcript")

    transcript = st.session_state.transcript

    st.write(
        f"**Transcript ID:** "
        f"{transcript['transcript_id']}"
    )

    st.write(
        f"**Total Turns:** {len(transcript['turns'])}"
    )

    st.write(
        f"**File:** `{st.session_state.transcript_path}`"
    )

    st.json(transcript)

    transcript_json = json.dumps(
        transcript,
        ensure_ascii=False,
        indent=2,
        default=str
    )

    st.download_button(
        "Download Transcript JSON",
        data=transcript_json,
        file_name=(
            transcript["transcript_id"]
            + ".transcript.json"
        ),
        mime="application/json"
    )


# =====================================
# TAB 3: AGENT INFORMATION
# =====================================

with tab_info:

    st.subheader("Agent Configuration")

    st.write({
        "Provider": st.session_state.provider_name,
        "Model": st.session_state.agent["model"],
        "System Prompt": str(SYSTEM_PROMPT),
        "Tools": str(TOOLS_FILE),
        "History Window": history_window,
        "Max Tool Rounds": max_tool_rounds
    })

    st.subheader("Available Tools")

    st.write(
        st.session_state.agent["tools"]
    )

    st.subheader("Artifact Version")

    st.write(
        artifact_version_dict(
            st.session_state.agent["artifact_version"]
        )
    )
