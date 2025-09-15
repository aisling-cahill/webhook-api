import asyncpg
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def check_database_optimization():
    database_url = os.getenv('DATABASE_URL')

    conn = await asyncpg.connect(database_url)

    try:
        # Check if index exists on patient_phone
        index_query = """
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE tablename = 'appointments_cache'
        AND indexdef LIKE '%patient_phone%';
        """

        indexes = await conn.fetch(index_query)
        print("Indexes on patient_phone:")
        for idx in indexes:
            print(f"  - {idx['indexname']}: {idx['indexdef']}")

        if not indexes:
            print("❌ NO INDEX found on patient_phone column!")
            print("\nTo fix this, run in Supabase SQL editor:")
            print("CREATE INDEX idx_appointments_cache_patient_phone ON appointments_cache(patient_phone);")
        else:
            print("✅ Index exists on patient_phone")

        # Check table size
        size_query = """
        SELECT
            schemaname,
            tablename,
            attname,
            n_distinct,
            correlation
        FROM pg_stats
        WHERE tablename = 'appointments_cache'
        AND attname = 'patient_phone';
        """

        stats = await conn.fetchrow(size_query)
        if stats:
            print(f"\nTable stats:")
            print(f"  - Distinct phone numbers: {stats['n_distinct']}")
            print(f"  - Correlation: {stats['correlation']}")

    finally:
        await conn.close()

asyncio.run(check_database_optimization())