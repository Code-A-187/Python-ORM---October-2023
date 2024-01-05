from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL
from sqlalchemy import create_engine
from models import User, Order

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# with Session() as session:
#     session.add_all([User(username='john_doe', email='john@example.com'), User(username='john_doe', email='john@example.com')])
#     session.commit()

# with Session() as session:
    # # Query the user you want to update
    # user_to_update = session.query(User).filter_by(username='john_doe').first()
    # print(user_to_update)
    # # Update the user's information
    # if user_to_update:
    #     user_to_update.email = 'new_email@example.com'
    #     session.commit()
    #     print("User updated successfully")
    # else:
    #     print("User not found")

# with Session() as session:
#     # Query the user you want to delete
#     user_to_delete = session.query(User).filter_by(username='john_doe').first()
#     # Delete the user
#     if user_to_delete:
#         session.delete(user_to_delete)
#         session.commit()
#         print("User deleted successfully")
#     else:
#         print("User not found")


# def populate_order_table():
#     with Session() as session:
#         session.add_all((Order(user_id=5), Order(user_id=6)))
#
#         session.commit()
#
# populate_order_table()

with Session() as session:
    orders = session.query(Order).order_by(Order.user_id.desc()).all()
    # print(orders)
    if not orders:
        print('No orders in the database')
    else:
        for order in orders:
            print(order.user.email)
            print(f'order id {order.id} is completed {order.is_completed} for user {order.user.username}')
        # print([(order.id, order.user_id) for order in orders])