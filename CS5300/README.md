## Objective
To develop a program that takes a database (relations) and functional dependencies as input, normalizes the relations based on the provided functional dependencies, produces SQL queries to generate the normalized database tables, and optionally determines the highest normal form of the input table.

## Input Requirements
The program requires the complete set of tables (relations) from the database schema that need normalization. Each table should be defined with its name, list of columns (attributes), key constraints (including primary keys and candidate keys relevant to 2NF, 3NF, and BCNF definitions), and any attributes holding multi-valued, non-atomic data. Since normalization is typically applied to individual tables, the program processes one table at a time, which is acceptable.

## Output
Upon successful completion of the normalization process, the program provides:

### SQL Queries
These include table definition queries ready for execution, incorporating commands to create normalized tables with appropriate constraints such as primary keys and foreign keys.

### Normalized Relational Database Schema
Alternatively, a detailed schema diagram or textual representation of the normalized tables is presented. This includes each table's name, list of attributes, and relevant constraints identified during the normalization process.

## Core Components
- **Input Parser**: To parse the input dataset and functional dependencies.
- **Normalizer**: To normalize the dataset based on functional dependencies.
- **Final Relation Generator**: To generate normalized schema for the database.

## The implementation includes:
- **Source Code**: Well-commented source code in the language of your choice.
- **Code Description**: Detailed documentation describing the flow, logic, and methodology of the code.

## Input Parser
Responsible for parsing the input dataset and functional dependencies.

## Normalizer
Executes the normalization process based on identified functional dependencies.

## Program Description
This Python 3 project is designed to process a CSV file that includes a table, primary key, and functional dependencies. The user is prompted to specify the desired normal form for table normalization, and the resulting normalized tables are displayed in the standard output.

- **main.py**: Manages all user interactions, including input and optional debugging features.
- **table.py**: Defines the structure and operations for manipulating table data within the program. It includes various getter functions for accessing information such as super keys and candidate keys.
- **normalizer.py**: Provides helper functions responsible for normalizing the table according to different normal forms.
- **parser.py**: Defines the parser function.

## Program Flow
1. **Input Data Collection**:
   - `main.py`: Request user input for table Data and parses the data from the file given.
   
2. **Table Object Construction**:
   - Parsed table data is passed to the constructor in `table.py` to create a table Object.

3. **Additional Data Input**:
   - `main.py`: Requests additional user data such as functional dependencies, primary key, and multivalue functional dependencies.
   - The table object is updated with these user-provided values.

4. **Normalization Request**:
   - `main.py`: Asks the user to specify the desired normal form for normalization.

5. **Normalization Process**:
   - Sequentially calls corresponding functions in `normalizer.py` to normalize the table and returns normalized tables.

6. **Output**:
   - Displays the normalized tables as output.

## How to run
1. Open terminal.
2. Ensure that the latest version of Python is installed.
3. Clone the project into the terminal.
4. Run `python3 main.py`.
5. Enter the CSV file.
6. Run the program.

## Final Relation Generator
Produces the final normalized schema for the database.
