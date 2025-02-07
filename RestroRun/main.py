import kivy
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
import sqlite3
import requests

# Set mobile-friendly window size
Window.size = (360, 640)

item_prices = {
    "Chicken Burger": 5.99, "French Fries": 2.99, "Veg Pizza": 4.99,
    "Coke": 1.99, "Pasta Alfredo": 3.99, "Garlic Bread": 2.99, "Samosas": 2.50,
    "Mango Lassi": 3.50, "Burrito": 7.50, "Sushi Platter": 15.00,
    "Miso Soup": 4.50, "Tacos": 3.00, "Ramen": 10.00,
    "Chicken Curry": 9.50, "Cheeseburger": 6.50, "Pad Thai": 11.00
}

KV = '''
ScreenManager:
    id: screen_manager
    RestaurantScreen:
    MenuScreen:
    CartScreen:

<RestaurantScreen>:
    name: 'restaurant'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: '#F5F5F5'
        MDTopAppBar:
            title: 'Select Restaurant'
            elevation: 0
            md_bg_color: '#FFFFFF'
            specific_text_color: '#000000'
        ScrollView:
            MDList:
                spacing: '12dp'
                padding: '16dp'
                adaptive_height: True
                OneLineListItem:
                    text: 'George'
                    theme_text_color: 'Custom'
                    text_color: '#333333'
                    on_press: root.select_restaurant('George')
                    _no_ripple_effect: False
                OneLineListItem:
                    text: 'Sushi House'
                    theme_text_color: 'Custom'
                    text_color: '#333333'
                    on_press: root.select_restaurant('Sushi House')
                    _no_ripple_effect: False
                OneLineListItem:
                    text: 'Burger Joint'
                    theme_text_color: 'Custom'
                    text_color: '#333333'
                    on_press: root.select_restaurant('Burger Joint')
                    _no_ripple_effect: False

<MenuScreen>:
    name: 'menu'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: '#F5F5F5'
        MDTopAppBar:
            id: menu_toolbar
            title: 'Menu'
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [['cart-outline', lambda x: root.go_to_cart()]]
            elevation: 0
            md_bg_color: '#FFFFFF'
            specific_text_color: '#000000'
        ScrollView:
            MDList:
                id: menu_items
                spacing: '8dp'
                padding: '16dp'

<CartScreen>:
    name: 'cart'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: '#F5F5F5'
        MDTopAppBar:
            title: 'Cart'
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [['delete', lambda x: root.clear_cart()]]
            elevation: 0
            md_bg_color: '#FFFFFF'
            specific_text_color: '#000000'
        ScrollView:
            MDList:
                id: cart_items
                spacing: '8dp'
                padding: '16dp'
        MDBoxLayout:
            orientation: 'vertical'
            padding: '16dp'
            spacing: '16dp'
            MDLabel:
                id: total_label
                text: 'Total: $0.00'
                font_style: 'H6'
                halign: 'center'
            MDRaisedButton:
                text: 'Place Order'
                md_bg_color: '#4CAF50'
                text_color: '#FFFFFF'
                on_press: root.place_order()
                pos_hint: {'center_x': .5}
'''

class RestaurantScreen(MDScreen):
    def select_restaurant(self, restaurant):
        menu_screen = self.manager.get_screen('menu')
        menu_screen.current_restaurant = restaurant
        menu_screen.load_menu()
        self.manager.current = 'menu'

class MenuScreen(MDScreen):
    current_restaurant = None

    def load_menu(self):
        menu_list = self.ids.menu_items
        menu_list.clear_widgets()
        
        restaurant_menus = {
            'George': ['Chicken Burger', 'French Fries', 'Veg Pizza', 'Coke'],
            'Sushi House': ['Sushi Platter', 'Miso Soup', 'Tacos', 'Ramen'],
            'Burger Joint': ['Cheeseburger', 'Chicken Curry', 'Pad Thai']
        }
        
        for item in restaurant_menus.get(self.current_restaurant, []):
            menu_list.add_widget(
                OneLineListItem(
                    text=f'{item} - ${item_prices[item]:.2f}',
                    theme_text_color='Custom',
                    text_color='#333333',
                    on_press=lambda x, i=item: self.show_quantity_dialog(i)
                )
            )
        self.ids.menu_toolbar.title = f'{self.current_restaurant} Menu'

    def show_quantity_dialog(self, item):
        self.quantity_dialog = MDDialog(
            title=f"Add {item}",
            type="custom",
            content_cls=MDTextField(
                id="quantity_input",
                hint_text="Quantity",
                input_type="number"
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    text_color='#666666',
                    on_press=lambda x: self.quantity_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ADD",
                    md_bg_color='#4CAF50',
                    on_press=lambda x: self.add_to_cart(item, 
                        int(self.quantity_dialog.content_cls.text or 1))
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
            item_total = price * quantity
            total += item_total
            cart_list.add_widget(
                OneLineListItem(
                    text=f'{item} x{quantity} - ${item_total:.2f}',
                    theme_text_color='Custom',
                    text_color='#333333',
                    on_press=lambda x, i=item: self.remove_from_cart(i)
                )
            )

        self.ids.total_label.text = f'Total: ${total:.2f}'

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
        con = sqlite3.connect("./delivery.db")
        cur = con.cursor()

        cur.execute("SELECT MAX(order_id) FROM orders")
        last_order_id = cur.fetchone()[0]
        
        if last_order_id:
            order_number = f'ORD{int(last_order_id[3:]) + 1:04d}'
        else:
            order_number = 'ORD0001'

        for item, quantity in self.cart.items():
            cur.execute("""
                INSERT INTO orders (order_id, item, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (order_number, item, quantity, item_prices[item] * quantity))

        con.commit()
        con.close()

        try:
            response = requests.get('https://your-order-tracking-url.com/order')
            print(f"Order {order_number} placed successfully")
        except Exception as e:
            print(f"Error sending order: {e}")

        self.cart.clear()
        self.update_cart_view()
        self.manager.current = 'restaurant'

class DeliveryApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    DeliveryApp().run()