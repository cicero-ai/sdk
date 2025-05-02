
from cicero_sdk import Sophia, Router

def vacation(verb_position: int, phrase_num: int, phrase: dict, output: dict) -> None:

    for noun in phrase["nouns"]:
        token = output["mwe"][noun["head"]]
        print(f"Looks like we're vacationing in {token['word']}")

def main():
    # Initialize Sophia and Router
    nlu = Sophia()
    router = Router()

    # Add a route for the 'verbs/action/travel/depart' category
    router.add("verbs/action/travel/depart", vacation)

    # Process the input
    nlu.route(router, "I want to take off to Thailand and have some fun")
    print("Done")

if __name__ == "__main__":
    main()



