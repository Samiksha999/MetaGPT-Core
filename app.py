import asyncio
import logging
import streamlit as st
from typing import Dict, Any, List
from collections import deque

# Configure structured system tracing for orchestration visibility
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class SharedEventBus:
    """Thread-safe, asynchronous pub-sub message fabric for multi-agent sync."""
    def __init__(self):
        self._subscribers: Dict[str, List[asyncio.Queue]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, topic: str) -> asyncio.Queue:
        async with self._lock:
            queue = asyncio.Queue()
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(queue)
            return queue

    async def publish(self, topic: str, message: Dict[str, Any]):
        async with self._lock:
            if topic in self._subscribers:
                for queue in self._subscribers[topic]:
                    await queue.put(message)

class MetaAgentNode:
    """High-performance agent wrapper with localized O(1) state monitoring."""
    def __init__(self, agent_id: str, role: str, bus: SharedEventBus):
        self.agent_id = agent_id
        self.role = role
        self.bus = bus
        self.state_history = deque(maxlen=100)

    async def run_lifecycle(self, listen_topic: str, publish_topic: str, log_container):
        queue = await self.bus.subscribe(listen_topic)
        log_container.info(f"🚀 Agent [{self.agent_id}] initialized as {self.role}. Listening on: {listen_topic}")
        
        try:
            while True:
                message = await queue.get()
                log_container.warning(f"⚙️ Agent [{self.agent_id}] Processing state mutation: {message.get('data')}")
                await asyncio.sleep(1.0) # Simulate complex analytical calculation steps
                
                processed_payload = {
                    "sender": self.agent_id,
                    "role": self.role,
                    "status": "COMPLETED",
                    "data": f"Executed tactical blueprint sequence for: {message.get('data')}"
                }
                
                await self.bus.publish(publish_topic, processed_payload)
                log_container.success(f"✅ Agent [{self.agent_id}] successfully committed output to {publish_topic}!")
                queue.task_done()
        except asyncio.CancelledError:
            pass

# --- Streamlit Observability Dashboard Frontend Layout ---
st.set_page_config(page_title="Agent Control Room", page_icon="🧠", layout="centered")
st.title("🧠 Agent Control Room")
st.caption("A tenant-aware, observable product-to-architecture multi-agent loop.")

st.markdown("---")

# User Configuration Input Components
with st.container():
    tenant = st.text_input("👤 Tenant Identifier", value="demo-tenant")
    request = st.text_area("📝 Engineering Request Prompt", value="Design a reliable document ingestion service with automated circuit breakers")

st.markdown(" ")

if st.button("🚀 Run Orchestration Agent", type="primary"):
    st.subheader("📊 System Telemetry Log Streams")
    log_slot = st.empty()
    
    async def trigger_pipeline():
        bus = SharedEventBus()
        pm_agent = MetaAgentNode("A01", "ProductManager", bus)
        arch_agent = MetaAgentNode("A02", "SoftwareArchitect", bus)
        
        # Ingest initial requirements stream payload
        await bus.publish("requirements_stream", {"data": request, "tenant": tenant})
        
        # Concurrently coordinate asynchronous agent lifecycle states safely
        await asyncio.gather(
            pm_agent.run_lifecycle("requirements_stream", "architecture_stream", log_slot),
            arch_agent.run_lifecycle("architecture_stream", "execution_stream", log_slot),
        )
    
    try:
        asyncio.run(trigger_pipeline())
    except Exception as e:
        pass
