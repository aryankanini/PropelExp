import asyncio
from cms_planner.modules.extraction.job_runner import ExtractionJobRunner

async def test():
    runner = ExtractionJobRunner()
    job_id = runner.create_job()

    async def fast_work():
        pass

    await runner.run(job_id, fast_work())
    buf = runner._events.get(job_id, [])
    print(f"buffer len={len(buf)}")
    for e in buf:
        print(f"  id={e.event_id} terminal={e.terminal_status}")

    print("--- stream_events output ---")
    async for ev in runner.stream_events(job_id, 0):
        print(f"  yielded id={ev.event_id} terminal={ev.terminal_status}")
    print("done")

asyncio.run(test())
