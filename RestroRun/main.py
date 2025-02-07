import kivy
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.clock import Clock
import sqlite3
import requests

# Register the custom font (ensure the file is in your project directory)
LabelBase.register(name="Quicksand", fn_regular=r"C:\Users\ASUS\Downloads\Quicksand\Quicksand-VariableFont_wght.ttf")

# Set mobile-friendly window size
Window.size = (360, 640)

# Use a common icon for all food items
common_food_icon = "silverware-fork-knife"

# -------------------------------
# Data dictionaries for the app
# -------------------------------

# Prices for each dish
item_prices = {
    # George (Family-style diner)
    "Chicken Burger": 5.99,
    "French Fries": 2.99,
    "Veg Pizza": 4.99,
    "Coke": 1.99,
    "Pasta Alfredo": 7.50,
    "Garlic Bread": 3.50,
    "Samosas": 2.50,
    # Sushi House
    "Sushi Platter": 15.00,
    "Miso Soup": 4.50,
    "Tempura": 8.00,
    "Sashimi": 12.00,
    "Ramen": 10.00,
    "Edamame": 5.00,
    "Green Tea Ice Cream": 4.00,
    # Burger Joint
    "Cheeseburger": 6.50,
    "Bacon Burger": 7.99,
    "Veggie Burger": 6.99,
    "Chicken Burger": 6.50,  # Available at both George and Burger Joint
    "Onion Rings": 3.99,
    "Crispy Fries": 3.50,
    "Milkshake": 4.50
}

# Descriptions for each dish
item_descriptions = {
    # George
    "Chicken Burger": "Juicy grilled chicken burger with a crispy exterior.",
    "French Fries": "Golden, crispy fries served with ketchup.",
    "Veg Pizza": "A colorful medley of fresh vegetables on a classic crust.",
    "Coke": "Chilled soda to refresh your palate.",
    "Pasta Alfredo": "Creamy pasta with rich Alfredo sauce.",
    "Garlic Bread": "Toasted bread with garlic butter and herbs.",
    "Samosas": "Crispy pastry filled with spiced potatoes and peas.",
    # Sushi House
    "Sushi Platter": "An assorted platter of fresh sushi and sashimi.",
    "Miso Soup": "Warm and soothing traditional miso soup.",
    "Tempura": "Lightly battered and fried vegetables and shrimp.",
    "Sashimi": "Assorted fresh raw fish, sliced thinly.",
    "Ramen": "Hearty noodles in a savory broth, perfect for any day.",
    "Edamame": "Steamed young soybeans sprinkled with salt.",
    "Green Tea Ice Cream": "Refreshing ice cream with a subtle matcha flavor.",
    # Burger Joint
    "Cheeseburger": "Classic cheeseburger with all the fixings.",
    "Bacon Burger": "Juicy burger topped with crispy bacon and cheese.",
    "Veggie Burger": "A hearty burger made with a blend of vegetables.",
    "Chicken Burger": "Tender chicken burger with a flavorful twist.",
    "Onion Rings": "Crispy, golden rings of onion with a tangy dip.",
    "Crispy Fries": "Extra crispy fries seasoned to perfection.",
    "Milkshake": "Creamy and indulgent milkshake available in various flavors."
}

# Menus available per restaurant
restaurant_menus = {
    "George": [
        "Chicken Burger", "French Fries", "Veg Pizza",
        "Coke", "Pasta Alfredo", "Garlic Bread", "Samosas"
    ],
    "Sushi House": [
        "Sushi Platter", "Miso Soup", "Tempura",
        "Sashimi", "Ramen", "Edamame", "Green Tea Ice Cream"
    ],
    "Burger Joint": [
        "Cheeseburger", "Bacon Burger", "Veggie Burger",
        "Chicken Burger", "Onion Rings", "Crispy Fries", "Milkshake"
    ]
}

# Descriptions for restaurants
restaurant_descriptions = {
    "George": "Family-style diner serving classic American comfort food.",
    "Sushi House": "Experience the art of sushi with the freshest ingredients.",
    "Burger Joint": "Gourmet burgers crafted with passion and quality."
}

# ----------------------------------
# KV Layout including Splash Screen
# ----------------------------------
KV = '''
#:import dp kivy.metrics.dp

ScreenManager:
    id: screen_manager
    SplashScreen:
    RestaurantScreen:
    MenuScreen:
    CartScreen:

<SplashScreen>:
    name: 'splash'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        md_bg_color: "#1976D2"
        MDLabel:
            text: "Welcome to Delivery App"
            halign: "center"
            theme_text_color: "Custom"
            text_color: "#FFFFFF"
            font_name: "Quicksand"
            font_style: "H3"
        MDLabel:
            text: "Loading..."
            halign: "center"
            theme_text_color: "Custom"
            text_color: "#FFFFFF"
            font_name: "Quicksand"
            font_style: "Subtitle1"

<RestaurantScreen>:
    name: 'restaurant'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        md_bg_color: "#F5F5F5"
        MDTopAppBar:
            title: 'Select Restaurant'
            elevation: 4
            md_bg_color: '#1976D2'
            specific_text_color: '#FFFFFF'
            font_name: "Quicksand"
        ScrollView:
            MDCard:
                orientation: 'vertical'
                size_hint: None, None
                size: root.width - dp(20), self.minimum_height
                padding: dp(10)
                spacing: dp(10)
                md_bg_color: "#FFFFFF"
                radius: [10,]
                elevation: 4
                MDList:
                    id: restaurant_list
                    spacing: dp(10)
                    TwoLineAvatarListItem:
                        text: "George"
                        secondary_text: "Family-style diner serving classic American comfort food."
                        font_name: "Quicksand"
                        on_press: root.select_restaurant("George")
                        IconLeftWidget:
                            icon: "storefront"
                    TwoLineAvatarListItem:
                        text: "Sushi House"
                        secondary_text: "Experience the art of sushi with the freshest ingredients."
                        font_name: "Quicksand"
                        on_press: root.select_restaurant("Sushi House")
                        IconLeftWidget:
                            icon: "storefront"
                    TwoLineAvatarListItem:
                        text: "Burger Joint"
                        secondary_text: "Gourmet burgers crafted with passion and quality."
                        font_name: "Quicksand"
                        on_press: root.select_restaurant("Burger Joint")
                        IconLeftWidget:
                            icon: "storefront"

<MenuScreen>:
    name: 'menu'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        md_bg_color: "#F5F5F5"
        MDTopAppBar:
            id: menu_toolbar
            title: "Menu"
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [['cart-outline', lambda x: root.go_to_cart()]]
            elevation: 4
            md_bg_color: '#1976D2'
            specific_text_color: '#FFFFFF'
            font_name: "Quicksand"
        ScrollView:
            MDCard:
                orientation: 'vertical'
                size_hint: None, None
                size: root.width - dp(20), self.minimum_height
                padding: dp(10)
                spacing: dp(10)
                md_bg_color: "#FFFFFF"
                radius: [10,]
                elevation: 4
                MDList:
                    id: menu_items
                    spacing: dp(10)

<CartScreen>:
    name: 'cart'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        md_bg_color: "#F5F5F5"
        MDTopAppBar:
            title: 'Cart'
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [['delete', lambda x: root.clear_cart()]]
            elevation: 4
            md_bg_color: '#1976D2'
            specific_text_color: '#FFFFFF'
            font_name: "Quicksand"
        ScrollView:
            MDCard:
                orientation: 'vertical'
                size_hint: None, None
                size: root.width - dp(20), self.minimum_height
                padding: dp(10)
                spacing: dp(10)
                md_bg_color: "#FFFFFF"
                radius: [10,]
                elevation: 4
                MDList:
                    id: cart_items
                    spacing: dp(10)
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            MDLabel:
                id: total_label
                text: 'Total: $0.00'
                font_style: 'H6'
                halign: 'center'
                font_name: "Quicksand"
            MDRaisedButton:
                text: 'Place Order'
                md_bg_color: '#4CAF50'
                text_color: '#FFFFFF'
                font_name: "Quicksand"
                on_press: root.place_order()
                pos_hint: {'center_x': .5}
'''

# -------------------------
# Python Classes for Screens
# -------------------------
class SplashScreen(MDScreen):
    def on_enter(self):
        # Automatically switch to the restaurant screen after 3 seconds
        Clock.schedule_once(self.switch_to_restaurant, 3)

    def switch_to_restaurant(self, dt):
        # Check if the manager is available and switch screens safely
        if self.manager:
            self.manager.current = 'restaurant'
        else:
            print("Error: ScreenManager is not available.")

class RestaurantScreen(MDScreen):
    def select_restaurant(self, restaurant):
        # Set the selected restaurant and load its menu
        menu_screen = self.manager.get_screen('menu')
        menu_screen.current_restaurant = restaurant
        menu_screen.load_menu()
        self.manager.current = 'menu'

class MenuScreen(MDScreen):
    current_restaurant = None

    def load_menu(self):
        menu_list = self.ids.menu_items
        menu_list.clear_widgets()
        # Set the toolbar title to include the restaurant name
        self.ids.menu_toolbar.title = f"{self.current_restaurant} Menu"
        # Get the menu items for the selected restaurant
        for item in restaurant_menus.get(self.current_restaurant, []):
            # Create a two-line list item with name, price, and description
            list_item = TwoLineAvatarListItem(
                text=f"{item} - ${item_prices[item]:.2f}",
                secondary_text=item_descriptions.get(item, ""),
                font_name="Quicksand",
                on_press=lambda x, i=item: self.show_quantity_dialog(i)
            )
            list_item.add_widget(IconLeftWidget(icon=common_food_icon))
            menu_list.add_widget(list_item)

    def show_quantity_dialog(self, item):
        # Create a dialog to ask for quantity
        self.quantity_dialog = MDDialog(
            title=f"Add {item}",
            type="custom",
            content_cls=MDTextField(
                id="quantity_input",
                hint_text="Quantity",
                input_type="number",
                font_name="Quicksand"
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    text_color='#666666',
                    font_name="Quicksand",
                    on_press=lambda x: self.quantity_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ADD",
                    md_bg_color='#4CAF50',
                    font_name="Quicksand",
                    on_press=lambda x: self.add_to_cart(item, int(self.quantity_dialog.content_cls.text or 1))
                )
            ]
        )
        self.quantity_dialog.open()

    def add_to_cart(self, item, quantity):
        cart_screen = self.manager.get_screen('cart')
        cart_screen.add_to_cart(item, quantity)
        self.quantity_dialog.dismiss()
        self.manager.current = 'cart'

    def go_back(self):
        self.manager.current = 'restaurant'

    def go_to_cart(self):
        self.manager.current = 'cart'

class CartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = {}
        self.create_orders_table()
        self.confirmation_dialog = None

    def create_orders_table(self):
        con = sqlite3.connect("./delivery.db")
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT,
                item TEXT,
                quantity INTEGER,
                price REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        con.commit()
        con.close()

    def add_to_cart(self, item, quantity):
        self.cart[item] = self.cart.get(item, 0) + quantity
        self.update_cart_view()

    def update_cart_view(self):
        cart_list = self.ids.cart_items
        cart_list.clear_widgets()
        total = 0

        for item, quantity in self.cart.items():
            price = item_prices[item]
            subtotal = price * quantity
            total += subtotal
            list_item = TwoLineAvatarListItem(
                text=f"{item}",
                secondary_text=f"Quantity: {quantity}  |  Subtotal: ${subtotal:.2f}",
                font_name="Quicksand",
                on_press=lambda x, i=item: self.remove_from_cart(i)
            )
            list_item.add_widget(IconLeftWidget(icon=common_food_icon))
            cart_list.add_widget(list_item)

        self.ids.total_label.text = f"Total: ${total:.2f}"

    def remove_from_cart(self, item):
        if item in self.cart:
            self.cart[item] -= 1
            if self.cart[item] == 0:
                del self.cart[item]
            self.update_cart_view()

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_view()

    def go_back(self):
        self.manager.current = 'menu'

    def place_order(self):
        # Generate a new order number based on the last order in the DB
        con = sqlite3.connect("./delivery.db")
        cur = con.cursor()

        cur.execute("SELECT MAX(order_id) FROM orders")
        last_order_id = cur.fetchone()[0]
        if last_order_id:
            order_number = f"ORD{int(last_order_id[3:]) + 1:04d}"
        else:
            order_number = "ORD0001"

        # Insert each item from the cart into the orders table
        for item, quantity in self.cart.items():
            cur.execute("""
                INSERT INTO orders (order_id, item, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (order_number, item, quantity, item_prices[item] * quantity))

        con.commit()
        con.close()

        # Optionally, send the order to a remote server (example URL)
        try:
            response = requests.get('https://your-order-tracking-url.com/order')
            print(f"Order {order_number} placed successfully")
        except Exception as e:
            print(f"Error sending order: {e}")

        # Clear the cart and update the view
        self.cart.clear()
        self.update_cart_view()

        # Show a friendly confirmation dialog with order details
        self.confirmation_dialog = MDDialog(
            title="Order Placed!",
            text=(f"Your order {order_number} has been placed.\n"
                  "Estimated delivery time: 30 minutes.\n\nEnjoy your meal!"),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    md_bg_color='#4CAF50',
                    text_color='#FFFFFF',
                    font_name="Quicksand",
                    on_press=lambda x: self.close_confirmation_dialog()
                )
            ],
            font_name="Quicksand"
        )
        self.confirmation_dialog.open()

    def close_confirmation_dialog(self):
        self.confirmation_dialog.dismiss()
        self.manager.current = 'restaurant'

class DeliveryApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

if __name__ == '__main__':
    DeliveryApp().run()
