import streamlit as st
import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="",  
    database="grossary"
)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS groceries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    quantity INT NOT NULL,
                    price FLOAT NOT NULL)''')
conn.commit()


def get_groceries():
    cursor.execute("SELECT * FROM groceries")
    return cursor.fetchall()


def add_item(name, quantity, price):
    cursor.execute("INSERT INTO groceries (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    conn.commit()
    st.success("Item added successfully!")

# Function to delete an item
def delete_item(item_id):
    cursor.execute("DELETE FROM groceries WHERE id=%s", (item_id,))
    conn.commit()
    st.success("Item deleted successfully!")

st.title("🛒 Grocery Management System")


st.header("Add New Item")
with st.form("add_form"):
    name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price", min_value=1, step=1000)
    submitted = st.form_submit_button("Add Item")
    if submitted:
        add_item(name, quantity, price)


st.header("Grocery List")
groceries = get_groceries()
for item in groceries:
    with st.expander(f"{item[1]} (ID: {item[0]})"):
        st.write(f"Quantity: {item[2]}")
        st.write(f"Price: rs{item[3]:.2f}")
        if st.button(f"Delete {item[1]}", key=item[0]):
            delete_item(item[0])
            st.experimental_rerun()

# Close connection
cursor.close()
conn.close()


