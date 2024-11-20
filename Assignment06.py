# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_Starter
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Adam Savage,20241117,Modified script to a Class/SoC structure
# ------------------------------------------------------------------------------------------ #
from typing import TextIO
import json

# Define the Data Constants
FILE_NAME: str = "Enrollments.json"
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''

# Define the Data Variables and constants
students: list = []
menu_choice: str = ""


# Begin Classes and Functions definitions
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files
    ChangeLog: (Who, When, What)
    Adam Savage,20241117,Created class
    Adam Savage,20241117,Added read_data function
    Adam Savage,20241117,Added write_data function
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function reads data from a JSON file, copies it into the object 'student_data', and returns it.
        ChangeLog: (Who, When, What)
        Adam Savage,20241117,Created function
        :param file_name: source data file
        :param student_data: the object the data file is written to
        :return: none
        """
        # read data from JSON
        file: TextIO = None
        try:
            file = open(file_name, 'r')
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("JSON file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function writes data from a list of dictionaries-formatted object into a JSON file.
        ChangeLog: (Who, When, What)
        Adam Savage,20241117,Created function
        :param file_name: The destination file to write to.
        :param student_data: The list of dictionaries-formatted object holding the data.
        :return: none
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file.closed == False:
                file.close()


class IO:
    """
    A collection of presentation layer functions that manage user input and output
    ChangeLog: (Who, When, What)
    Adam Savage,20241117,Created class
    Adam Savage,20241117,Added function to handle error outputs
    Adam Savage,20241117,Added function to display the selection menu
    Adam Savage,20241117,Added function to receive user input
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        The function returns error message details to the user.
        ChangeLog: (Who, When, What)
        Adam Savage,20241117,Created function
        :param message: A custom message displayed to the user.
        :param error: The error code to reference technical information.
        :return: none
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        This function displays the selection menu to users.
        ChangeLog: (Who, When, What)
        Adam Savage,20241117,Created function
        :param menu: The menu constant to display to the user.
        :return: none
        """
        print(menu)
        pass

    @staticmethod
    def input_menu_choice():
        """
        A function to query the user and return the user-provide input.
        ChangeLog: (Who, When, What)
        Adam Savage,20241117,Created function
        :return: Returns the user-provided input
        """
        while True:
            user_input = input("Select an option from the menu: ")
            # if not 0 < int(user_input) < 5:
            #     print("\nPlease select only 1, 2, 3, or 4\n")
            #     continue
            if not user_input in ["1", "2", "3", "4"]:
                print("\nPlease select only 1, 2, 3, or 4\n")
                continue
            else:
                return user_input

    @staticmethod
    def input_student_data(student_data: list):
        """
        This function collects user input for student first name, last name, and course and assembled it into a dictionary to return.
        :param student_data: the list of dictionaries of student names and courses
        :return: returns student_data
        """
        global students
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should only contain letters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should only contain letters.")
            course_name = input("Please enter the name of the course: ")
            student_data = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            students.append(student_data)
            print(f"\nYou have registered {student_first_name} {student_last_name} for {course_name}.")
        except Exception as e:
            IO.output_error_messages(Exception=e)
        finally:
            return students

    @staticmethod
    def output_student_courses(student_data: list):
        """
        This function takes in a list of dictionaries and displays each item.
        :param student_data: the list of data
        :return: none
        """
        print()
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} {student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)


# End Classes and Functions definitions


# Read in pre-existing JSON file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Core program
while (True):

    # Present the menu of choices
    IO.output_menu(MENU)

    # Solicit a menu selection from the user
    menu_choice = IO.input_menu_choice()

    # Receive enrollment input from the user
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)

    # Present the current data to the user
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)

    # Save the data to a JSON file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        print()
        print("These data written to file:")
        IO.output_student_courses(student_data=students)

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")
