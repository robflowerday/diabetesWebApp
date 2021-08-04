#pip install streamlit
#pip install pandas

# imports 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt




# create ingredient lists
columns = ['Ingredient', 'Carbs per 100g']#, 'Standard portion size (g)']

packet_readings_leintwardine = [
    ['Garlic - Tesco - Redmore Farms', 16.3],
    ['Leeks, Trimmed - CO-OP', 2.9],
    ['Potatoes, New, Suffolk - CO-OP', 16],
    ['rice, brown, cooked, basmati - CO-OP', 29],
    ['bun, white, super soft - Jones - Village Bakery', 52.1],
    ['cashews, unsalted - costco - Kirland', 28],
    ['cashews, salted - costco', 20.2]
]

calculated_packet_readings_leintwardine = [
    # packet stated cooked carbs per 100 g and said 70g uncooked roughly equals 170g cooked, and that 70 is one serving
    ['rice, brown, uncooked, basmati - CO-OP', 70.4285714286]
]

# create ingredient dataframes from ingredient lists
packet_readings_leintwardine_df = pd.DataFrame(packet_readings_leintwardine, columns=columns)
calculated_packet_readings_leintwardine_df = pd.DataFrame(calculated_packet_readings_leintwardine, columns=columns)

# join data grom seperate dataframes
ingredient_data_df = pd.concat([packet_readings_leintwardine_df, calculated_packet_readings_leintwardine_df], axis=0)





# create streamlit app

# centre the page layout
st.set_page_config(layout='centered')

# streamlit title
st.header('Carbohydrate Calculator')


# started to work on frequent v non-frequent inputs and page layout
# page break
#st.write('---')
# create ingredient selection search box
#st.header('★ Frequent Inputs')



# page break
st.write('---')

# create ingredient selection search box
st.header('Meal Ingredients')
ingredient_choices = list(st.multiselect("Search for meal ingredients, e.g. 'onion'", ingredient_data_df.Ingredient))

# initialise list to hold the carbs per serving of each ingredient and total carbs eaten
carbs_in_chosen_servings = []
total_carbs_eaten = 0

# check that an ingredient, or several has been selected
if len(ingredient_choices) > 0:

    # filter on ingredient choices
    ingredient_choice_df = ingredient_data_df[ingredient_data_df['Ingredient'].isin(ingredient_choices)]
    
    # display the chosen ingredients
    st.write(ingredient_choice_df)

    st.write('---')
    st.header('Ingredient Weights (g)')

    
    for ingredient in ingredient_choices:

        # collect the weight of each ingredient
        ingredient_weight = st.number_input(ingredient, min_value=0, max_value=100000)

        # collect the carbs per hundred grams in each ingredient
        ingredient_carbs_per_hundred = ingredient_data_df[ingredient_data_df['Ingredient'] == ingredient]['Carbs per 100g']

        # calculate the carbs in a given serving
        carbs_in_chosen_serving = ingredient_carbs_per_hundred.values[0] * ingredient_weight / 100

        # display the carbs in a serving of the chosen ingredient
        st.write(f'carbs: {round(carbs_in_chosen_serving, 2)}g')

        # add the carbs consmed to the appropriate list
        carbs_in_chosen_servings.append(carbs_in_chosen_serving)


    
    # calculate the total carbs in the selected meal
    total_carbs_in_meal = sum(carbs_in_chosen_servings)

    # display the total carbs in the given meal
    st.subheader(f'**Total carbs in meal: {round(total_carbs_in_meal, 2)}g**')



    # page break
    st.write('---')

    # percentage of meal eaten
    st.header('Meal Proportion')
    pct = st.number_input('What proportion of the total meal did you eat', min_value=0, max_value=10000, value=100) / 100

    # calculate total carbs eaten
    total_carbs_eaten = total_carbs_in_meal * pct
    st.subheader(f'**Total carbs eaten: {round(total_carbs_eaten, 2)}g**')



# page break
st.write('---')

# collect current blood glucose level
st.header('Current Blood Glucose')
current_bm = st.number_input('Enter your current blood glucose level in mmols', min_value=0.0, max_value=100.0, value=0.0, step=0.1)

# collect current blood glucose level
st.header('Target Blood Glucose')
target_bm = st.number_input('Enter your target blood glucose level in mmols', min_value=0.0, max_value=100.0, value=8.0, step=0.1)

# calculate difference in current and target blood glucose levels
bm_diff = current_bm - target_bm



# page break
st.write('---')

# collect insulin to food ration
st.header('Blood Glucose : Carbs Ratio')
insulin_carb_ratio = st.number_input('Increase in Blood Glucose Levels per 10g of carbs', min_value=0.0, max_value=5.0, value=2.0, step=0.5)

# collect insulin to food ration
st.header('Blood Glucose : Insulin Ratio')
insulin_bm_ratio = st.number_input('Decrease in Blood Glucose Levels per unit of Insulin', min_value=0.0, max_value=5.0, value=2.0, step=0.5)



# page break if insulin calculations are possible
if len(ingredient_choices) > 0 or current_bm > 0:
    st.write('---')
    st.header('Insulin Dose Recommendations')

# initialise insulin dose values
insulin_food_cover = 0
insulin_correction = 0
insulin_total = 0

# check that an ingredient, or several has been selected
if len(ingredient_choices) > 0:
    # calculating insulin dose to cover food
    insulin_food_cover = total_carbs_eaten * insulin_carb_ratio / 10
    st.subheader(f'Food Cover Dose: {round(insulin_food_cover, 2)}')

# check that the current blood sugar level has been given
if current_bm > 0:
    # calculating insulin correction dose
    insulin_correction = bm_diff * (1 / insulin_bm_ratio)
    st.subheader(f'Correction Dose: {round(insulin_correction, 2)}')

# calculating total insulin dose
if len(ingredient_choices) > 0 and current_bm > 0:
    insulin_total = insulin_food_cover + insulin_correction
    st.subheader(f'Total Insulin Dose: {round(insulin_total, 2)}')


# check that an ingredient, or several has been selected
if len(ingredient_choices) > 0:
    # page break
    st.write('---')

    # shorten ingredient names to exclude their description (only include upto the first comma)
    ingredient_choices_short = [str.split(ingredient, ',')[0] for ingredient in ingredient_choices]

    # create dataframe of ingredients chosen and the carbs in the chosen portion sizes
    meal_ingredient_carbs_df = pd.DataFrame(zip(ingredient_choices_short, carbs_in_chosen_servings), columns=['Ingredient', 'Carbs in portion'])

    # set the ingredients as the index of the dataframe
    meal_ingredient_carbs_df.set_index('Ingredient', inplace=True)

    # sort the dataframe by the number of carbs
    meal_ingredient_carbs_df = meal_ingredient_carbs_df.sort_values(by='Carbs in portion', ascending=False)

    # show a bar chart indicating where the carbs in the meal are coming from
    #plt.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.bar(meal_ingredient_carbs_df.index, meal_ingredient_carbs_df['Carbs in portion'])
    ax.set_title('Meal Carb Breakdown')
    ax.set_ylabel('Carbs in portion')
    #ax.grid()
    #ax.tick_params(axis='x', labelrotation=45)
    st.pyplot(fig)