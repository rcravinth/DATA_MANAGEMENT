import streamlit as st
import pandas as pd
import pymysql as sql
import re
import datetime
import plotly.express as px

st.header("ZOMATA DATA ENTRY")

# Method to establish sql connection
def connect_db():
    try:
        connection = sql.connect(
            host="localhost",          # MySQL server host
            user="root",               # MySQL username
            password="mysql",          # MySQL password
            database="zomata",         # MySQL database name
        )
        return connection
    except sql.MySQLError as e:
        print(f"Error: {e}")

#Method to add customer data in customer table (tuple)
def add_customer_data(customer):
    try:
        connection = connect_db() #Establish db connection
        cursor = connection.cursor()
        check_customer_query = "select count(*) from customer where name = %s" #To ensure whether the customer already exist or not
        cursor.execute(check_customer_query,(customer[0],)) #customer[0] is customr id
        if cursor.fetchone()[0] > 0:
            st.error("Customer name Already exists")
            return False
        #Query to insert customer data
        insert_customer = """insert into customer(name,email,phone,location,signup_date,is_premium,preferred_cuisine,total_orders,average_rating) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(insert_customer,[customer]) #Passing the list for placeholder
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            #Close established sql connection to free up the connection
            cursor.close()
            connection.close() 

#Method to update customer details (dictionary,int)
def update_customer_data(customer,customer_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #iterate the dictionary keys to update the specific column values
        set_clause = ", ".join([f"{column} = %s" for column in customer.keys()])
        #Adding values and criteria value in list to replace the placeholder
        values = list(customer.values())
        values.append(customer_id)  # Append the order_id for the WHERE condition
        update_customer_query = f"UPDATE customer SET {set_clause} WHERE customer_id = %s" #Update query for customer data
        cursor.execute(update_customer_query,values)
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to add new rstaurant data (tuple)
def add_restaurant_data(restaurant):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        check_restaurant_query = "select count(*) from restaurant where name = %s" #Query ensure whether the restaurat data already present or not
        cursor.execute(check_restaurant_query,(restaurant[0],))
        if cursor.fetchone()[0]>0:
            st.error("Restaurant name already exists")
            return False
        #Insert query to add data in restaurant table
        insert_restaurant = """insert into restaurant(name,cuisine_type,location,owner_name,average_delivery_time_min,contact_number,rating,total_orders,is_active)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(insert_restaurant,[restaurant])
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to update existing restaurant data (dictionary,int)
def update_restaurant_data(restaurant,restaurant_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Iterate the dictionary keys to update the specific columns
        set_clause = ", ".join([f"{column} = %s" for column in restaurant.keys()])
        values = list(restaurant.values())
        values.append(restaurant_id)  # Append the order_id for the WHERE condition
        update_restaurant_query = f"UPDATE restaurant SET {set_clause} WHERE restaurant_id = %s" #Update query for restaurant data
        cursor.execute(update_restaurant_query,values)
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to add delivery person data (tuple)
def add_delivery_person_data(person):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        check_person_query = "select count(*) from delivery_person where name = %s" #Ensure whether the delivery person is already exist
        cursor.execute(check_person_query,(person[0],))
        if cursor.fetchone()[0]>0:
            st.error("Delivery Person name already exists") 
            return False
        #Insert query for delivery person
        insert_person = """insert into delivery_person(name,contact_number,total_deliveries,average_rating,location)
        values(%s,%s,%s,%s,%s)"""
        cursor.executemany(insert_person,[person])
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to update delivery person (dictionary,int)
def update_delivery_person_data(delivery_person,delivery_person_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Iterate the dictionary keys to update the specific columns
        set_clause = ", ".join([f"{column} = %s" for column in delivery_person.keys()]) 
        values = list(delivery_person.values())
        values.append(delivery_person_id)  # Append the order_id for the WHERE condition
        update_delivery_person_query = f"UPDATE delivery_person SET {set_clause} WHERE delivery_person_id = %s" #Update query for delivery person data
        cursor.execute(update_delivery_person_query,values)
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to add new order data
def add_order_data(order):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Insert query to add data in orders table
        insert_order_query = """insert into orders(customer_id,restaurant_id,order_date,delivery_time,status,total_amount,payment_mode,discount_applied,feedback_rating)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(insert_order_query,[order])
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to add delivery data
def add_delivery_data(delivery):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Insert query add data in delivery table
        insert_delivery_query = """insert into delivery(order_id,delivery_person_id,delivery_status,distance_in_km,delivery_time_min,estimated_time_min,delivery_fee,vehicle_type)
        values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(insert_delivery_query,[delivery])
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the all customer name list
def get_customer_list():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        get_customer_list_query = "select name from customer" #Query to get all customer name
        cursor.execute(get_customer_list_query)
        customer_list = [row[0] for row in cursor.fetchall()] #convert the tuple data to list data #Iterate the first index of the tuple data
        return customer_list #return customer name in list
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the all restaurant name list
def get_restaurant_list():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        get_restaurant_list_query = "select name from restaurant" #Query get restaurant name 
        cursor.execute(get_restaurant_list_query)
        restaurant_list = [row[0] for row in cursor.fetchall()] #convert the tuple data to list data #Iterate the first index of the tuple data
        return restaurant_list #return restaurant name in list
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get all th order list
def get_order_list():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        get_order_list_query = "select order_id from orders" #Query to get all order
        cursor.execute(get_order_list_query)
        order_list = [row[0] for row in cursor.fetchall()] #convert the tuple data to list data #Iterate the first index of the tuple data
        return order_list #return order id in list
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the delivery person name list
def get_delivery_person_name():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        get_deliveryperson_query = "select name from delivery_person" #Query to get all delivery person name
        cursor.execute(get_deliveryperson_query)
        delivery_person_name = [row[0] for row in cursor.fetchall()] #convert the tuple data to list data #Iterate the first index of the tuple data
        return delivery_person_name #return delivery person name in list
    except sql.MySQLError as e:
        st.write()
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get all and specific customer details
def get_customer_detail(name):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        if name == 'none':
            get_customerid_query = "select * from customer" #Query to get all the customer details
            cursor.execute(get_customerid_query)
            customer_detail = cursor.fetchall()
        else:
            get_customerid_query = "select * from customer where name = %s" #Query to get specific customer details
            cursor.execute(get_customerid_query,(name,)) # Pass the customer name in query
            customer_detail = cursor.fetchone()
        return customer_detail
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get specific restaurant details
def get_restaurant_detail(name):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        get_restaurantid_query = "select * from restaurant where name = %s" # Query to get specific restaurant details
        cursor.execute(get_restaurantid_query,(name,)) # Pass the restaurant name in query
        restaurant_detail = cursor.fetchone()
        return restaurant_detail
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the specific delivery person details
def get_delivery_person_detail(name):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        get_person_id_query = "select * from delivery_person where name = %s" # Query to et the specific delivery person details
        cursor.execute(get_person_id_query,(name,)) #Pass the delivery person name in query 
        delivery_person_detail = cursor.fetchone()
        return delivery_person_detail
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
        
#Method to delete existing customer data
def delete_customer_data(id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Before removing the parent table need to remove the child table data to due to foriegn key constraints
        get_order_id = "select order_id from orders where customer_id = %s"  #Query to get the order for specific customer id
        cursor.execute(get_order_id,(id,))
        order_id = cursor.fetchall()
        order_list = [x[0] for x in order_id]
        placeholders = ', '.join(['%s'] * len(order_list))
        delete_delivery_query = f"delete from delivery where order_id in ({placeholders})" #Query to remove the order data, The ordr table has the orders id as foriegn key which reference orders table
        cursor.execute(delete_delivery_query,tuple(order_list))
        delete_order_query = "delete from orders where customer_id = %s" #Query to remove the order data, The ordr table has the customer id as foriegn key which reference customer table
        cursor.execute(delete_order_query,(id,))
        delete_customer_query = "delete from customer where customer_id = %s" #Query to remove customer data
        cursor.execute(delete_customer_query,(id,))
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Query to delte restaurant data
def delete_restaurant_data(id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Before removing the parent table need to remove the child table data to due to foriegn key constraints
        get_order_id = "select order_id from orders where restaurant_id = %s" #Query to get order id for specific restaurant id data
        order_id = cursor.fetchall()
        order_list = [x[0] for x in order_id]
        placeholders = ', '.join(['%s'] * len(order_list))
        delete_delivery_query = f"delete from delivery where order_id in ({placeholders})" #Query to remove the delivery data, The ordr table has the orders id as foriegn key which reference orders table
        cursor.execute(get_order_id,(id,))
        cursor.execute(delete_delivery_query,tuple(order_list))
        delete_order_query = "delete from orders where restaurant_id = %s"
        cursor.execute(delete_order_query,(id,))
        delete_restaurant_query = "delete from restaurant where restaurant_id = %s"
        cursor.execute(delete_restaurant_query,(id,))
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Query to remove delivery person data
def delete_delivery_person_data(id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        delete_delivery_query = "delete from delivery where delivery_person_id = %s" #Query to remove the order data, The ordr table has the orders id as foriegn key which reference orders table
        cursor.execute(delete_delivery_query,(id,))
        delete_delivery_person_query = "delete from delivery_person where delivery_person_id = %s" #Query to remove the delivery person data
        cursor.execute(delete_delivery_person_query,(id,))
        connection.commit()
        return True
    except sql.MySQLError as e:
        st.write(e)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get top orders based on the location
def top_order_by_location():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        order_count_query = "select location,sum(total_orders) as orders from customer group by location order by orders desc limit 10" #Query to get the top 10 orders based on the location
        cursor.execute(order_count_query)
        top_order = cursor.fetchall()
        return top_order
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the delayed deliveries
def delayed_delivery_list():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get the delayed deliveries based on which delivery time is more than estimated delivery time
        delay = "select estimated_time_min,delivery_time_min,delivery_person.name from delivery inner join delivery_person on delivery_person.delivery_person_id = delivery.delivery_person_id where estimated_time_min<delivery_time_min order by (delivery_time_min-estimated_time_min) desc limit 10;"
        cursor.execute(delay)
        top_delay = cursor.fetchall()
        return top_delay
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get cuisine wise total orders
def cuisinewise_total_orders():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get the cuisine type and total orders for that cuisine
        cuisinewsie = "select cuisine_type,sum(total_orders) as orders from restaurant group by cuisine_type order by orders desc;"
        cursor.execute(cuisinewsie)
        cuisinewise_total_orders = cursor.fetchall()
        return cuisinewise_total_orders
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the rank value based on customer order value count
def rank_by_customer_order_value():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Use rank function to assign rank for customer based on total amount
        customer_rank_query = "select customer.name as Customer_Name,sum(orders.total_amount) as Amount,dense_rank() over (order by sum(orders.total_amount) desc) as 'Rank' from customer inner join orders on orders.customer_id = customer.customer_id group by orders.customer_id limit 10;"
        cursor.execute(customer_rank_query)
        customer_rank = cursor.fetchall()
        return customer_rank
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the delivery person total deliveries
def get_delivery_person_total_deliveries():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get delivery person name, total deliveries
        total_deliveries_query = "select name,total_deliveries from delivery_person order by total_deliveries desc limit 10;"
        cursor.execute(total_deliveries_query)
        total_deliveries = cursor.fetchall()
        return total_deliveries
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get average delivery time of delivery person
def get_avg_del_time():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get the delivery person name and Average delivery time
        avg_del_time_query = "select distinct name, avg(delivery.delivery_time_min) over (partition by delivery.delivery_person_id) as avg_del_time from delivery_person inner join delivery on delivery.delivery_person_id = delivery_person.delivery_person_id order by avg_del_time;"
        cursor.execute(avg_del_time_query)
        avg_del_time = cursor.fetchall()
        return avg_del_time
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get average delivery time based on location
def get_average_delivery_time_for_location():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get delivery person name, ordered location,average delivery time
        avg_del_location_query = "select distinct delivery_person.name,customer.location as Location,avg(delivery.delivery_time_min) over (partition by delivery.delivery_person_id,customer.location) as avg_del_time from delivery_person inner join delivery on delivery.delivery_person_id = delivery_person.delivery_person_id inner join orders on orders.order_id = delivery.order_id inner join customer on customer.customer_id = orders.customer_id order by avg_del_time;"
        cursor.execute(avg_del_location_query)
        avg_del_location = cursor.fetchall()
        return avg_del_location
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to restaurant yearly total orders of the restuarant
def get_res_tot_orders_per_year():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get order year, restaurant name, total orders based on year
        tot_orders_per_year_query = "select year(order_date) as Year,restaurant.name as name,count(order_id) as total_orders from orders inner join restaurant on restaurant.restaurant_id = orders.restaurant_id group by Year,restaurant.name ORDER BY Year, total_orders DESC;"
        cursor.execute(tot_orders_per_year_query)
        tot_orders_per_year = cursor.fetchall()
        return tot_orders_per_year
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the delivery status
def get_delivery_status():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get the delivery status and its count
        delivery_status_query = "select delivery_status, count(delivery_id) as count from delivery group by delivery_status;"
        cursor.execute(delivery_status_query)
        delivery_status = cursor.fetchall()
        return delivery_status
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Method to get the top 10 restaurant based on total orders
def top_restauarant():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get restaurant name, Total orders
        top_order_restauarant_query = "select restaurant.name,total_orders from restaurant order by total_orders desc limit 10;"
        cursor.execute(top_order_restauarant_query)
        top_order_restaurant = cursor.fetchall()
        return top_order_restaurant
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

#Mthod to get the top 10 restaurant by order values
def top_restaurant_value():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        #Query to get the restaurant name, total order amount
        top_restaurant_value_query = "select restaurant.name as Name, sum(orders.total_amount) as Total_amount from restaurant inner join orders on orders.restaurant_id = restaurant.restaurant_id group by orders.restaurant_id order by Total_amount desc limit 10;"
        cursor.execute(top_restaurant_value_query)
        top_value_restauarant = cursor.fetchall()
        return top_value_restauarant
    except sql.MySQLError as e:
        st.write(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

st.sidebar.subheader("DATA UPDATE") #Sidebar subheader

#Intruce side bar button
add = st.sidebar.button("ADD NEW ENTRY") #Button to open the add entry form
update = st.sidebar.button("DATA UPDATE") #Button to open the data update form
delete = st.sidebar.button("DELETE DATA") #Button to delte the existing data form
st.sidebar.subheader("DATA ANALYSIS") #sidebar subheader
analysis = st.sidebar.button("DATA INSIGHTS") #Button to open data anlaysis page

# Initialize session state variables for form visibility and selection
if "show_form" not in st.session_state:
    st.session_state["show_form"] = None

if add:
    st.session_state["show_form"] = "Add new"
    st.session_state["update_form"] = False
elif update:
    st.session_state["show_form"] = "Data update"
    st.session_state["add_form"] = False
elif delete:
    st.session_state["show_form"] = "Delete data"
    st.session_state["add_form"] = False
elif analysis:
    st.session_state["show_form"] = "Data Insights"
    st.session_state["delete_form"] = False
    st.session_state["update_form"] = False
    st.session_state["add_form"] = False

pattern = r"^[6-9]\d{9}$"  # Phone number must start with 6, 7, 8, or 9 and be 10 digits long

#Page to open add entry
if st.session_state["show_form"]=="Add new":           
    st.subheader("ADD NEW ENTRY")
    form_type = st.selectbox("Choose the form to display", ["Select", "Customer", "Restaurant","Delivery Person","Order","Delivery"]) # Dropdown to select the type of entry
    #Customer entry form
    if form_type=='Customer': 
        if 'customer_form_data' not in st.session_state:
            #initiate the session state for customer form data
            st.session_state.customer_form_data = {'customer_name': '', 'Email': '','phone_number': '','Email': '','location': '','signup': '','premium': '','preferred_cuisine': '','total_orders': '','avg_rating': ''}
        #Enter into customer form
        with st.form(key='customer_form'):
            customer_name = st.text_input("Customer Name", max_chars=30) #For customer name field maximum characters is 30
            Email = st.text_input("Email")
            phone_number = st.text_input("Phone number", placeholder="e.g., 9876543210")
            location = st.text_input("Location",max_chars=40) #For location field maximum characters is 30
            signup = st.date_input("Signup Date")
            premium = st.radio("Premium",['YES','NO'],index = 1) #Radio button to select the customer is premium or not
            #Convert this Yes or no data to 0 or 1 for db data updation
            if premium == 'NO': is_premium = 0
            else : is_premium = 1 
            preferred_cuisine = st.selectbox("Preferred Cuisine",['Indian','Chinese','Italian','Mexican','Thai','Japanese']) #Introduce select box for cuisine type selection
            total_orders = st.number_input("Total Orders",min_value=0,step=1) #Total orders field minimum value is 0 and step is 1
            avg_rating = st.slider("Average Rating",min_value=1.0,max_value=5.0,step=0.5) #Slider to select rating. Average rating field minimum value is 1.0 and step is 0.5 and stop value 5.0
            submit = st.form_submit_button("Submit") #Button to submit the form
            if submit:
                #check customer name is empty or not, If empty show error in console
                if not customer_name.strip(): 
                    st.error("Customer name cannot be empty.")
                #check location is empty or not, If empty show error in console
                elif not location.strip(): 
                    st.error("Location cannot be empty")
                #Regex validation for mobile number
                elif not re.fullmatch(pattern,phone_number): 
                    st.error("Invalid phone number. It should start with 6-9 and be 10 digits long.")     
                else:
                    #Process customer data and call method to add customer data
                    customer = (customer_name,Email,phone_number,location,signup,is_premium,preferred_cuisine,total_orders,avg_rating)
                    success = add_customer_data(customer) 
                    if success:
                        st.success("Form submitted successfully! You can add another entry.")
                    else:
                        st.error("Data updation failed")
    
    #Restaurant entry form
    if form_type=='Restaurant':
        if 'restaurant_form_data' not in st.session_state:
            #initiate the session state for restaurant form
            st.session_state.restaurant_form_data = {'restaurant_name':'','cuisine_type':'','location':'','owner_name':'','avg_del_time_min':'','contact_number':'','rating':'','total_orders':'','is_active':''}    
        #Enter into restaurant form
        with st.form(key='restaurant_form'):
            restaurant_name = st.text_input("Restaurant Name",max_chars=40)
            cuisine_type = st.selectbox("Cuisine Type",['Indian','Chinese','Italian','Mexican','Thai','Japanese'])
            location = st.text_input("Location",max_chars=40)
            owner_name = st.text_input("Owner Name",max_chars=30)
            avg_del_time_min = st.slider("Average Delivery time(Mins)",min_value=10,max_value=60)
            contact_number = st.text_input("Contact Number", placeholder="e.g., 9876543210")
            rating = st.slider("Average Rating",min_value=1.0,max_value=5.0,step=0.5)
            total_orders = st.number_input("Total Orders",min_value=0,step=1)
            is_active = st.radio("Active Customer",['YES','NO'],index = 1)
            if is_active == 'NO': is_active = 0
            else : is_active = 1
            submit = st.form_submit_button("Submit")
            if submit:
                if not restaurant_name.strip():
                    st.error("Restaurant name should not be empty")
                elif not location.strip():
                    st.error("location Cannot be empty")
                elif not owner_name.strip():
                    st.error("owner name cannot be empty")
                elif not re.fullmatch(pattern,contact_number):
                    st.error("Invalid phone number. It should start with 6-9 and be 10 digits long.")
                else:
                    #Process restaurant data and call method to add rstaurant data
                    restaurant = (restaurant_name,cuisine_type,location,owner_name,avg_del_time_min,contact_number,rating,total_orders,is_active)
                    success = add_restaurant_data(restaurant)
                    if success:
                        st.success("Form submitted successfully! You can add another entry")
                    else:
                        st.error("Data updation failed")

    #Delivery person entry form
    if form_type=='Delivery Person':
        if 'delivery_person_form_data' not in st.session_state:
            #initiate the session state for delivery person data
            st.session_state.delivery_person_form_data = {'person_name':'','contact_number':'','total_deliveries':'','rating':'','location':''}
        #Enter into delivery person form
        with st.form(key='delivery_person_form'):
            person_name = st.text_input("Delivery Person Name",max_chars=30)
            contact_number = st.text_input("Contact Number", placeholder="e.g., 9876543210")
            total_deliveries = st.number_input("Total Deliveries",min_value=0,step=1)
            rating = st.slider("Rating",min_value=0.0,max_value=5.0,step=0.5)
            location = st.text_input("Location",max_chars=40)
            submit = st.form_submit_button("Submit")
            if submit:
                if not person_name.strip():
                    st.error("Delivery person name cannot be empty")
                elif not re.fullmatch(pattern,contact_number):
                    st.error("Invalid phone number. It should start with 6-9 and be 10 digits long.")
                else:
                    #Process delivery person data and call method to add delivery person data
                    person = (person_name,contact_number,total_deliveries,rating,location)
                    success = add_delivery_person_data(person)
                    if success:
                        st.success("Form submitted successfully! You can add another entry")
                    else:
                        st.error("Data updation failed")

    #Order entry form
    if form_type=='Order':
        if 'order_form_data' not in st.session_state:
            #initiate the order form data
            st.session_state.order_form_data = {'customer_name':'','restaurant_name':'','order_date':'','delivery_time':'','status':'','total_amount':'','payment_mode':'','discount_applied':'','feedback_rating':'',}
        #Enter into order form
        with st.form(key='order_form'):
            customer = get_customer_list() #Get the customer name list
            customer_name = st.selectbox("Customer name",customer,None) #Drop down customer name to select
            customer_id = get_customer_detail(customer_name) #Get thecustomer id by passing the customer name
            restaurant = get_restaurant_list() #get restaurant name list
            restaurant_name = st.selectbox("Restaurant name",restaurant,None) #Drop down restaurant name to select
            restaurant_id = get_restaurant_detail(restaurant_name) #Get the restaurant id passing the restaurant name
            ord_date = st.date_input("Order Date")
            order_time = st.time_input("Order time")
            order_date = datetime.datetime.combine(ord_date, order_time) # Combine both input date and time
            delivery_time = st.time_input("Delivery time")
            delivery_time = datetime.datetime.combine(ord_date, delivery_time)
            status = st.radio("Status",['Pending','Delivered','Cancelled'],index=0)
            total_amount = st.number_input("Total amount",format="%0.2f",min_value=0.00) #field to update to total amount with two decimal value 
            payment_mode = st.radio("Payment Mode",['Card','Cash','UPI','Netbanking'],index=1) 
            discount_applied = st.number_input("Discount Applied",format="%0.2f",min_value=0.00)
            feedback_rating = st.slider("Feedback Rating", min_value=0.0, max_value=5.0,step=0.5)
            submit = st.form_submit_button("Submit")
            if submit:
                if customer_name==None:
                    st.error("Please select customer name")
                elif restaurant_name==None:
                    st.error("Please select restaurant name")
                elif total_amount<=0.00:
                    st.error("Amount cannot be empty")
                else:
                    #Process order data and call method to add order data
                    order = (customer_id[0],restaurant_id[0],order_date,delivery_time,status,total_amount,payment_mode,discount_applied,feedback_rating)
                    success = add_order_data(order)
                    if success:
                        st.success("Form submitted successfully! You can add another entry")
                    else:
                        st.error("Data Updation failed")
            
    #Delivery entry form
    if form_type == 'Delivery':
        if 'delivery_form_data' not in st.session_state:
            #initiate the delivery person form data
            st.session_state.delivery_form_data = {'order_id':'','delivery_person_name':'','delivery_status':'','distance_in_km':'','delivery_time_min':'','estimated_time_min':'','delivery_fee':'','vehicle_type':''}
        with st.form(key='delivery_form'):
            order_id = get_order_list()
            order = st.selectbox("Order Id",order_id)
            delivery_person = get_delivery_person_name() # get all delivery person name
            delivery_person_name = st.selectbox("Delivery Person",delivery_person,None) #Drop down the delivery person name to select
            delivery_person_id = get_delivery_person_detail(delivery_person_name)
            delivery_status = st.radio("Delivery Status",['Pending','Delivered','Cancelled'],index=0)
            distance_in_km = st.number_input("Distance (KM)",min_value=1,max_value=30,step=2)
            del_in_min = st.slider("Delivery time(Mins)",min_value=10,max_value=60)
            est_del_time = st.slider("Estmiated Delivery Time(Mins)",min_value=10,max_value=60)
            delivery_fee = st.number_input("Delivery Fees",format="%0.2f",min_value=0.00)
            vehicle_type = st.radio("Vehicle_type",['Bike','Cycle','Car'])
            submit = st.form_submit_button("Submit")
            if submit:
                if delivery_person_name==None :
                    st.error("Please select restaurant name")
                else:
                    #Process delivery data and call method to add delivery data
                    delivery = (order,delivery_person_id[0],delivery_status,distance_in_km,del_in_min,est_del_time,delivery_fee,vehicle_type)
                    success = add_delivery_data(delivery)
                    if success:
                        st.success("Form submitted succcessfully! You can add another entry")
                    else:
                        st.error("Data updation failed")

#Page to open Data update
elif st.session_state["show_form"] == "Data update":          
    st.subheader("EXISTING DATA UPDATE")   
    # Dropdown to select the type of entry
    form_type = st.selectbox("Choose the form to display", ["Select", "Customer", "Restaurant","Delivery Person"])
    if form_type=='Customer':
        #Initiate the session state for customer data update
        if 'customer_form_data' not in st.session_state:
            st.session_state.customer_form_data = {'customer': '', 'name': '','email': '','contact_number': '','location': '','premium': '','total_orders': '','avg_rating': ''}
        #Enter into customer data update form
        with st.form(key='customer1_form'):
            customer_list = get_customer_list() #get the customer list name 
            customer = st.selectbox("Choose customer name",customer_list) #Drop down the customer name to select 
            show_user = st.form_submit_button("Show user data") #submit button to shows the selected customer details
            if show_user: 
                customer_detail = get_customer_detail(customer)
                customer_detail = list(customer_detail) # Convert the dictionary to list
                customer_detail[9] = float(customer_detail[9])  # Convert Decimal to float
                cus_columns = ['Customer id', 'Name', 'Email', 'Contact Number', 'Location', 'Signup Date', 'Premium', 'Cuisine Type', 'Total Orders', 'Average Rating']
                customer_dataframe = pd.DataFrame(customer_detail,cus_columns) #Convert the fetched dataframe
                # Store the fetched data in session state to retain the fetched data
                st.session_state['customer_data'] = customer_dataframe
            if 'customer_data' in st.session_state:
                customer_dataframe = st.session_state['customer_data']
                cx_transpose = customer_dataframe.transpose().rename_axis("Values") # transform the row to column and column to row and rename the axis
                st.dataframe(cx_transpose,hide_index=True) #shows the dataframe in streamlit app
                #Store the dataframe values to new variable
                customer_id = cx_transpose['Customer id'][0] 
                customer_name = cx_transpose['Name'][0]
                email = cx_transpose['Email'][0]
                contact_number = cx_transpose['Contact Number'][0]
                location = cx_transpose['Location'][0]
                premium = cx_transpose['Premium'][0]
                total_orders = cx_transpose['Total Orders'][0]
                avg_rating = cx_transpose['Average Rating'][0]
                #shows the fecthed value in streamlit app form field
                name = st.text_input("Customer Name",value=customer_name)
                email = st.text_input("Email",value=email)
                contact_number = st.text_input("Contact Number",value=contact_number)
                location = st.text_input("Locaton",value=location)
                premium = st.text_input("Preium",value=premium)
                st.write("0 = False, 1 = True") # showing the value reference in console
                total_orders = st.text_input("Total Orders",value=total_orders)
                average_rating = st.text_input("Average Rating",value=avg_rating)
                update = st.form_submit_button("Submit")
                if update:
                    if not customer_name.strip():
                        st.error("Customer name cannot be empty.")
                    elif not location.strip():
                        st.error("Location cannot be empty")
                    elif not re.fullmatch(pattern,contact_number):
                        st.error("Invalid phone number. It should start with 6-9 and be 10 digits long.")
                    elif not premium in ('0','1'):
                        st.error("Premium should be zero or one")
                    else:
                        #Process the data and passing the dictionary values to method to update the data in DB
                        update_customer = {"name":name,"email":email,"phone":contact_number,"location":location,"is_premium":premium,"total_orders":total_orders,"average_rating":average_rating}
                        success = update_customer_data(update_customer,customer_id)
                        if success:
                            st.success("Form submitted successfully! You can add another entry.")
                        else:
                            st.error("Data updation failed")

    if form_type=='Restaurant':
        if 'restaurant_form_data' not in st.session_state:
            #Initiate the session state for restaurant data update
            st.session_state.restaurant_form_data = {'name': '','location': '','owner': '','avg_del_time': '','contact_number': '','rating': '','total_orders': '','active':''}
        #Ener into restaurant form
        with st.form(key='restaurant1_form'):
            restaurant_list = get_restaurant_list() #get the restaurant name list for selection
            restaurant = st.selectbox("Choose restaurant name",restaurant_list)
            show_restaurant = st.form_submit_button("Show restaurant data")
            if show_restaurant:
                restaurant_detail = get_restaurant_detail(restaurant) #get the selected restaurant complete details for updation
                restaurant_detail = list(restaurant_detail)
                restaurant_detail[7] = float(restaurant_detail[7])  # Convert Decimal to float
                res_columns = ['Restaurant id', 'Name', 'Cuisine Type', 'Location', 'Owner Name', 'Average Delivery Time', 'Contact Number', 'Rating', 'Total Orders', 'Is Active']
                restaurant_dataframe = pd.DataFrame(restaurant_detail, res_columns)
                # Store the fetched data in session state to retain the fetched data
                st.session_state['restaurant_data'] = restaurant_dataframe # submit button will open the update fprm
            if 'restaurant_data' in st.session_state:
                #change the column and row value in data frame
                restaurant_dataframe = st.session_state['restaurant_data']
                res_transpose = restaurant_dataframe.transpose().rename_axis("Values")
                st.dataframe(res_transpose,hide_index=True)
                #store the datframe data to new variable
                restaurant_id = res_transpose['Restaurant id'][0]
                restaurant_name = res_transpose['Name'][0]
                location = res_transpose['Location'][0]
                owner = res_transpose['Owner Name'][0]
                avg_del_time = res_transpose['Average Delivery Time'][0]
                contact_number = res_transpose['Contact Number'][0]
                rating = res_transpose['Rating'][0]
                total_orders = res_transpose['Total Orders'][0]
                active = res_transpose['Is Active'][0]
                #shows the fetched value in streamlit app form field
                name = st.text_input("Restaurant Name",value=restaurant_name)          
                location = st.text_input("Locaton",value=location)
                owner = st.text_input("Owner Name",value=owner)
                avg_del_time = st.text_input("Average Delivery Time",value=avg_del_time)
                contact_number = st.text_input("Contact Number",value=contact_number)
                rating = st.text_input("Rating",value=rating)
                total_orders = st.text_input("Total Orders",value=total_orders)
                active = st.text_input("Active",value=active)
                st.write("0 = False, 1 = True")
                update1 = st.form_submit_button("Submit")
                if update1:
                    if not name.strip():
                        st.error("Restaurant name cannot be empty.")
                    elif not location.strip():
                        st.error("Location cannot be empty")
                    elif not re.fullmatch(pattern,contact_number):
                        st.error("Invalid phone number. It should start with 6-9 and be 10 digits long.")
                    elif not active in ('0','1'):
                        st.error("Active should be zero or one")
                    else:
                        #Process the data and passing the value as dictionary to update the data in DB
                        update_restaurant = {"name":name,"owner_name":owner,"contact_number":contact_number,"location":location,"is_active":active,"total_orders":total_orders,"rating":rating,"average_delivery_time_min":avg_del_time}
                        success = update_restaurant_data(update_restaurant,restaurant_id)
                        if success:
                            st.success("Form submitted successfully! You can add another entry.")
                        else:
                            st.error("Data updation failed")
    if form_type=='Delivery Person':
        if 'delivery_form_data' not in st.session_state:
            #Initiate the session state for delivery person data update
            st.session_state.delivery_form_data = {'name': '','location': '','owner': '','avg_del_time': '','contact_number': '','rating': '','total_orders': '','active':''}
        # Enter delivery person update form 
        with st.form(key='delivery1_form'):
            del_per_list = get_delivery_person_name() #get delivery person name to shows the list in drop down
            delivery_person = st.selectbox("Choose Delivery Person Name",del_per_list)
            show_person = st.form_submit_button("Show Delivery Person data")
            if show_person:
                person_detail = get_delivery_person_detail(delivery_person) #get selected delivery person details
                person_detail = list(person_detail)
                person_detail[4] = float(person_detail[4])  # Convert Decimal to float
                per_columns = ['Delivery Person Id', 'Name', 'Contact Number', 'Total Deliveries', 'Average Rating', 'Location']
                person_dataframe = pd.DataFrame(person_detail, per_columns)
                # Store the fetched data in session state to retain the fetched data
                st.session_state['person_data'] = person_dataframe
            if 'person_data' in st.session_state:
                person_dataframe = st.session_state['person_data']
                per_transpose = person_dataframe.transpose().rename_axis("Values")
                st.dataframe(per_transpose,hide_index=True)
                # update the dataframe data into new variables
                delivery_person_id = per_transpose['Delivery Person Id'][0]
                delivery_person_name = per_transpose['Name'][0]
                location = per_transpose['Location'][0]
                contact_number = per_transpose['Contact Number'][0]
                rating = per_transpose['Average Rating'][0]
                total_deliveries = per_transpose['Total Deliveries'][0]
                # shows the fetched data in steamlit app console form fields for update
                name = st.text_input("Delivery Person Name",value=delivery_person_name)    
                contact_number = st.text_input("Contact Number",value=contact_number)      
                location = st.text_input("Locaton",value=location)
                rating = st.text_input("Average Rating",value=rating)
                total_deliveries = st.text_input("Total Deliveries",value=total_deliveries)
                update2 = st.form_submit_button("Submit")
                if update2:
                    if not name.strip():
                        st.error("Restaurant name cannot be empty.")
                    elif not location.strip():
                        st.error("Location cannot be empty")
                    elif not re.fullmatch(pattern,contact_number):
                        st.error("Invalid phone number. It should start with 6-9 and be 10 digits long.")
                    else:
                        #Process the data and update the data in db
                        update_delivery_person = {"name":name,"contact_number":contact_number,"location":location,"total_deliveries":total_deliveries,"average_rating":rating}
                        success = update_delivery_person_data(update_delivery_person,delivery_person_id)
                        if success:
                            st.success("Form submitted successfully! You can add another entry.")
                        else:
                            st.error("Data updation failed")

#Enter into Delete entry form
elif st.session_state["show_form"] == "Delete data":          
    st.subheader("DELETE DATA")   
    # Dropdown to select the type of entry
    form_type = st.selectbox("Choose the form to display", ["Select", "Customer", "Restaurant","Delivery Person"])
    if form_type=='Customer':
        if 'customer_form_data' not in st.session_state:
            st.session_state.customer_form_data = {'customer': ''}
        #Enter into customer delete form
        with st.form(key='customer1_form'):
            customer_list = get_customer_list() #Get the customer list to select for deletion
            customer = st.selectbox("Choose customer name",customer_list)
            customer_id = get_customer_detail(customer) #get selected customer id
            submit = st.form_submit_button("Delete")
            if submit:
                #Delete selected customer details from db
                success = delete_customer_data(customer_id[0])
                if success:
                    st.success(f"{customer} removed successfully!")
                else:
                    st.error("Data deletion failed")
    if form_type=='Restaurant':
        if 'restaurant_form_data' not in st.session_state:
            st.session_state.restaurant_form_data = {'restaurant': ''}
        #Enter into restaurant delete form
        with st.form(key='restaurant1_form'):
            restaurant_list = get_restaurant_list() #Get the restaurant list to select for deletion
            restaurant = st.selectbox("Choose restaurant name",restaurant_list)
            restaurant_id = get_restaurant_detail(restaurant) #get selected restaurant id
            submit = st.form_submit_button("Delete") 
            if submit:
                #Delete selected restaurant details from the db
                success = delete_restaurant_data(restaurant_id[0])
                if success:
                    st.success(f"{restaurant} removed successfully!")
                else:
                    st.error("Data deletion failed")
    if form_type=='Delivery Person':
        if 'delivery_person_form_data' not in st.session_state:
            st.session_state.delivery_person_form_data = {'restaurant': ''}
        #Enter into delivery person delte form
        with st.form(key='person1_form'):
            delivery_person_list = get_delivery_person_name() #get delivery person name to select for deletion
            delivery_person = st.selectbox("Choose delivery person name",delivery_person_list)
            delivery_person_id = get_delivery_person_detail(delivery_person) #ge selected delivery person id
            submit = st.form_submit_button("Delete")
            if submit:
                #Delete selected delivery person details from db
                success = delete_delivery_person_data(delivery_person_id[0])
                if success:
                    st.success(f"{delivery_person} removed successfully!")
                else:
                    st.error("Data deletion failed")

#Enter into Data insights page
elif st.session_state["show_form"] == "Data Insights":
    customer_detail = get_customer_detail('none') #Get the all customer details from db
    col = {0:'Customer id', 1:'Name', 2:'Email', 3:'Contact Number', 4:'Location', 5:'Signup Date', 6:'Premium', 7:'Cuisine Type', 8:'Total Orders', 9:'Average Rating'}
    customer_dataframe = pd.DataFrame(customer_detail)
    customer_dataframe.rename(columns=col,inplace=True) #rename the datframe column name 
    sorted = customer_dataframe.sort_values(by="Total Orders",ascending=False) #sorting the data based on total orders
    top10_customer = sorted.head(10) #ge top 10 data only
    st.subheader("Chart of Top 10 customers based on order frequency")
    st.bar_chart(data=top10_customer,x="Name",y="Total Orders") #bar chart for customer vs order count

    st.subheader("Customer Rank by order value")
    customer_rank = rank_by_customer_order_value() #get the customer order value with rank data
    cx_rank = pd.DataFrame(customer_rank)
    cx_rank.rename(columns={0:'Customer Name',1:'Order Value',2:'Rank'},inplace=True) #rename the dataframe column names
    st.dataframe(cx_rank,hide_index=True) #shows thw data set in stramlit console

    st.subheader("Top 10 delivery person by number of deliveries")
    del_per_deliveries = get_delivery_person_total_deliveries() #get delivery person name and total deliveries
    tot_del = pd.DataFrame(del_per_deliveries)
    tot_del.rename(columns={0:'Delivery Person Name',1:'Total Deliveries'},inplace=True) #rename the dataframe column names
    st.bar_chart(data=tot_del,x='Delivery Person Name',y='Total Deliveries') #bar chart for delivery person name vs Total deliveries

    top_order_by_location = top_order_by_location() #get location and total orders
    tobl = pd.DataFrame(top_order_by_location) 
    tobl.rename(columns={0:'Location',1:'Total Orders'},inplace=True) #rename the dataframe column names
    sorted = tobl.sort_values(by="Total Orders",ascending=False) #sort dataframe data based on total orders
    sorted['Total Orders'] = sorted['Total Orders'].astype(int) #convert the total orders data type to integer
    st.subheader("Top 10 orders by location")
    st.bar_chart(data=sorted,x="Location",y="Total Orders") #bar chart for location vs total orders

    st.subheader("Top 10 Restaurant by orders")
    top_res = top_restauarant() #get data restaurant name and total orders
    tot_restaurant = pd.DataFrame(top_res)
    tot_restaurant.rename(columns={0:'Restaurant Name',1:'Total Orders'},inplace=True) #rename the dataframe column names
    st.bar_chart(data=tot_restaurant,x='Restaurant Name',y='Total Orders') #bar chart for restaurant name vs total orders

    st.subheader("Top 10 Restaurant By revenue")
    top_res_value = top_restaurant_value() #get data restaurant name and order value
    top_restaurant_val = pd.DataFrame(top_res_value)
    top_restaurant_val.rename(columns={0:'Restaurant Name',1:'Total Order Amount'},inplace=True) #rename the dataframe column values
    top_restaurant_val['Total Order Amount'] = top_restaurant_val['Total Order Amount'].astype(int) #convert the total order amount type to integer
    st.bar_chart(data=top_restaurant_val,x='Restaurant Name',y='Total Order Amount') #bar chart for restaurant name vs total order amount

    st.subheader("Reataurant total orders per year")
    tot_orders_per_year = get_res_tot_orders_per_year() #get data of resturant name, order year, total orders
    total_orders_per_year = pd.DataFrame(tot_orders_per_year)
    total_orders_per_year.rename(columns={0:'Year',1:'Restaurant Name',2:'Total Orders'},inplace=True) #rename the dataframe column values
    total_orders_per_year['Total Orders'] = total_orders_per_year['Total Orders'].astype(int) #convert the total order type to integret
    pivot_table = pd.pivot(columns="Restaurant Name",index="Year",values="Total Orders",data = total_orders_per_year) #restructure the dataframe
    fig = px.imshow(pivot_table,labels=dict(x="Restaurant Name", y="Year", color="Total Orders"),color_continuous_scale='blues') #form the heatmap
    fig.update_layout(width=500,height=800) #hetamp layout
    fig.update_traces(hovertemplate='%{x}<br>%{y}<br>Total Oredrs Per Year %{z:.2f}') #define what are the values will be showing for hoverover the heatmap
    st.plotly_chart(fig) #Plot the chart in streamlit

    cuisinewise_totalorders = cuisinewise_total_orders() #get data cuisine type and total orders
    cuisine = pd.DataFrame(cuisinewise_totalorders)
    cuisine.rename(columns={0:'Cuisine Type',1:'Total Orders'},inplace=True) #rename the datframe column name
    cuisine['Total Orders'] = cuisine['Total Orders'].astype(int) # change the total orders data type
    st.subheader("Cuisine type wise Total orders")
    st.bar_chart(data=cuisine,x="Cuisine Type",y="Total Orders") # bar chart for cuisine type vs total orders

    st.subheader("Delivery persons average delivery time")
    avg_del_time = get_avg_del_time() #get delivery person name and average delivery time
    person_avg_del_time = pd.DataFrame(avg_del_time)
    person_avg_del_time.rename(columns={0:'Delivery Person Name',1:'Average Delivery Time in minutes'},inplace=True) #rename the dataframe column name 
    person_avg_del_time['Average Delivery Time in minutes'] = person_avg_del_time['Average Delivery Time in minutes'].astype(int) #convert the delivery time type to integer
    st.bar_chart(data=person_avg_del_time,x='Delivery Person Name',y='Average Delivery Time in minutes') #bar chart delivery person name vs average delivery time in minutes

    st.subheader("Average Delivery Time by Delivery Person and Location")
    avg_del_time_location = get_average_delivery_time_for_location() #get delivery person name, order location, average delivery time
    average_delivery_time = pd.DataFrame(avg_del_time_location)
    average_delivery_time.rename(columns={0:'Delivery Person',1:'Location',2:'Average Delivery Time'},inplace=True)
    average_delivery_time['Average Delivery Time'] = average_delivery_time['Average Delivery Time'].astype(int)
    pivot_table = pd.pivot(columns="Delivery Person",index="Location",values="Average Delivery Time",data = average_delivery_time) #recontruct the dataframe
    fig = px.imshow(pivot_table,labels=dict(x="Delivery Person", y="Delivery Location", color="Average Delivery Time"),color_continuous_scale='blackbody') #dfine the data in heatmap
    fig.update_layout(width=500,height=800)
    fig.update_traces(hovertemplate='%{x}<br>%{y}<br>Average Delivery Time: %{z:.2f}') #define what are the values will be showing for hoverover the heatmap
    st.plotly_chart(fig)

    st.subheader("Delivery status")
    delivery_status = get_delivery_status() #get delivery status and count
    del_status = pd.DataFrame(delivery_status)
    del_status.rename(columns={0:'Delivery Status',1:'Order Count'},inplace=True) #rename the dataframe column name
    fig = px.pie(del_status, values='Order Count', names='Delivery Status') #define the data for pie chart
    st.plotly_chart(fig) #plot the pie chart

    cuisinewise_totalorders = cuisinewise_total_orders() #get the cuisine type and total orders
    cuisine = pd.DataFrame(cuisinewise_totalorders)
    cuisine.rename(columns={0:'Cuisine Type',1:'Total Orders'},inplace=True) #convert the dataframe column name
    cuisine['Total Orders'] = cuisine['Total Orders'].astype(int)
    st.subheader("Cuisine type wise Total orders")
    st.bar_chart(data=cuisine,x="Cuisine Type",y="Total Orders") #bar chart cuisine type vs Total orders

   
