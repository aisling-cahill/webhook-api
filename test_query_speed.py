import asyncpg
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()

async def test_query_speed():
    database_url = os.getenv('DATABASE_URL')

    # Test connection time
    start = time.time()
    conn = await asyncpg.connect(database_url)
    connect_time = (time.time() - start) * 1000
    print(f"Connection time: {connect_time:.1f}ms")

    try:
        # Test query time
        start = time.time()
        result = await conn.fetchrow("""
            SELECT *
            FROM public.appointments_cache
            WHERE patient_phone = $1
            ORDER BY appointment_time DESC
            LIMIT 1;
        """, "+353857688030")
        query_time = (time.time() - start) * 1000
        print(f"Query time: {query_time:.1f}ms")

        print(f"Total time: {connect_time + query_time:.1f}ms")
        print(f"Found result: {result is not None}")

    finally:
        await conn.close()

asyncio.run(test_query_speed())