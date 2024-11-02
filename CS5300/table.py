# Programmer: Amrit Bhaganagare 12619462 and Venkata Dheeraj Reddy Busireddy 12576469

class Table:
    
    def __init__(
        self, 
        columns: list[str], 
        tuples: 'list[tuple[str]]' = []
    ):
        self.columns: list[str] = columns
        
        self.tuples: 'list[tuple[str]]' = []
        for tuple in tuples:
            self.add_tuple(tuple)
        
        # These will be set in other functions
        self.primary_key: list[int] = []
        self.funct_depends: 'list[tuple[list[int], list[int]]]'= []
        self.multi_funct_depends: 'list[tuple[int, int]]' = []
        
    def set_primary_key(self, attributes: list[str])-> None:
        '''
        This takes in one or more attributes and sets self.primary_key to the indexes of them in self.columns\n
        Returns a RuntimeError if any attribute is not found
        '''
        for attribute in attributes:
            self.check_attribute_if_valid(attribute)
        
        for attribute in attributes:
            self.primary_key.append(self.columns.index(attribute))
    
    def check_if_superkey(self, key: list[int]) -> bool:
        '''
        This takes in a list of integers representing attributes and outputs True if they fully describe the whole table
        '''
        # We remove attributes from this list if they are described by some dependent
        remaining_attributes = list(range(len(self.columns)))
        
        # All attributes describe themselves, so we remove any that appear explicitly in the key
        for attr in key:
            remaining_attributes.remove(attr)
        if len(remaining_attributes) == 0:
            return True
        
        # We create a copy of the key so that we can add dependents to it
        effective_key = key.copy()
        # We now loop until we empty remaining attributes because they are described by the effective key (return statement)
        # Or we run out of new functional dependencies to match with (invariant is failed to be set)
        invariant = True
        while invariant:
            invariant = False
            
            # Now we go through each dependency and see if we have a match that hasnt yet occured
            for det, dep in self.funct_depends:
                det_in_effective_key = all(attr in effective_key for attr in det)
                if not det_in_effective_key:
                    continue
                dep_in_effective_key = all(attr in effective_key for attr in dep)
                if dep_in_effective_key:
                    # Means we already have explored this dependency
                    continue
                for attr in dep:
                    # Remove from remaining attributes
                    if attr in remaining_attributes:
                        remaining_attributes.remove(attr)
                    # Return true if remaining is empty
                    if len(remaining_attributes) == 0:
                        return True # <---------------- If we empty remaining attrubutes
                    # Add to effective key
                    if not (attr in effective_key):
                        effective_key.append(attr)
                invariant = True
                break
        # In this case, the invariant is not set 
        # Meaning we have run out of functional dependencies before we could empty remaining attributes
        return False
    
    def super_key_recursion(self, current_attributes: list[int], super_keys: list[list[int]] = []) -> list[list[int]]:
        '''
        Recursive helper function for finding superkeys\n
        Dont call this outside of the class, itll be weird
        '''
        # In this function, we are working from the top down,
        # Meaning we are starting with an attributes list containing all attributes
        # And eliminating one at each recursion step, once for each remaining attribute
        
        # Stop condition(s)
        # 1) If we are exploring a duplicate possibility
        if current_attributes in super_keys:
            return super_keys
        # 2) If this recursion is no longer a superkey
        is_superkey = self.check_if_superkey(current_attributes)
        #print(f"{[self.columns[i] for i in current_attributes]} is superkey? {is_superkey}") # Debug
        if not is_superkey:
            return super_keys
        
        # Add the current iteration to the list of super_keys
        super_keys.append(current_attributes)
        
        # Remove one attribute and recur for each attribute removed
        for attr in current_attributes:
            new_attributes = current_attributes.copy()
            new_attributes.remove(attr)
            #print(f"Testing key: {[self.columns[i] for i in new_attributes]}")
            
            self.super_key_recursion(new_attributes, super_keys)
        return super_keys
    
    def get_superkeys(self) -> list[list[int]]:
        '''
        This returns a list of integers representing superkeys of the table
        '''
        current_columns = list(range(len(self.columns)))
        supa_keys = self.super_key_recursion(current_columns, [])
        return supa_keys
            
    def get_candidate_keys(self) -> list[list[int]]:
        '''
        This returns a list of lists of integers representing candidate keys of the table
        '''
        super_keys = self.get_superkeys()
        super_keys.sort(key=len)
        
        candidate_keys: list[list[int]] = []
        
        for pot_can in super_keys:
            is_candidate = True
            for attr in pot_can:
                temp = pot_can.copy()
                temp.remove(attr)
                if temp in super_keys:
                    is_candidate = False
                    break
            if is_candidate:
                candidate_keys.append(pot_can)
        
        return candidate_keys
            
    def get_primes(self) -> list[int]:
        '''
        This returns a list of integers representing the index of attributes that are prime
        '''
        candidate_keys = self.get_candidate_keys()
        
        prime_attributes = []
        for key in candidate_keys:
            prime_attributes.extend(attr for attr in key if attr not in prime_attributes)
        return prime_attributes
    
    def set_functional_dependencies(self, *dependencies: tuple[list[str], list[str]]) -> None:
        '''
        This takes in one or more functional dependencies in the form of tuples (a, b) where a -> b.\n 
        And sets self.funct_depends to these values\n
        Returns a RuntimeError if any attribute is not found
        '''
        for dependency in dependencies:
            determinant = dependency[0]
            determ_list: list[int] = []
            for attr in determinant:
                self.check_attribute_if_valid(attr)
            dependent = dependency[1]
            depend_list: list[int] = []
            for attr in dependent:
                self.check_attribute_if_valid(attr)
            
            for attr in determinant:
                index = self.columns.index(attr)
                determ_list.append(index)
            for attr in dependent:
                index = self.columns.index(attr)
                depend_list.append(index)
            
            self.funct_depends.append((determ_list, depend_list))
            
    def get_determinants(self, dependent: int) -> list[list[int]]:
        '''
        This takes in a dependent (as an int) and outputs the determinants as a list of lists of ints\n
        Returns empty list if there are no determinants
        '''
        determinants = []
        for det, dep in self.funct_depends:
            if not (dependent in dep):
                continue
            determinants.append(det)
        return determinants
    
    def get_dependents(self, determinant: list[int]) -> list[int]:
        '''
        This takes in a determinant (as a list of ints) and outputs the dependents as a list of ints\n
        Returns empty list if no dependents are found
        '''
        for det, dep in self.funct_depends:
            if determinant != det:
                continue
            return dep
        return []
    
    def get_partial_dependencies(self) -> list[tuple[list[int], list[int]]]:
        '''
        This will return all partial dependencies in the table
        That is, all dependencies where the dependent is non-prime and partially dependent on any candidate key
        This should only be run on a table that is in 1nf
        '''
        dependencies: list[tuple[list[int], list[int]]] = []
        # Get all non-primes
        primes = self.get_primes()
        candidate_keys = self.get_candidate_keys()
        non_primes = list(range(len(self.columns)))
        for attr in primes:
            non_primes.remove(attr)
            
        # For each non-prime attribute, check if its determinant is a proper subset of the primary key
        # TODO this can be done better by searching through FDs instead of non prime attributes? maybe not, but think on it
        for attr in non_primes:
            determinants = self.get_determinants(attr)
            
            #partial_determinant: list[int] = []
            for key in candidate_keys:
                for det in determinants:
                    det_subset_key = all(attr in key for attr in det)
                    if not det_subset_key:
                        continue
                    det_is_key = det == key
                    if det_is_key:
                        continue
                    
                    # If we get here, the determinant is a proper subset of some candidate key
                    # Add the full dependency to the list of partial_dependencies
                    dependents = self.get_dependents(det)
                    dep: list[int] = []
                    # Check if a dependent is a prime attribute and if it isnt, add it to the list of dependencies to add to the new FD
                    for attr in dependents:
                        if not (attr in primes):
                            dep.append(attr)
                    new_depend = (det, dep)
                    if not (new_depend in dependencies):
                        dependencies.append(new_depend)
                        
        return dependencies
    
    def get_transitive_dependencies(self) -> list[tuple[list[int], list[int]]]:
        '''
        This will return all transitive dependencies in the table\n
        That is, all dependencies where the dependent is non-prime and transitivley dependent on the primary key\n
        This should only be run on a table that is in 2nf
        '''
        dependencies: list[tuple[list[int], list[int]]] = []
        # Get all non-primes
        primes = self.get_primes()
        non_primes = list(range(len(self.columns)))
        for attr in primes:
            non_primes.remove(attr)
        
        # For all non-trivial FDs (explicitly defined FDs), check if the determinant is non-prime
        # We assume that all non-prime attributes are fully functionally dependent on primary key
        
        for det, dep in self.funct_depends:
            det_is_non_prime = all(attr in non_primes for attr in det)
            
            if not det_is_non_prime:
                continue
            # If the determinant is non-prime, we see if its dependents are non-prime as well
            # If an attribute in the dependents is non-prime, we add it to the list of dependents
            dependent: list[int] = []
            for attr in dep:
                if not (attr in primes):
                    dependent.append(attr)
            if len(dependent) == 0:
                continue
            new_depend = (det, dependent)
            if not (new_depend in dependencies):
                dependencies.append(new_depend)
        return dependencies

    def get_non_superkey_dependencies(self) -> list[tuple[list[int], list[int]]]:
        '''
        This returns all dependencies in the table such that\n
        Where there is a non-trivial functional dependency X -> Y, X is not a superkey
        '''
        dependencies: list[tuple[list[int], list[int]]] = []
        # We need to check, for each functional dependency in the table, if the determinant is a superkey
        super_keys = self.get_superkeys()
        for det, dep in self.funct_depends:
            det_is_superkey = det in super_keys
            if not det_is_superkey:
                new_depend = (det, dep)
                dependencies.append(new_depend)
        return dependencies
        
    def set_multivalue_funct_depends(self, *dependencies: tuple[int, int]) -> None:
        '''
        This takes in two multivalue functional dependencies in the form of tuples (a, b) where a ->-> b.\n 
        And sets self.funct_depends to these values\n
        Returns a RuntimeError if any attribute is not found or if any value other than two functional dependencies are inputted
        '''
        for dependency in dependencies:
            determinant = dependency[0]
            self.check_attribute_if_valid(determinant)
            dependent = dependency[1]
            self.check_attribute_if_valid(dependent)
            
            det_index = self.columns.index(determinant)
            dep_index = self.columns.index(dependent)
            
            new_dependency = (det_index, dep_index)
            
            self.multi_funct_depends.append(new_dependency)
    
    def get_mvd_dependents(self, determinant: int) -> list[int]:
        '''
        This takes in a determinant (as a list of ints) and outputs the dependents of the mvd as a list of ints\n
        Returns empty list if no dependents are found
        '''
        dependents = []
        for det, dep in self.multi_funct_depends:
            if determinant != det:
                continue
            dependents.append(dep)
        return dependents
        
    def check_attribute_if_valid(self, attr: str) -> None:
        if not (attr in self.columns):
            raise RuntimeError(f"'{attr}' is not a valid attribute")
    
    def add_tuple(self, tuple: tuple[str]) -> None:
        if len(tuple) != len(self.columns):
            raise RuntimeError(f"{tuple} values dont line up with {self.columns}")
        self.tuples.append(tuple)
    
    def add_tuples(self, tuples: list[tuple[str]]) -> None:
        '''
        This takes in a list of tuples and adds them to the tuple list
        '''
        for tuple in tuples:
            self.add_tuple(tuple)
    
    def remove_tuple(self, primary_key: tuple) -> None:
        '''
        Takes in a tuple of the PK values of the specific tuple to remove.\n
        Make sure the order of these values match the order of the attributes you entered to set the PK\n
        Raises a runtime error if no tuple is found or if more than one tuple is found
        To keep it simple, enter these in the order they appear in the table <----!!!!
        '''
        tuples_to_search = self.tuples.copy()
        # TODO make sure that the PK values are entered in the order they appear in the column list (just sort them)
        if len(primary_key) != len(self.primary_key):
            raise RuntimeError(f"{primary_key} values dont line up with {self.primary_key}")
        # For each primary key value
        for i in range(len(primary_key)):
            matching_tuples = []
            pk_index = self.primary_key[i]
            # For each tuple in the list of tuples
            for tuple in tuples_to_search:
                if tuple[pk_index] == primary_key[i]: 
                    matching_tuples.append(tuple)
            tuples_to_search = matching_tuples.copy()
        if len(tuples_to_search) == 0:
            raise RuntimeError(f"No tuple found with PK {primary_key}")
        if len(tuples_to_search) != 1:
            raise RuntimeError(f"PK {primary_key} does not uniquely describe tuple, returned {tuples_to_search}")
        self.tuples.remove(tuples_to_search[0])
    
    def get_columns(self, indexes: list[int]) -> str:
        '''
        This takes in a list of indexes to specific columns\n
        And returns the names of those columns, formatted into a string, with a comma seperating them\n
        Mostly just a helper function so that I dont have to repeat code i wrote over and over
        '''
        string = ""
        
        first_elem = self.columns[indexes[0]]
        string += first_elem
        for i in indexes[1:]:
            string += f", {self.columns[i]}"
        
        return string

    def print_table(self) -> None:
        """
        This will print the table data in a formatted manner
        """
        # Print headers
        header = ' | '.join(self.columns)
        print(header)

    # Print separator line
        separator = '+'.join('-' * (len(col) + 2) for col in self.columns)
        print(separator)

    # Print rows
        for row in self.tuples:
            formatted_row = ' | '.join(str(col) for col in row)
            print(formatted_row)

    # Print closing separator line
        print(separator)
    
    def print_primary_key(self) -> None:
        '''
        Prints the primary key for the table
        '''
        pk_str = self.get_columns(self.primary_key)
        print(f"PK: {{ {pk_str} }}")

    def print_functional_dependencies(self) -> None:
        '''
        Prints list of functional dependencies
        '''
        if len(self.funct_depends) == 0:
            return
        print("Functional dependencies:")
        for dependency in self.funct_depends:
            determinant = dependency[0]
            determ_str = self.get_columns(determinant)
            
            depenant = dependency[1]
            depend_str = self.get_columns(depenant)
            
            print(f" - {determ_str} -> {depend_str}")
    
    def print_mvds(self) -> None:
        '''
        Prints list of multivalue functional dependencies
        '''
        if len(self.multi_funct_depends) == 0:
            return
        print("Multivalue Functional dependencies:")
        for dependency in self.multi_funct_depends:
            determinant = dependency[0]
            determ_str = self.get_columns([determinant])
            
            depenant = dependency[1]
            depend_str = self.get_columns([depenant])
            print(f" - {determ_str} -> {depend_str}")
