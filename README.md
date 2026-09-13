# MetaGPT-Core: Tenant-Isolated Asynchronous Multi-Agent Orchestration Platform

A high-performance, tenant-isolated multi-agent orchestration framework built to manage long-horizon concurrent planning workflows with zero resource mutation race conditions.

## 🧠 Core Architecture & System Problem Solved
Traditional multi-agent networks operate sequentially or lack memory synchronization, resulting in major blocking wait states and data corruption hazards when multiple tenants scale simultaneous tasks. 

**MetaGPT-Core resolves this by implementing:**
* **Asynchronous Pub-Sub Event Bus:** Completely eliminates blocking wait states by executing agent lifecycle nodes on non-blocking async loops via an optimized `asyncio.Queue` system topology.
* **Thread-Safe Mutual Exclusion Isolation:** Leverages lock-synchronized primitives (`asyncio.Lock`) to isolate data structures and state mutations across unique tenant instances.

## 🛠️ Tech Stack
* **Core Language:** Python 3.10+
* **Concurrency Primitives:** Asyncio, Thread Synchronization Locks, Deque collections
* **Observability UI:** Streamlit Engine
* **System Logging:** Python Logging Module (Telemetry Tracing)

## 🚀 Step-by-Step Local Deployment Setup

Ensure you have Python 3.10 or higher installed on your computer.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd MetaGPT-Core
   ```

2. **Install Required Runtime Dependencies:**
   ```bash
   pip install streamlit
   ```

3. **Launch the Web UI Dashboard Interface:**
   ```bash
   streamlit run app.py
   ```

4. **Access the System Terminal Panel:**
   Open your browser and navigate to `http://localhost:8501` to view the live multi-agent execution tracks and telemetry stream logs.
