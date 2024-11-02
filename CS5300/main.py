
# Programmer: Amrit Bhaganagare 12619462 and Venkata Dheeraj Reddy Busireddy 12576469
# Class: CS 5300


import table
import normalizer
import csv
import sys
from parser import parse_csv


def input_funct_depends(myTable: table.Table) -> None:
    '''
    Receives a table object, prompts the user to input functional dependencies, and incorporates them into the table.
    '''
    print()
    counter = 0
    for col in myTable.columns:
        print(f"{counter}) {col}")
        counter += 1
    print(
        "Please enter any valid functional dependencies.\n"
        "Format example: 0,1 -> 2,3"
    )
    done = False
    while not done:
        entry = input(": ")
        if entry.strip() == "":
            return
        if not ("->" in entry):
            print("Try again, there was no '->' in your definition.")
            continue
        splentry = entry.split("->")
        
        determinant = splentry[0]
        dependent = splentry[1]
        
        spleterminant = determinant.split(",")
        splependant = dependent.split(",")
        
        try:
            streterminant = [int(attr.strip()) for attr in spleterminant]
            strependant = [int(attr.strip()) for attr in splependant]
        except ValueError as error:
            print(f"Error in input: {error}")
            continue
        try:
            for i in streterminant:
                myTable.columns[i]
            for i in strependant:
                myTable.columns[i]
            myTable.funct_depends.append((streterminant, strependant))
            print(f"Successfully added {[myTable.columns[i] for i in streterminant]} -> {[myTable.columns[i] for i in strependant]} to the list of functional dependencies.")
        except IndexError as error:
            print(f"Found issue with one or more of your attributes entered: {error}")
            continue
        
    
def inputMVDS(myTable: table.Table) -> None:
    '''
    This function accepts a table object, prompts the user for multivalue functional dependencies, and adds them to the table.
    '''
    print()
    counter = 0
    for col in myTable.columns:
        print(f"{counter}) {col}")
        counter += 1
    print("Enter any valid multivalue functional dependencies.\nFormat: Determinant ->-> dependent ")
    done = False
    while not done:
        entry = input(": ")
        if entry.strip() == "":
            return
        if not ("->->" in entry):
            print("Try again, there was no '->' in your definition.")
            continue
        splentry = entry.split("->->")
        
        determinant = splentry[0]
        dependent = splentry[1]
        
        try:
            numerminant = int(determinant.strip())
            numendant = int(dependent.strip())
        except ValueError as error:
            print(f"Error in input: {error}")
            continue
        
        try:
            myTable.columns[numerminant]
            myTable.columns[numendant]
            myTable.multi_funct_depends.append((numerminant, numendant))
            print(f"Added {myTable.columns[numerminant]} ->-> {myTable.columns[numendant]} to list of functional dependencies.")
        except RuntimeError as error:
            print(f"One or more of your attributes entered had an issue: {error}")
            continue

def input_primary_key(myTable: table.Table) -> None:
    '''
    Function accepts a table object as input, prompts the user to specify the primary key, and then assigns this primary key within the table.
    '''
    print()
    candidate_keys = myTable.get_candidate_keys()
    counter = 0
    for key in candidate_keys:
        print(f"{counter}) {[myTable.columns[i] for i in key]}")
        counter += 1
    print("Select a candidate key to be a primary key")
    done = False
    while not done:
        entry = input(": ")
        try:
            nentry = int(entry.strip())
        except ValueError as error:
            print(f"Error in input: {error}")
            continue
            
        try:
            myTable.primary_key = candidate_keys[nentry]
            done = True
        except IndexError as error:
            print(f"Error in input: {error}")
            
import parser

def create_table() -> table.Table:
    '''
    Function prompts the user to select a CSV file and then returns a table object populated with the data from that file.
    '''
    while True:
        print()
        csv_file = input("Input a CSV file with a single table: ")
        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                csv_cols = next(csv_reader)
                csv_rows = list(csv_reader)
                return table.Table(csv_cols, csv_rows)
        except FileNotFoundError as error:
            print(error)
        except RuntimeError as error:
            print(error)
            ## Programmer: Madeline Harmon
def find_normal_form(myTable: table.Table) -> None:
    '''
    Function accepts a table as input, identifies its highest normal form, and prints the result.
    '''
    form = ""
    if not normalizer.is_1nf(myTable):
        form = "Not normalized to any level"
    elif not normalizer.is_2nf(myTable):
        form = "1NF"
    elif not normalizer.is_3nf(myTable):
        form = "2NF"
    elif not normalizer.is_bcnf(myTable):
        form = "3NF"
    elif not normalizer.is_4nf(myTable):
        form = "BCNF"
    else:
        form = "4NF or 5NF"
    
    print("Highest normal form:", form)
            
def normalize_to_form(start_table: table.Table, form: int) -> list[table.Table]:
    '''
    Takes in a table object and a form as an int 1 -> 1st, 4 -> bc, 6 -> 5th\n
    Outputs a list of tables normalized to the given form
    '''
    form_counter = 0
    table_list = [start_table]
    while form_counter != form:
        print()
        form_counter += 1
        new_table_list: list[table.Table] = []
        print_str = ""
        for myTable in table_list:
            match form_counter:
                case 1:
                    print_str = "Normalized 1NF"
                    new_table_list += normalizer.first_normal_form(myTable)
                case 2:
                    print_str = "Normalized 2NF"
                    new_table_list += normalizer.second_normal_form(myTable)
                case 3:
                    print_str = "Normoalized 3NF"
                    new_table_list += normalizer.third_normal_form(myTable)
                case 4:
                    print_str = "Normalized BCNF"
                    new_table_list += normalizer.boyce_codd_normal_form(myTable)
                case 5:
                    print_str = "Normalized 4NF"
                    new_table_list += normalizer.forth_normal_form(myTable)
                case 6:
                    print_str = "Normalized 5NF"
                    new_table_list += normalizer.fifth_normal_form(myTable)
                case _:
                    raise RuntimeError(f"Runtime Error")
        print(f"{print_str}")
        for new_table in new_table_list:
            print()
            new_table.print_table()
            new_table.print_primary_key()
            new_table.print_functional_dependencies()
            new_table.print_mvds()
        table_list = new_table_list
    return table_list

def main():
    myTable = create_table()
    
    input_funct_depends(myTable)
    input_primary_key(myTable)
    inputMVDS(myTable)
    
    normal_form = int(input(
        "What number form you would like to normalize to?\n"
        "1) 1NF\n"
        "2) 2NF\n"
        "3) 3NF\n"
        "4) BCNF\n"
        "5) 4NF\n"
        "6) 5NF\n"
        "Form: "
    ))
    
    find_highest_form = input("Find the highest form of the input table? (1: Yes, 2: No): ")
    
    print("\nOriginal Table")
    myTable.print_table()
    myTable.print_primary_key()
    myTable.print_functional_dependencies()
    myTable.print_mvds()
    
    normalize_to_form(myTable, normal_form)
    
    if find_highest_form.strip() == "1":
        print()
        find_normal_form(myTable)
    
    # DEBUG

def debug_main(myTable: table.Table):
    print("\nOriginal Table")
    myTable.print_table()
    myTable.print_primary_key()
    myTable.print_functional_dependencies()
    myTable.print_mvds()
    
    super_keys = myTable.get_superkeys()
    super_keys.sort(key=len)
    print(f"Super keys: ")
    for key in super_keys:
        print(key)
    candidate_keys = myTable.get_candidate_keys()
    print(f"Candidate keys:")
    for key in candidate_keys:
        print([myTable.columns[i] for i in key])
    
    fnf_tables: list[table.Table] = normalizer.first_normal_form(myTable)
    print("\n1NF")
    print(fnf_tables)
    for fnf in fnf_tables:
        fnf.print_table()
        fnf.print_functional_dependencies()
        fnf.print_mvds()
    
    snf_tables: list[table.Table] = []
    for fnf in fnf_tables:
        snf_tables.extend(normalizer.second_normal_form(fnf))
    
    print("\n2NF")
    for snf in snf_tables:
        snf.print_table()
        snf.print_primary_key()
        snf.print_functional_dependencies()
        snf.print_mvds()
    
    tnf_tables: list[table.Table] = []
    for snf in snf_tables:
        tnf_tables.extend(normalizer.third_normal_form(snf))
    
    print("\n3NF")
    for tnf in tnf_tables:
        tnf.print_table()
        tnf.print_primary_key()
        tnf.print_functional_dependencies()
        tnf.print_mvds()
        
    bcnf_tables: list[table.Table] = []
    for tnf in tnf_tables:
        bcnf_tables.extend(normalizer.boyce_codd_normal_form(tnf))
    
    print("\nBCNF")
    for bcnf in bcnf_tables:
        bcnf.print_table()
        bcnf.print_primary_key()
        bcnf.print_functional_dependencies()
        bcnf.print_mvds()
    
    fnf_tables: list[table.Table] = []
    for bcnf in bcnf_tables:
        fnf_tables.extend(normalizer.forth_normal_form(bcnf))
    
    print("\n4NF")
    for fnf in fnf_tables:
        fnf.print_table()
        fnf.print_primary_key()
        fnf.print_functional_dependencies()
        fnf.print_mvds()


if __name__ == "__main__":
    main()
    #debug()
    #debug2()
