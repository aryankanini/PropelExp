import asyncio
from cms_planner.modules.extraction.job_runner import ExtractionJobRunner

async def test():
    runner = ExtractionJobRunner()
    job_id = runner.create_job()

    async def slow_work():
        await asyncio.sleep(0.1)

    asyncio.create_task(runner.run(job_id, slow_work()))

    # First connection - gets all events
    print("--- first connection ---")
    last_seen = 0
    async for ev in runner.stream_events(job_id, last_seen):
        print(f"  id={ev.event_id} terminal={ev.terminal_status}")
        last_seen = ev.event_id

    # Simulate reconnect after terminal (onerror fires after stream closes)
    print(f"--- reconnect with last_event_id={last_seen} ---")
    async for ev in runner.stream_events(job_id, last_seen):
        print(f"  id={ev.event_id} terminal={ev.terminal_status}")
    print("done")

asyncio.run(test())
