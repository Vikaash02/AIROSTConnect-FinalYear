import json
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProgramRecommender:
    def __init__(self, programs=None):
        """
        Initializes the ProgramRecommender class.

        :param programs: List of programs to recommend (default: empty list)
        """
        # Initialize the list of programs (default is an empty list)
        self.programs = programs or []
        
        # Initialize the TfidfVectorizer which will be used to convert text into TF-IDF features
        # `stop_words='english'` removes common English stopwords during the vectorization
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def add_program(self, program):
        """
        Adds a new program to the list of programs.

        :param program: A dictionary containing program details
        """
        # Append the new program to the list
        self.programs.append(program)

    def generate_recommendations(self, user_categories, top_n=5):
        """
        Generates program recommendations based on the user's selected categories.

        :param user_categories: List of user's selected categories
        :param top_n: The number of recommended programs to return (default is 5)
        :return: A list of recommended programs
        """
        # If no programs are available, print a message and return an empty list
        if not self.programs:
            print("No programs available.")
            return []

        # Create a list of program descriptions by combining the program's name, category, and notes
        descriptions = [
            f"{p.get('name', '')} {p.get('category', '')} {p.get('notes', '')}" 
            for p in self.programs
        ]
        
        # Convert the program descriptions into a TF-IDF matrix where each row is a program, and each column is a feature (word)
        tfidf_matrix = self.vectorizer.fit_transform(descriptions)

        # Filter the programs based on the selected categories
        category_matches = [
            p for p in self.programs 
            if p.get('category') in user_categories
        ]

        # Debugging: Print the matching programs based on user categories
        print(f"Matching programs for categories {user_categories}: {category_matches}")  # Debugging

        # If no programs match the selected categories, print a message and return an empty list
        if not category_matches:
            print(f"No programs found for the selected categories: {user_categories}")
            return []

        # Create a TF-IDF matrix for the category-matched programs
        category_descriptions = [
            f"{p.get('name', '')} {p.get('category', '')} {p.get('notes', '')}" 
            for p in category_matches
        ]
        category_tfidf = self.vectorizer.transform(category_descriptions)

        # Calculate the cosine similarities between the category-matched programs and all programs
        similarities = cosine_similarity(category_tfidf, tfidf_matrix)

        # For each program in the category-matched list, find the index of the most similar program in the overall list
        similar_program_indices = similarities.argmax(axis=1)

        # Return the top N most similar programs based on the indices
        recommended_programs = [self.programs[i] for i in similar_program_indices[:top_n]]
        
        return recommended_programs


def load_program_data(program_data_file):
    """
    Loads program data from a JSON file.

    :param program_data_file: Path to the program data JSON file
    :return: List of programs
    """
    # Open the specified file and load the JSON data
    with open(program_data_file, 'r') as f:
        # Return the list of programs from the JSON data
        return json.load(f)['programs']


def load_user_preferences(preferences_file):
    """
    Loads user preferences (selected categories) from a JSON file.

    :param preferences_file: Path to the user preferences JSON file
    :return: User preferences (list of preferred categories)
    """
    # Open the specified file and load the JSON data
    with open(preferences_file, 'r') as f:
        # Return the user preferences
        return json.load(f)


def main():
    """
    The main function that executes the recommendation engine process.
    """
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description='Generate program recommendations.')
    
    # Add arguments for program data file, user preferences file, and the number of recommendations
    parser.add_argument('--programs', type=str, required=True, help='Path to program data JSON file')
    parser.add_argument('--preferences', type=str, required=True, help='Path to user preferences JSON file')
    parser.add_argument('--top_n', type=int, default=5, help='Number of recommended programs to return')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Load the program data from the specified file
    program_data = load_program_data(args.programs)
    
    # Load the user preferences (selected categories) from the specified file
    user_preferences = load_user_preferences(args.preferences)

    # Create an instance of the ProgramRecommender class with the loaded programs
    recommender = ProgramRecommender(programs=program_data)

    # Generate program recommendations based on the user's preferred categories
    recommended_programs = recommender.generate_recommendations(user_preferences['preferred_categories'], top_n=args.top_n)

    # Output the recommended programs
    if recommended_programs:
        for program in recommended_programs:
            # Print the details of each recommended program
            print(f"Program Name: {program['name']}, Category: {program['category']}, Venue: {program['venue']}")
    else:
        # If no recommendations are available, print a message
        print("No recommendations available.")

if __name__ == '__main__':
    # Run the main function
    main()
