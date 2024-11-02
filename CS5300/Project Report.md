## Program Description:
This Python 3 project is designed to process a CSV file that includes a table, primary key, and functional dependencies. The user is prompted to specify the desired normal form for table normalization, and the resulting normalized tables are displayed in the standard output.

- main.py: Manages all user interactions, including input and optional debugging features.

- table.py: Defines the structure and operations for manipulating table data within the program. It includes various getter functions for accessing information such as super keys and candidate keys.

- normalizer.py: Provides helper functions responsible for normalizing the table according to different normal forms.

## Program Flow:

1. Input Data Collection:
- main.py: Request user input for table Data and parses the data from the file given

2. Table Object Construction:
- parsed table data is passed to the constructor in table.py to create a table Object

3. Additional Data Input:

- main.py: Requests additional user data such as functional dependencies, primary key, and multivalue functional dependencies.
- The table object is updated with these user-provided values.

4. Normalization Request:
- main.py: Asks the user to specify the desired normal form for normalization.

5. Normalization Process:
- Sequentially calls corresponding functions in normalizer.py to normalize the table.
Returns normalized tables.

6. Output:
- Displays the normalized tables as output

## How to run:
1. Open terminal
2. Ensure that latest version of python is installed
3. run 'python3 main.py'
4. enter csv file 
5. run the program