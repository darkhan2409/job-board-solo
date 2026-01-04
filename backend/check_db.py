import sqlite3

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM jobs')
jobs_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM companies')
companies_count = cursor.fetchone()[0]

print(f'✅ Database Statistics:')
print(f'   Jobs: {jobs_count}')
print(f'   Companies: {companies_count}')

cursor.execute('SELECT title, location, salary FROM jobs LIMIT 5')
print(f'\n📋 Sample jobs:')
for row in cursor.fetchall():
    print(f'   - {row[0][:50]}... | {row[1]} | {row[2] or "Not specified"}')

conn.close()
