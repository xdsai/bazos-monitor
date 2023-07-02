import requests
from bs4 import BeautifulSoup
import utils
import threading
import time


def user_controls():
    """Function to get user inputs for the program."""
    while True:
        print("\nPlease choose an option from the following:")
        print("1. Run all search monitors")
        print("2. Add a search term")
        print("3. Remove a search term")
        print("4. List all search terms")
        print("5. Set a webhook")
        print("6. Remove a webhook")
        print("7. Exit")
        choice = input("Enter your choice: ")

        match choice:
            case "1":
                print("Running all search monitors...")
                print("You can stop the program at any time by pressing CTRL+C")
                for term in utils.list_search_terms():
                    threading.Thread(target=monitor, args=(term,)).start()
                    time.sleep(5)
                break

            case "2":
                search_term_dict = {"site":"",
                               "keyword":"",
                               "price_min":"",
                               "price_max":"",
                               "location":"",
                               "radius":""}
                print("Please enter the following details for your search term (default blanks)")

                site = input("Enter a site (cz/sk): ")
                if site != "cz" and site != "sk":
                    print("Invalid site.")
                    break

                keyword = input("Enter a search keyword (eg.: bmw e46): ")

                price_min = input("Enter a minimum price (eg.: 1000): ")
                if (price_min.isdigit() == False and price_min != ""):
                    if int(price_min) < 0:
                        print("Invalid price.")
                        break

                price_max = input("Enter a maximum price (eg.: 10000): ")
                if (price_max.isdigit() == False and price_max != ""):
                    if int(price_max) < int(price_min):
                        print("Invalid price.")
                        break

                location = input("Enter a location (eg.: Brno): ")
                radius = input("Enter a radius (km) (eg.: 10): ")
                if radius.isdigit() == False and radius != "":
                    print("Invalid radius.")
                    break

                search_term_dict["site"] = site
                search_term_dict["keyword"] = keyword
                search_term_dict["price_min"] = price_min
                search_term_dict["price_max"] = price_max
                search_term_dict["location"] = location
                search_term_dict["radius"] = radius

                print("Does this look right?")
                print(f"Site: Bazos {site}\nKeyword: {keyword}\nPrice min: {price_min}\nPrice max: {price_max}\nLocation: {location}\nRadius: {radius}")
                confirm = input("y/n: ")

                if confirm == "y":
                    utils.add_search_term(search_term_dict)
                    print("Search term added.")
                else:
                    print("Search term not added.")

            case "3":
                print("Select a search term to remove:")

                ctr = 0
                for term in utils.list_search_terms():
                    print(f"{ctr}. {term['keyword']}, {term['site']}")
                    ctr += 1
                
                choice = input("Enter your choice: ")
                if choice.isdigit() == False or int(choice) < 0 or int(choice) > ctr:
                    print("Invalid choice.")
                    break

                utils.remove_search_term(utils.list_search_terms()[int(choice)])

            case "4":
                print("Search terms:")
                for term in utils.list_search_terms():
                    print(f"{term['keyword']}, {term['site']}")
            
            case "5":
                webhook = input("Enter a webhook: ")
                utils.set_webhook(webhook)
                print("Webhook set.")

            case "6":
                utils.rm_webhook()
                print("Webhook removed.")

            case "7":
                print("Exiting...")
                exit()

            case _:
                print("Invalid choice.")
            
        

def monitor(search_term):
    """Function to monitor a search term on Bazos."""    
    site = search_term["site"]
    keyword = search_term["keyword"]
    price_min = search_term["price_min"]
    price_max = search_term["price_max"]
    location = search_term["location"]
    radius = search_term["radius"]

    search_link = f"https://www.bazos.{site}/search.php?hledat={keyword}&rubriky=www&hlokalita={location}&humkreis={radius}&cenaod={price_min}&cenado={price_max}&order=4&kitx=ano"

    print(f"Running monitor for {keyword} on Bazos {site}...")

    while True:
        try:
            r = requests.get(search_link)
        except:
            print("Error connecting to Bazos.")
            pass

        soup = BeautifulSoup(r.text, "html.parser")

        results = soup.find_all("div", class_="inzeraty inzeratyflex")

        for result in results:
            title = result.find("h2").text.strip()
            price = result.find("div", class_="inzeratycena").text.strip()
            link = result.find("h2", class_="nadpis").find("a")["href"]
            picture = result.find("img")["src"]
            location_tmp = result.find("div", class_="inzeratylok").text.strip()
            location = location_tmp[:6] + " " + location_tmp[len(location_tmp)-6:]
            desc = result.find("div", class_="popis").text.strip()

            if utils.check_link(link) == False:
                utils.add_link(link)
                print(f"New result for {keyword} on Bazos {site}!")
                print(f"Title: {title}")
                print(f"Price: {price}")
                print(f"Link: {link}")
                print("Sending webhook...")
                utils.send_webhook(title, price, link, picture, location, desc)
                print("Webhook sent.")

        time.sleep(300)

user_controls()