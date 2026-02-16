"""Entry point: python -m marketing.run"""

import asyncio

from marketing.agent import run_agent_cycle


def main():
    asyncio.run(run_agent_cycle())


if __name__ == "__main__":
    main()
