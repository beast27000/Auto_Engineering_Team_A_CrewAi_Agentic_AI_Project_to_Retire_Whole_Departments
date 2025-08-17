# EngineeringTeam Crew

Welcome to the EngineeringTeam Crew project, powered by [CrewAI](https://crewai.com/). This project demonstrates how a team of specialized AI agents can work together like a real engineering department—designing, coding, testing, and deploying a fullstack application with a Gradio frontend and an SQL backend.

The goal is to showcase that agentic AI is not just another LLM-based assistant, but a fully functioning autonomous engineering team, capable of building complete working software systems—without humans in the loop.

## Key Capabilities

- Multi-Agent Engineering Team – AI agents with specialized roles (frontend, backend, database, QA, architect, PM) collaborate seamlessly.
- Code Generation & Execution – Agents write, review, and run their own code inside a controlled environment.
- Fullstack Development – End-to-end project delivery with:
  - Frontend – Interactive UI built using Gradio.
  - Backend – API + business logic powered by Python.
  - Database – Fully integrated SQL backend.
- Containerized Execution – Code is executed in Docker environments for safety and reproducibility.
- Human-Free Workflow – Agents can plan, code, test, debug, and deliver final outputs autonomously.

## Installation

Ensure you have Python >=3.10 <3.13 installed. This project uses [UV](https://github.com/astral-sh/uv) for dependency management.

Install uv if not already:

```bash
pip install uv
```

Navigate to the project directory and install dependencies:

```bash
uv sync
```

(Optional) lock dependencies with:

```bash
crewai install
```

## Customizing

- Add your `OPENAI_API_KEY` in the `.env` file.
- Modify `src/engineering_team/config/agents.yaml` to define your agents.
- Modify `src/engineering_team/config/tasks.yaml` to define your tasks.
- Extend `src/engineering_team/crew.py` for logic, tools, and coordination.
- Update `src/engineering_team/main.py` to adjust project inputs.

## Running the Project

To launch your autonomous engineering team:

```bash
crewai run
```

This initializes the EngineeringTeam Crew, assigns tasks, and orchestrates collaboration across agents. The default example will output a `report.md` and a working fullstack demo project (frontend + backend + DB).

## Understanding Your Crew

The EngineeringTeam Crew is structured like a real software department:

- Frontend Agent – Builds interactive UIs with Gradio.
- Backend Agent – Creates APIs, business logic, and integrations.
- Database Agent – Sets up, queries, and manages SQL.
- QA Agent – Tests and validates outputs.
- Project Manager Agent – Coordinates tasks and ensures delivery.

Tasks are defined in `config/tasks.yaml` and roles/capabilities in `config/agents.yaml`. Together, they collaborate as a self-sufficient team—capable of building production-level applications.

## Why This Matters

This project is a proof of concept that agentic AI can replicate and even replace entire engineering teams. Instead of simply answering questions or generating snippets, these agents:

- Collaborate like real engineers.
- Generate and execute working code.
- Build complete projects (UI + backend + DB).
- Deliver ready-to-run applications autonomously.

This is not just AI-assisted coding—it’s AI-driven engineering. A glimpse into the near future where whole departments can be replaced by agentic AI systems.


## Project Images 

![WhatsApp Image 2025-07-14 at 13 23 59_92c7339e](https://github.com/user-attachments/assets/ee01cf23-97c7-4ca4-ba0e-d05d5d9d0920)


![WhatsApp Image 2025-07-14 at 13 25 19_627acab7](https://github.com/user-attachments/assets/98d3e2ce-10f5-4aa0-85a0-844f27ed0537)


![WhatsApp Image 2025-07-14 at 13 25 28_b36e3843](https://github.com/user-attachments/assets/bddf5eb1-6cb7-4d2f-bc4a-d63bceae8763)


![WhatsApp Image 2025-07-14 at 13 25 54_9e7c3fb1](https://github.com/user-attachments/assets/34db3177-eb86-4016-88a0-f545356faf94)


![WhatsApp Image 2025-07-14 at 13 26 06_40fa6c26](https://github.com/user-attachments/assets/0c881fab-1d67-4dd9-9941-c84fd3da480e)


![WhatsApp Image 2025-07-14 at 13 26 35_0fb03862](https://github.com/user-attachments/assets/a6ef112a-f0d8-4bc8-80f7-e93c482309fa)


![WhatsApp Image 2025-07-14 at 13 26 58_1fcbda63](https://github.com/user-attachments/assets/fa3caedf-c9f9-4614-bd13-63f7f7d095cd)


![WhatsApp Image 2025-07-14 at 13 27 29_b69d6a77](https://github.com/user-attachments/assets/1c463a66-bf73-4ab3-850b-9bd6780802c9)


![WhatsApp Image 2025-07-14 at 13 27 43_4f6415b6](https://github.com/user-attachments/assets/90911cce-2047-47e0-8bc2-127af0956d26)


![WhatsApp Image 2025-07-14 at 13 27 43_e72cacf1](https://github.com/user-attachments/assets/80c43502-b8e7-4638-a81a-b48896cb70bd)


![WhatsApp Image 2025-07-14 at 13 28 18_04fc663f](https://github.com/user-attachments/assets/66f1656c-fa0b-492c-88ab-c16ef1ec9cbd)

## Output

![WhatsApp Image 2025-07-14 at 14 53 58_f5558aec](https://github.com/user-attachments/assets/45f4a45c-ea20-4606-bb85-33f9471cfaf1)


![WhatsApp Image 2025-07-14 at 14 54 11_8bcd96f8](https://github.com/user-attachments/assets/749e8460-262e-4e29-910f-b363b8d24d4e)


![WhatsApp Image 2025-07-14 at 14 54 23_37d99455](https://github.com/user-attachments/assets/43257024-9a2b-48e9-b56e-03128a8c1f9a)


## Made by 
Vishvvesh Nagappan
