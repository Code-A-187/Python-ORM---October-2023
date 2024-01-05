from main import Session
from models import User
# Start a session
session = Session()
try:
# Begin a transaction
    session.begin()
# Perform database operations within the transaction
    session.query(User).delete()
# Commit the transaction
    session.commit()
    print('All users deleted successfully')

except Exception as e:
    # Rollback the transaction if an exception occurs
    session.rollback()
    print("An error occurred:", str(e))
finally:
    # Close the session
    session.close()