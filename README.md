# **AIROST Connect Documentation**

## **Overview**
The `recommendation_engine.py` script is designed to recommend programs to a user based on their selected categories. It uses **TF-IDF** (Term Frequency-Inverse Document Frequency) and **cosine similarity** to generate recommendations from a set of programs based on a user's preferences. The script accepts input data via command-line arguments, processes it, and outputs the top `n` recommended programs.

The main components of the script are:
1. **ProgramRecommender**: A class that handles the logic of generating recommendations based on user preferences and program data.
2. **Command-Line Interface (CLI)**: Using `argparse`, the script allows users to input data files and the number of recommendations desired.

---

## **Features**
1. **Generate Recommendations**: Given a set of user preferences, the script generates program recommendations based on matching categories.
2. **TF-IDF Vectorization**: The program descriptions are vectorized using TF-IDF, allowing the script to compute cosine similarities between category-matched programs and all available programs.
3. **Error Handling**: The script provides detailed logs and error messages for cases where no matching programs are found or if there are issues with the input files.
4. **Command-Line Arguments**: The script can accept input for:
   - The **program data file** (`programs`),
   - The **user preferences file** (`preferences`),
   - The **number of recommendations** to return (`top_n`).

---

## **File Structure**
The script operates with two main input files:
1. **program_details.json**: Contains a list of available programs, each with a name, category, venue, and description.
2. **user_preferences.json**: Contains the categories selected by the user for which they wish to receive recommendations.

---

## **Installation**

1. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```
3. **Install dependencies**:
   Create a `requirements.txt` file with the following content:
   ```txt
   scikit-learn>=0.24.0
   numpy>=1.19.0
   flask>=2.0.0
   flask-cors>=3.1.1
   ```
   Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

The script can be run from the command line using the following syntax:

```bash
python recommendation_engine.py --programs program_details.json --preferences user_preferences.json --top_n 5
```

### **Arguments**:
1. **`--programs`**: The path to the `program_details.json` file containing program data.
2. **`--preferences`**: The path to the `user_preferences.json` file containing the user's selected categories.
3. **`--top_n`**: The number of recommended programs to return (default: 5).

### **Example**:

```bash
python recommendation_engine.py --programs program_details.json --preferences user_preferences.json --top_n 5
```

This will:
- Load the program data from `program_details.json`.
- Load the user preferences from `user_preferences.json`.
- Recommend the top 5 programs based on the selected categories.

---

## **Functionality**

### **`ProgramRecommender` Class**
The `ProgramRecommender` class handles the core recommendation logic. It uses **TF-IDF Vectorization** and **cosine similarity** to generate program recommendations.

#### **Methods**:

- **`__init__(self, programs=None)`**:
  - Initializes the recommender with a list of programs. If no programs are passed, it defaults to an empty list.
  
- **`add_program(self, program)`**:
  - Adds a new program to the list of programs.

- **`generate_recommendations(self, user_categories, top_n=5)`**:
  - Generates and returns the top `n` recommended programs based on the user’s selected categories.
  - Uses **TF-IDF vectorization** to convert program descriptions into vectors and **cosine similarity** to find the most similar programs.
  - If no programs match the user’s selected categories, it returns an empty list and prints a message.

### **Helper Functions**:

- **`load_program_data(program_data_file)`**:
  - Loads the program data from the specified JSON file. Expects the file to contain a "programs" key with a list of programs.

- **`load_user_preferences(preferences_file)`**:
  - Loads the user preferences (categories) from the specified JSON file. Expects the file to contain a "preferred_categories" key with a list of categories.

---

## **Input Files**

### **`program_details.json`**:
This file contains the program data with details such as **name**, **category**, **venue**, and **notes**.

Example:

```json
{
  "programs": [
    {
      "name": "AI Basics",
      "category": "AI",
      "venue": "Tech Hall A",
      "date_time": "2024-12-15 10:00",
      "notes": "Introduction to Artificial Intelligence"
    },
    {
      "name": "IoT for Smart Homes",
      "category": "IoT",
      "venue": "Conference Room 1",
      "date_time": "2024-12-16 14:00",
      "notes": "Learn to build IoT-based smart home systems"
    }
  ]
}
```

### **`user_preferences.json`**:
This file contains the user’s preferred categories. The categories in this file should match the categories in the program data.

Example:

```json
{
  "preferred_categories": ["AI", "IoT"]
}
```

---

## **Output**

The script will output the recommended programs based on the user's preferences. If no programs match, it will print:

```
No programs found for the selected categories.
```

If there are matching programs, it will print:

```
Program Name: AI Basics, Category: AI, Venue: Tech Hall A
Program Name: IoT for Smart Homes, Category: IoT, Venue: Conference Room 1
```

---

## **Error Handling**

- **Empty Program List**: If the list of programs is empty, the system will return an empty list of recommendations and print `"No programs available."`
- **No Matching Programs**: If no programs match the user’s selected categories, it prints a message: `"No programs found for the selected categories."`
- **Invalid Input Files**: If the input files are missing or have incorrect formats, appropriate error messages will be shown.

---

## **Example Usage**

### **Example 1:**
If you want to get the top 5 program recommendations for a user who prefers **AI** and **IoT**, run the following command:

```bash
python recommendation_engine.py --programs program_details.json --preferences user_preferences.json --top_n 5
```

### **Example 2:**
If you have a smaller number of programs and only want the top 3 recommendations:

```bash
python recommendation_engine.py --programs program_details.json --preferences user_preferences.json --top_n 3
```

---

## **Conclusion**

This script provides a **command-line tool** for generating program recommendations based on user-selected categories. It uses **TF-IDF** and **cosine similarity** to find programs that match the user’s preferences. The script is highly configurable via command-line arguments, making it suitable for a variety of use cases where user preferences need to be matched with available program data.
