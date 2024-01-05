from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers import session_decorator
from models import Recipe, Chef

engine = create_engine('postgresql+psycopg2://postgres-user:password@localhost/sql_alchemy_db_exercise')
Session = sessionmaker(bind=engine)

session = Session()


@session_decorator(session)
def create_recipe(name: str, ingredients: str, instructions: str):
    new_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions,
    )

    session.add(new_recipe)

@session_decorator(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str):
    records_changed = (
        session.query(Recipe)
        .filter_by(name=name)
        .update({
            Recipe.name: new_name,
            Recipe.ingredients: new_ingredients,
            Recipe.instructions: new_instructions
        })
    )

    # recipe_to_update= session.query(Recipe).filter_by(name=name).first()
    #
    # recipe_to_update.name = new_name
    # recipe_to_update.ingredients = new_ingredients
    # recipe_to_update.instructions = new_instructions

    return records_changed


@session_decorator(session)
def delete_recipe_by_name(name: str):
    changed_records: int = (
        session.query(Recipe)
        .filter_by(name=name)
        .delete()
    )

    return changed_records


@session_decorator(session)
def get_recipes_by_ingredient(ingredient_name: str):
    recipies_with_ingredient = (
        session.query(Recipe)
        .filter(Recipe.ingredients.ilike(f'%{ingredient_name}%'))
        .all()
        )

    return recipies_with_ingredient


@session_decorator(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str):
    first_recipe = (
        session.query(Recipe)
        .filter_by(name=first_recipe_name)
        .with_for_update()
        .one()
    )

    second_recipe = (
        session.query(Recipe)
        .filter_by(name=second_recipe_name)
        .with_for_update()
        .one()
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@session_decorator(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str):
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()

    if recipe and recipe.chef:
        return f'Recipe: {recipe_name} already has a related chef'

    chef = session.query(Chef).filter_by(name=chef_name).first()

    recipe.chef = chef

    return f'Related recipe {recipe_name} with chef {chef_name}'


@session_decorator(session)
def get_recipes_with_chef():
    recipes_with_chef = (
        session.query(Recipe.name, Chef.name.label('chef_name'))
        .join(Chef, Recipe.chef)
        .all()
    )

    return '\n'.join(
        f'Recipe: {recipe_name} made by chef: {chef_name}'
        for recipe_name, chef_name in recipes_with_chef
    )

# Delete all objects (recipes and chefs) from the database
session.query(Recipe).delete()
session.query(Chef).delete()
session.commit()

# Create chef instances
chef1 = Chef(name="Gordon Ramsay")
chef2 = Chef(name="Julia Child")
chef3 = Chef(name="Jamie Oliver")
chef4 = Chef(name="Nigella Lawson")

# Create recipe instances associated with chefs
recipe1 = Recipe(name="Beef Wellington", ingredients="Beef fillet, Puff pastry, Mushrooms, Foie gras", instructions="Prepare the fillet and encase it in puff pastry.")
recipe1.chef = chef1

recipe2 = Recipe(name="Boeuf Bourguignon", ingredients="Beef, Red wine, Onions, Carrots", instructions="Slow-cook the beef with red wine and vegetables.")
recipe2.chef = chef2

recipe3 = Recipe(name="Spaghetti Carbonara", ingredients="Spaghetti, Eggs, Pancetta, Cheese", instructions="Cook pasta, mix ingredients.")
recipe3.chef = chef3

recipe4 = Recipe(name="Chocolate Cake", ingredients="Chocolate, Flour, Sugar, Eggs", instructions="Bake a delicious chocolate cake.")
recipe4.chef = chef4

recipe5 = Recipe(name="Chicken Tikka Masala", ingredients="Chicken, Yogurt, Tomatoes, Spices", instructions="Marinate chicken and cook in a creamy tomato sauce.")
recipe5.chef = chef3

session.add_all([chef1, chef2, chef3, chef4, recipe1, recipe2, recipe3, recipe4, recipe5])
session.commit()
print(get_recipes_with_chef())
