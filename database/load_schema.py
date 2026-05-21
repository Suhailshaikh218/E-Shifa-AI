"""
Load database schema into Neon PostgreSQL
"""
import asyncio
import asyncpg
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

async def load_schema():
    """Load SQL schema into database"""
    
    # Read schema file
    schema_path = Path(__file__).parent / "mvp_schema.sql"
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    print("🔌 Connecting to Neon PostgreSQL...")
    
    # Connect to database
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("📋 Loading schema...")
        
        # Execute schema
        await conn.execute(schema_sql)
        
        print("✅ Schema loaded successfully!")
        
        # Verify tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
        
        # Count sample data
        users_count = await conn.fetchval("SELECT COUNT(*) FROM users_auth")
        providers_count = await conn.fetchval("SELECT COUNT(*) FROM providers")
        
        print(f"\n📦 Sample data loaded:")
        print(f"  - {users_count} users")
        print(f"  - {providers_count} providers")
        
    finally:
        await conn.close()
        print("\n🔌 Database connection closed")

if __name__ == "__main__":
    asyncio.run(load_schema())
