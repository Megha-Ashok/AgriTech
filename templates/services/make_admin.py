import sqlite3

conn = sqlite3.connect('database.db')
cur  = conn.cursor()

# Promote this email to admin
admin_email = 'megha@1234'
cur.execute("""
    UPDATE users
    SET is_admin = 1
    WHERE email = ?
""", (admin_email,))

conn.commit()
print(f"Rows updated: {conn.total_changes}")

# Verify
cur.execute("SELECT name, email, is_admin FROM users WHERE email = ?", (admin_email,))
print(cur.fetchone())

conn.close()
