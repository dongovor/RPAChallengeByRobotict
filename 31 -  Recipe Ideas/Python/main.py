import requests
from bs4 import BeautifulSoup
import re
import os


BASE_URL = 'https://www.bbcgoodfood.com/'
URL_PARTS = {
        'recipes': 'recipes/',
        'search': 'search?q='
        }


def get_recipes():
    recipies_dict = dict()
    user_input = input('What do you want to eat? ')
    recipies_to_extract = input('How many recipies do you want to extract? ')
    user_input = user_input.replace(' ', '+')
    recipe_counter = 0
    response = requests.get(f'{BASE_URL}{URL_PARTS["search"]}{user_input}')

    soup = BeautifulSoup(response.text, 'html.parser')
    recipies = soup.find_all("a", class_="standard-card-new__article-title")
    for recipie in recipies:
        steps = []
        ingredients = []
        dish_name = re.sub(' +', ' ', recipie.text.strip())
        dish_link = recipie.get('href')
        response = requests.get(f'{BASE_URL}{URL_PARTS["recipes"]}{dish_link}')
        recipie_soup = BeautifulSoup(response.text, 'html.parser')
        ingredients_raw = recipie_soup.find_all('li', class_='pb-xxs pt-xxs list-item list-item--separator')

        for ingredient in ingredients_raw:
            ingredients.append(ingredient.text.strip())

        steps_raw = recipie_soup.find_all('li', class_='pb-xs pt-xs list-item')
        for step in steps_raw:
            # print(step.text.strip())
            step = step.text.strip().replace('STEP', '')
            step = step[1:]
            steps.append(step)

        recipies_dict[dish_name] = ([ingredients, steps])
        recipe_counter += 1

        if recipe_counter >= int(recipies_to_extract):
            break
    return recipies_dict


def write_recipe(input_dict, idx):
    with open(f'{list(input_dict.keys())[idx - 1]}.txt', 'w') as f:
        f.write(f'{list(input_dict.keys())[idx - 1]}\n')
        for ingredient in input_dict[list(input_dict.keys())[idx - 1]][0]:
            f.write(f'{ingredient}\n')
        f.write('\n')
        for step in input_dict[list(input_dict.keys())[idx - 1]][1]:
            f.write(f'{step}\n')
    print(f'{list(input_dict.keys())[idx - 1]}.txt file was created')
    print(f'Full path: {os.path.abspath(f"{list(input_dict.keys())[idx - 1]}.txt")}')


def main():
    print('asdasd')
    recipies_dict = get_recipes()
    print('Please choose recipie:')
    for idx in recipies_dict.keys():
        recipe_number = list(recipies_dict.keys()).index(idx) + 1
        print(f'{recipe_number}. {idx}')
    user_input = int(input('Please choose recipie: '))
    write_recipe(recipies_dict, user_input)



if __name__ == '__main__':
    main()
    print('Done.')
