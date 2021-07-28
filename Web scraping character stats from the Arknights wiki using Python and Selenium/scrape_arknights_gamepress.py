import pickle
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
# Install web drivers dynamically
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.INFO)

# Dynamically install and set up a Google Chrome web driver for Selenium
driver = webdriver.Chrome(ChromeDriverManager().install())
# Make the driver wait X seconds
driver.implicitly_wait(7)

# Scrape the operator's names and page URLs
req = requests.get("https://gamepress.gg/arknights/tools/interactive-operator-list")
soup = BeautifulSoup(req.content, "lxml")

# Get all the table cells (<td>) with information about the operators
op_list = soup.find_all("td", class_="operator-cell")
op_dict = {}
for op in op_list:
    # Get the name and their personal page from these HTML elements
    name = op.find("div", class_="operator-title").a.text
    page = "https://gamepress.gg" + \
        op.find("div", class_="operator-title").a["href"]
    # Add the new information to the dictionary
    op_dict[name] = page

logging.info(f"{datetime.datetime.now()}: Found {len(op_list)} operators")

# Additional manually discovered alternate form operators
op_dict["Amiya (Guard)"] = "https://gamepress.gg/arknights/operator/amiya-guard"

# Write this dictionary to a pickle file
with open("operator_pages.pickle", "wb") as f:
    pickle.dump(op_dict, f)
    logging.info(f"{datetime.datetime.now()}: Created pickle file with operator pages")

# Running dataframe to collect operator data into
main_df = pd.DataFrame(
    {
        "operator": list(),
        "rarity": list(),
        "class": list(),
        "promotion_level": list(),
        "level": list(),
        "hp": list(),
        "attack": list(),
        "defense": list(),
        "resistance": list(),
        "redeployment_time": list(),
        "dp_cost": list(),
        "block_count": list(),
        "attack_interval": list(),
        "cn_release_date": list(),
        "global_release_date": list(),
        "is_limited": list()
    }
)

# Uncomment to use a subset instead of all characters
# op_dict = {
#     "SilverAsh": "https://gamepress.gg/arknights/operator/silverash",
#     "W": "https://gamepress.gg/arknights/operator/w",
#     "Amiya": "https://gamepress.gg/arknights/operator/amiya",
#     "THRM-EX": "https://gamepress.gg/arknights/operator/thrm-ex"
# }

def get_stats_per_level(num_levels: int, df: pd.DataFrame) -> pd.DataFrame:

    for i in range(num_levels):

        # Current elite rank
        promotion_level_selected_elem = driver.find_element_by_class_name("current-button")
        promotion_level = "0" if promotion_level_selected_elem.text == "Non-Elite" else promotion_level_selected_elem.text[-1]

        # Current operator level
        operator_level = driver.find_element_by_id("myRange").get_attribute('value')

        # Hp, Atk, Def
        stats_container_elem = driver.find_element_by_id("stats-container")
        # Split the stat names and values into a list (split at newlines)
        stats_split = stats_container_elem.text.splitlines()
        # Get the individual stat values
        op_hp, op_atk, op_def = stats_split[1], stats_split[3], stats_split[5]

        # Other stats
        other_stats_container_elem = driver.find_element_by_class_name("other-stat-cell")
        # Split the stat names and values into a list (split at newlines)
        other_stats_split = other_stats_container_elem.text.splitlines()
        # Get the individual stat values
        op_res, op_redeploy, op_cost, op_block, op_atk_interv = other_stats_split[1], other_stats_split[3], other_stats_split[5], other_stats_split[7], other_stats_split[9]

        # Create a dictionary to append to the DataFrame with latest data scraped
        row_to_append = {
            "operator": operator,
            "rarity": operator_rarity,
            "class": operator_class,
            "promotion_level": promotion_level,
            "level": operator_level,
            "hp": op_hp,
            "attack": op_atk,
            "defense": op_def,
            "resistance": op_res,
            "redeployment_time": op_redeploy,
            "dp_cost": op_cost,
            "block_count": op_block,
            "attack_interval": op_atk_interv,
            "cn_release_date": cn_release_date,
            "global_release_date": global_release_date,
            "is_limited": operator_is_limited
        }
        df = df.append(row_to_append, ignore_index=True)

        # Get the arrow to increase operator level
        increase_level_button = driver.find_element_by_class_name("fa-arrow-right")
        # Click the button (increase 1 level)
        increase_level_button.click()

    # Return the DF with all the data accumulated so far
    return df


# Get data for each available operator
for operator in op_dict:
    logging.info(f"{datetime.datetime.now()}: Scraping {operator}")

    # These character pages are still a WIP on the wiki so they break the script :(
    # wip_characters = ["Tequila", "La Pluma", "Mizuki", "Ch'en The Holungday"]
    # if operator in wip_characters:
    #     continue

    target_url = op_dict[operator]

    # Open the target URL
    driver.get(target_url)
    # Create an ActionChains object used to scroll in the page
    actions = ActionChains(driver)

    # Select an element down in the page to scroll down to
    # This makes a sticky ad appear
    scroll_to_element = driver.find_element_by_class_name("popular-items-block")
    actions.move_to_element(scroll_to_element).perform()
    # Close sticky ad
    sticky_ad_close_btn = driver.find_element_by_id("closeIcon")
    sticky_ad_close_btn.click()

    # First thing we need before reading data: decrease the operator level (even if it is already at the lowest level possible)
    # Otherwise some stats may be missing
    decrease_level_button = driver.find_element_by_class_name("fa-arrow-left")
    decrease_level_button.click()

    # List of 3 buttons for each promotion level (E0, E1, E2)
    rank_buttons = driver.find_elements_by_class_name("rank-button")

    # Read the opreator class
    operator_class = driver.find_element_by_class_name("profession-title").text.strip()
    # Read the operator rarity by counting the number of stars in their rarity
    operator_rarity = len(
        driver
        .find_element_by_class_name("rarity-cell")
        .find_elements_by_tag_name("img")
    )

    # HTML tables with info on operator release date and availability limit status
    obtain_approach_tables = driver.find_element_by_class_name("obtain-approach-table").find_elements_by_tag_name("table")

    # Get the release date in the chinese server
    cn_release_date = obtain_approach_tables[1].find_elements_by_tag_name("tr")[0].find_element_by_tag_name("td").text
    # Get the release date in the global server
    global_release_date = obtain_approach_tables[1].find_elements_by_tag_name("tr")[1].find_element_by_tag_name("td").text
    # Text with headhunting availability status
    headhunting_type = obtain_approach_tables[0].find_elements_by_tag_name("tr")[0].find_element_by_tag_name("td").text
    # If the text has the word limited, then the unit is limited
    operator_is_limited = True if "limited" in headhunting_type.lower() else False

    # Get stats for all the promotion levels available for the current operator

    if len(rank_buttons) == 1:
        # Get stats for all E0 levels
        main_df = get_stats_per_level(30, main_df)

    elif len(rank_buttons) == 2:
        # Get stats for all E0 levels
        main_df = get_stats_per_level(40, main_df)
        # Now promote to E1 i.e. click the E1 button
        rank_buttons[1].click()
        main_df = get_stats_per_level(55, main_df)

    elif len(rank_buttons) == 3:
        # Get stats for all E0 levels
        main_df = get_stats_per_level(50, main_df)
        # Now promote to E1 i.e. click the E1 button
        rank_buttons[1].click()
        main_df = get_stats_per_level(80, main_df)
        # Now promote to E2 i.e. click the E2 button
        rank_buttons[2].click()
        main_df = get_stats_per_level(90, main_df)

logging.info(f"{datetime.datetime.now()}: Finished scraping data")

# Output the DF as a CSV
main_df.drop_duplicates(inplace=True)
main_df.to_csv("arknights_operator_stats.csv", index=False)

logging.info(f"{datetime.datetime.now()}: Output CSV file successfully")

driver.quit()