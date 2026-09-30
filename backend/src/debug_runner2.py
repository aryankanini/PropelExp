import asyncio
from cms_planner.modules.extraction.job_runner import ExtractionJobRunner

async def test():
    runner = ExtractionJobRunner()
    job_id = runner.create_job()

    async def slow_work():
        await asyncio.sleep(0.2)

    # Start job in background
    asyncio.create_task(runner.run(job_id, slow_work()))

    # SSE client connects immediately (before job finishes)
    print("--- stream_events output (client connects before job done) ---")
    async for ev in runner.stream_events(job_id, 0):
        print(f"  yielded id={ev.event_id} terminal={ev.terminal_status} percent={ev.percent}")
    print("done")

asyncio.run(test())
