from yaml import load
from datetime import datetime
from markdown import markdown
from markdown_checklist.extension import ChecklistExtension

def main():
	# Load all recipes as dicts into recipes list.
	filename = '/Users/pranavharathi/GitHub/groceries/recipes/tuscan_kale_salad.yml'
	filename2 = '/Users/pranavharathi/GitHub/groceries/recipes/broccoli_rabe_pasta.yaml'
	recipes = readRecipes([filename, filename2])

	# Create a list of ingredients with aggregate amounts to output.
	# The structure is "ingredientName" => { "oz" => 5 } (unitType => amount)
	groceries = aggregateGroceries(recipes)

	list_of_groceries = prettyPrint(groceries)
	html_list = markdown(list_of_groceries, extensions=[ChecklistExtension()])
	gl_filename = f'grocery_list_{datetime.today().strftime("%Y_%m_%d")}'
	with open(f'{gl_filename}.md', 'w') as grocery_file:
		grocery_file.write(list_of_groceries)
	with open(f'{gl_filename}.html', 'w') as grocery_html:
		grocery_html.write(html_list)

	print(f'List in file {gl_filename}')

def readRecipes(recipe_filenames):
	recipes = []
	for recipe_filename in recipe_filenames:
		with open(recipe_filename, 'r') as recipe_file:
			recipes.append(load(recipe_file))
	return recipes

# recipes is a list of dicts containing information about the ingredients of each rßcipe.
def aggregateGroceries(recipes):
	groceries = {}
	for recipe in recipes:
		for ingredient in recipe['ingredients']:
			amounts = groceries.setdefault(ingredient['name'], {})
			if "type" not in ingredient or ingredient['type'] != "seasoning":
				unitAmt = amounts.setdefault(ingredient['unit'], 0)
				amounts[ingredient['unit']] = unitAmt + ingredient.get('quantity', 0)
	return groceries


def prettyPrint(groceries):
	title = f"## Grocery list for {datetime.today().strftime('%Y_%m_%d')}:"
	items = []
	for ingredient_name in groceries:
		amounts = []
		for unit in groceries[ingredient_name]:
			amounts.append(f'{groceries[ingredient_name][unit]} {unit}')
		items.append(f'* [ ] {ingredient_name}, {", ".join(amounts)}')
	return title + "\n" + "\n".join(items)


if __name__ == '__main__':
	main()
