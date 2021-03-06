import copy
from substitutions import SUB
import random
import ConfigManager as cm
import Ingredient
import CookingStep

class Recipe:
    '''
    Recipe
    A class for storing needed information for a single recipe and handling transformations of the recipe.
    '''
    def __init__(self, ingredients, cooking_steps, tools, methods):
        self.ingredients = ingredients
        self.cooking_steps = cooking_steps
        self.tools = tools
        self.methods = methods

    def transform_healthy(self):
        '''
        Transforms the recipe to be more healthy.
        :return: The transformed recipe. A dictionary mapping original ingredients to their substitution/scaled version.
        '''

        # Make a copy of the current recipe
        transformed_recipe = copy.deepcopy(self)

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_healthy']:

                # Get a list of all possible substitutions for this ingredient
                substitution_candidates = copy.deepcopy(SUB['to_healthy'][orig_ing.name])

                # Remove all candidates that already exist within the recipe
                valid_candidates = []
                ingredient_names = [ing.name for ing in transformed_recipe.ingredients]
                for candidate in substitution_candidates:
                    if candidate not in ingredient_names:
                        valid_candidates.append(candidate)

                # Pick a new ingredient to substitute in
                if len(valid_candidates) > 0:
                    new_ing_name = random.choice(valid_candidates)

                    # Perform the ingredient substitution
                    transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                    # make a note of which ingredient was substituted for what (so we can report that to the user)
                    actual_substitutions[orig_ing.name] = new_ing_name

        # Half the amount of condiments or unhealthy spices/herbs
        manager = cm.ConfigManager()
        unhealthy_ingredients_set = manager.load_unhealthy_ingredients()

        for ing in transformed_recipe.ingredients:
            if ing.name in unhealthy_ingredients_set:
                old_ing = copy.deepcopy(ing)
                ing.scale(0.5)
                actual_substitutions[old_ing.__str__()] = ing.__str__()

        return transformed_recipe, actual_substitutions

    def transform_unhealthy(self):
        '''
        Transforms the recipe to be more unhealthy.
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = copy.deepcopy(self)

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_unhealthy']:

                # Get a list of all possible substitutions for this ingredient
                substitution_candidates = copy.deepcopy(SUB['to_unhealthy'][orig_ing.name])

                # Remove all candidates that already exist within the recipe
                valid_candidates = []
                ingredient_names = [ing.name for ing in transformed_recipe.ingredients]
                for candidate in substitution_candidates:
                    if candidate not in ingredient_names:
                        valid_candidates.append(candidate)

                # Pick a new ingredient to substitute in
                if len(valid_candidates) > 0:
                    new_ing_name = random.choice(valid_candidates)

                    # Perform the ingredient substitution
                    transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                    # make a note of which ingredient was substituted for what (so we can report that to the user)
                    actual_substitutions[orig_ing.name] = new_ing_name

        # Double the amount of condiments or unhealthy spices/herbs
        manager = cm.ConfigManager()
        unhealthy_ingredients_set = manager.load_unhealthy_ingredients()

        for ing in transformed_recipe.ingredients:
            if ing.name in unhealthy_ingredients_set:
                old_ing = copy.deepcopy(ing)
                ing.scale(1.5)
                actual_substitutions[old_ing.__str__()] = ing.__str__()

        return transformed_recipe, actual_substitutions

    def transform_vegetarian(self):
        '''
        Transforms the recipe to be vegetarian.
        :return: The transformed recipe.
        '''

        # Make a copy of the current recipe
        transformed_recipe = copy.deepcopy(self)

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_vegetarian']:

                # Get a list of all possible substitutions for this ingredient
                substitution_candidates = copy.deepcopy(SUB['to_vegetarian'][orig_ing.name])

                # Remove all candidates that already exist within the recipe
                valid_candidates = []
                ingredient_names = [ing.name for ing in transformed_recipe.ingredients]
                for candidate in substitution_candidates:
                    if candidate not in ingredient_names:
                        valid_candidates.append(candidate)

                # Pick a new ingredient to substitute in
                if len(valid_candidates) > 0:
                    new_ing_name = random.choice(valid_candidates)

                    # Perform the ingredient substitution
                    transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                    # make a note of which ingredient was substituted for what (so we can report that to the user)
                    actual_substitutions[orig_ing.name] = new_ing_name

        return transformed_recipe, actual_substitutions


    def transform_non_vegetarian(self):
        '''
        Transforms the recipe to be non-vegetarian.
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = copy.deepcopy(self)

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB['to_non_vegetarian']:

                # Get a list of all possible substitutions for this ingredient
                substitution_candidates = copy.deepcopy(SUB['to_non_vegetarian'][orig_ing.name])

                # Remove all candidates that already exist within the recipe
                valid_candidates = []
                ingredient_names = [ing.name for ing in transformed_recipe.ingredients]
                for candidate in substitution_candidates:
                    if candidate not in ingredient_names:
                        valid_candidates.append(candidate)

                # Pick a new ingredient to substitute in
                if len(valid_candidates) > 0:
                    new_ing_name = random.choice(valid_candidates)

                    # Perform the ingredient substitution
                    transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                    # make a note of which ingredient was substituted for what (so we can report that to the user)
                    actual_substitutions[orig_ing.name] = new_ing_name

        # If there are no ways to make this dish non-vegetarian through pure substitution, add a half cup of chicken
        if len(actual_substitutions) == 0 and not self.contains_meat():
            new_ing = Ingredient.Ingredient('chicken', 0.5, 'cup', ['cooked'], ['diced'])
            new_cooking_step = CookingStep.CookingStep(ingredients=[new_ing.name], text='Add {0}.')

            transformed_recipe.ingredients.append(new_ing)
            transformed_recipe.cooking_steps.append(new_cooking_step)

            actual_substitutions['NEW_ING'] = new_ing.name

        return transformed_recipe, actual_substitutions

    def transform_cuisine(self, cuisine_name):
        '''
        Transforms the recipe to be more like the cuisine type given.
        :param cuisine_name: The name of the cuisine to transform to. Valid names: {mexico, japan, italy}
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = copy.deepcopy(self)

        # Init dictionary of substitutions that are actually performed by the transformation
        actual_substitutions = {}

        for orig_ing in self.ingredients:
            if orig_ing.name in SUB[cuisine_name]:

                # Get a list of all possible substitutions for this ingredient
                substitution_candidates = copy.deepcopy(SUB[cuisine_name][orig_ing.name])

                # Remove all candidates that already exist within the recipe
                valid_candidates = []
                ingredient_names = [ing.name for ing in transformed_recipe.ingredients]
                for candidate in substitution_candidates:
                    if candidate not in ingredient_names:
                        valid_candidates.append(candidate)

                # Pick a new ingredient to substitute in
                if len(valid_candidates) > 0:
                    new_ing_name = random.choice(valid_candidates)

                    # Perform the ingredient substitution
                    transformed_recipe.substitute_ingredients(orig_ing, new_ing_name)

                    # make a note of which ingredient was substituted for what (so we can report that to the user)
                    actual_substitutions[orig_ing.name] = new_ing_name

        return transformed_recipe, actual_substitutions


    def transform_size(self, scale):
        '''
        Transforms the recipe to be larger or smaller based on the scale factor given.
        :param scale: The factor by which to scale the recipe.
        :return: The transformed recipe.
        '''
        # Make a copy of the current recipe
        transformed_recipe = copy.deepcopy(self)

        # Scale each ingredient quantity by the specified amount
        for ing in transformed_recipe.ingredients:
            ing.scale(scale)
        for step in transformed_recipe.cooking_steps:
            step.quantities = [scale * quantity for quantity in step.quantities]

        return transformed_recipe


    def __str__(self):
        '''
        :return: The recipe in a nice format.
        '''
        ret_val = ''
        ret_val += '******************************************************************************************************************************\n'
        ret_val += '                                                            RECIPE:\n'
        ret_val += '******************************************************************************************************************************\n'
        ret_val += '***************************************************************\n'
        ret_val += 'INGREDIENTS:\n'
        ret_val += '***************************************************************\n    '
        ret_val += '\n    '.join([str(ingredient) for ingredient in self.ingredients]) + '\n'
        ret_val += '\n***************************************************************\n'
        ret_val += 'COOKING STEPS:\n'
        ret_val += '***************************************************************\n    - '
        ret_val += '\n    - '.join([str(cooking_step) for cooking_step in self.cooking_steps]) + '\n'
        ret_val += '\n***************************************************************\n'
        ret_val += 'TOOLS:\n'
        ret_val += '***************************************************************\n    '
        ret_val += '\n    '.join(self.tools) + '\n'
        ret_val += '\n***************************************************************\n'
        ret_val += 'METHODS:\n'
        ret_val += '***************************************************************\n    '
        ret_val += '\n    '.join(self.methods) + '\n'
        ret_val += '\n***************************************************************\n'

        return ret_val

    def substitute_ingredients(self, old_ing, new_ing_name):
        '''
        Substitutes out the old ingredient for the new ingredient in both the ingredient list and the cooking steps.
        :param old_ing: The old ingredient to substitute out of the recipe.
        :param new_ing_name: The name new ingredient to add to the recipe .
        :return: None
        '''

        for i in range(len(self.ingredients)):
            if self.ingredients[i].name == old_ing.name:
                self.ingredients[i].name = new_ing_name
                self.ingredients[i].descriptor = []
        for i in range(len(self.cooking_steps)):
            for j in range(len(self.cooking_steps[i].ingredients)):
                if self.cooking_steps[i].ingredients[j] == old_ing.name:
                    self.cooking_steps[i].ingredients[j] = new_ing_name
        return

    def contains_meat(self):
        '''
        Determines if the recipe contains meat.
        :return: Boolean that says whether the current recipe contains meat or not.
        '''

        manager = cm.ConfigManager()
        meat_set = manager.load_meat_ingredients()

        for ing in self.ingredients:
            if ing.name in meat_set:
                return True

        return False
