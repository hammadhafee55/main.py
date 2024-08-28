from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from plyer import filechooser
from kivy.utils import platform
import os

# Ensure the font file path is correct
font_path = "Roboto-Regular.ttf"
if not os.path.isfile(font_path):
    print(f"Font file not found at {font_path}. Please ensure the file is in the correct location.")
else:
    LabelBase.register(name="Roboto", fn_regular=font_path)

class IngredientInput(BoxLayout):
    def __init__(self, **kwargs):
        super(IngredientInput, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = None
        self.height = 40

        # Product Name
        self.ingredient_name = TextInput(hint_text="Product Name", size_hint_x=0.5)
        self.add_widget(self.ingredient_name)

        # Quantity
        self.ingredient_quantity = TextInput(hint_text="Quantity", size_hint_x=0.25)
        self.add_widget(self.ingredient_quantity)

        # Price
        self.ingredient_price = TextInput(hint_text="Price", size_hint_x=0.25)
        self.add_widget(self.ingredient_price)

class RecipeBook(BoxLayout):
    def __init__(self, **kwargs):
        super(RecipeBook, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Title
        self.header = Label(text="Recipe Book", font_size='24sp', font_name="Roboto", size_hint=(1, 0.1), halign='center')
        self.add_widget(self.header)

        # Add name input
        self.name_input = TextInput(hint_text="Enter name of the person", size_hint=(1, 0.1))
        self.add_widget(self.name_input)

        # Ingredients section
        self.ingredients_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        self.add_widget(self.ingredients_layout)

        # Add initial ingredient input
        self.add_ingredient_input()

        # Button to add more ingredient inputs
        self.add_ingredient_btn = Button(text="Add Ingredient", size_hint=(1, 0.1), background_color=(0.2, 0.6, 0.9, 1))
        self.add_ingredient_btn.bind(on_press=self.add_ingredient_input)
        self.add_widget(self.add_ingredient_btn)

        # Button to generate recipe
        self.generate_btn = Button(text="Generate Recipe", size_hint=(1, 0.1), background_color=(0.4, 0.8, 0.6, 1))
        self.generate_btn.bind(on_press=self.generate_recipe)
        self.add_widget(self.generate_btn)

        # Recipe output
        self.recipe_output = Label(text="Generated Recipe will appear here.", size_hint=(1, 0.2), font_name="Roboto")
        self.add_widget(self.recipe_output)

        # Button to download recipe
        self.download_btn = Button(text="Download Recipe", size_hint=(1, 0.1), background_color=(0.9, 0.4, 0.4, 1))
        self.download_btn.bind(on_press=self.download_recipe)
        self.add_widget(self.download_btn)

        # Footer
        self.footer = Label(text="Created by Hammad Hafeez Daula", size_hint=(1, 0.1), halign='center', font_name="Roboto", color=(0.5, 0.5, 0.5, 1))
        self.add_widget(self.footer)

    def add_ingredient_input(self, instance=None):
        ingredient_input = IngredientInput()
        self.ingredients_layout.add_widget(ingredient_input)

    def generate_recipe(self, instance):
        if self.ingredients_layout.children:
            recipe = f"Recipe for {self.name_input.text}:\n"
            total_price = 0.0
            
            for ingredient in self.ingredients_layout.children[::-1]:  # Reverse to match input order
                name = ingredient.ingredient_name.text
                quantity = ingredient.ingredient_quantity.text
                price_text = ingredient.ingredient_price.text
                
                try:
                    price = float(price_text)
                except ValueError:
                    price = 0.0
                
                total_price += price
                
                if name and quantity and price:
                    recipe += f"{name} - {quantity} - Rs {price:.2f}\n"
            
            # Add total price to the recipe
            recipe += f"\nTotal Price: Rs {total_price:.2f}"
            
            self.recipe_output.text = recipe
        else:
            self.recipe_output.text = "Add some ingredients first!"

    def download_recipe(self, instance):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
        
        if self.recipe_output.text:
            path = filechooser.save_file(title="Save Recipe", filters=["*.txt"])
            if path:
                with open(path[0], 'w') as file:
                    file.write(self.recipe_output.text)
                self.recipe_output.text = "Recipe saved successfully."
            else:
                self.recipe_output.text = "Save operation canceled."

class RecipeBookApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Set background color
        return RecipeBook()

if __name__ == '__main__':
    RecipeBookApp().run()
