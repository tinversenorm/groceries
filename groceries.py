from yaml import load
from datetime import datetime
from markdown import markdown
from markdown_checklist.extension import ChecklistExtension
import argparse

def main(args):
	# Load all recipes as dicts into recipes list.
	recipe_file_list = args.recipes
	recipes = read_recipes(recipe_file_list)

	# Create a list of ingredients with aggregate amounts to output.
	# The structure is "ingredientName" => { "oz" => 5 } (unitType => amount)
	groceries = aggregate_groceries(recipes)

	list_of_groceries = pretty_print(groceries)
	html_list = markdown(list_of_groceries, extensions=[ChecklistExtension()])
	gl_filename = f'grocery_list_{datetime.today().strftime("%Y_%m_%d")}'
	with open(f'{gl_filename}.md', 'w') as grocery_file:
		grocery_file.write(list_of_groceries)
	with open(f'{gl_filename}.html', 'w') as grocery_html:
		grocery_html.write(html_list)

	print(f'List in file {gl_filename}')

def read_recipes(recipe_filenames):
	recipes = []
	for recipe_filename in recipe_filenames:
		with open(recipe_filename, 'r') as recipe_file:
			recipes.append(load(recipe_file))
	return recipes

# recipes is a list of dicts containing information about the ingredients of each rßcipe.
def aggregate_groceries(recipes):
	groceries = {}
	for recipe in recipes:
		for ingredient in recipe['ingredients']:
			amounts = groceries.setdefault(ingredient['name'], {})
			if "type" not in ingredient or ingredient['type'] != "seasoning":
				unitAmt = amounts.setdefault(ingredient['unit'], 0)
				amounts[ingredient['unit']] = unitAmt + ingredient.get('quantity', 0)
	return groceries


def pretty_print(groceries):
	title = f"## Grocery list for {datetime.today().strftime('%Y_%m_%d')}:"
	items = []
	for ingredient_name in groceries:
		amounts = []
		for unit in groceries[ingredient_name]:
			amounts.append(f'{groceries[ingredient_name][unit]} {unit}')
		items.append(f'* [ ] {ingredient_name}, {", ".join(amounts)}')
	return title + "\n" + "\n".join(items)

def create_parser():
	parser = argparse.ArgumentParser(
		description="Takes recipe yaml files and outputs a grocery list")
	parser.add_argument("recipes", type=str, nargs='+', help="list of recipe yaml files")
	return parser


if __name__ == '__main__':
	args = create_parser().parse_args()
	main(args)
