
#Task Manager CLI Roadmap Practice Project

#-------------------------------------------------------------------------------------------------

import sys #importing sys module to handle command line arguments
import json #importing json module to handle saving and loading tasks from a file

#global variables

task_list = {} #empty dictionary to hold tasks
next_task_ID = 1 #variable to keep track of the next task ID to assign

TASKS_FILE = "tasks.json" #constant for the filename to save and load tasks

#Task Statuses Constants

STATUS_COMPLETE = "complete"
STATUS_IN_PROGRESS = "in progress" 
STATUS_INCOMPLETE = "incomplete"

VALID_STATUSES = [STATUS_COMPLETE, STATUS_IN_PROGRESS, STATUS_INCOMPLETE] #list of valid task statuses

#-------------------------------------------------------------------------------------------------

def load_tasks(): #function to load tasks from a file
    global task_list, next_task_ID #declare task_list and next_task_ID as global to modify within function

    try:
        with open(TASKS_FILE, "r") as file: #opens the tasks file in read mode 
            task_list = json.load(file) #loads the tasks from the file into the task_list dictionary

        task_list = {int(task_ID): task_data for task_ID, task_data in task_list.items()} #converts the task IDs from strings to integers

        if task_list:
            next_task_ID = max(int(task_ID) for task_ID in task_list.keys()) + 1 #sets next_task_ID to one more than the highest existing task ID
                
    except FileNotFoundError: #if the file does not exist, it will be created when tasks are saved
        task_list = {} #initialize task_list as an empty dictionary
        next_task_ID = 1 #initialize next_task_ID to 1

#-------------------------------------------------------------------------------------------------

#view task functions

def view_tasks(): #function to view the current list of tasks
    print("Task List:") #header for task list

    for task_ID, task_data in task_list.items():
        if task_data["task_status"] == STATUS_COMPLETE:
            print(f"{task_ID}: [x] {task_data['task_name']}") #prints complete tasks with a checkbox

        elif task_data["task_status"] == STATUS_IN_PROGRESS:
            print(f"{task_ID}: [~] {task_data['task_name']}") #prints in progress tasks with a checkbox

        elif task_data["task_status"] == STATUS_INCOMPLETE:
            print(f"{task_ID}: [ ] {task_data['task_name']}") #prints incomplete tasks with a checkbox



def view_completed_tasks(): #function to view only completed tasks
    print("Completed Tasks:") #header for complete tasks list

    for task_ID, task_data in task_list.items():
        if task_data['task_status'] == STATUS_COMPLETE:
            print(f"{task_ID}: [x] {task_data['task_name']}") #prints complete tasks with a 'x' marked checkbox



def view_in_progress_tasks(): #function to view only in progress tasks
    print("Tasks In Progress:") #header for in progress tasks list

    for task_ID, task_data in task_list.items():
        if task_data['task_status'] == STATUS_IN_PROGRESS:
            print(f"{task_ID}: [~] {task_data['task_name']}") #prints in progress tasks with a '~' marked checkbox



def view_incomplete_tasks(): #function to view only incomplete tasks
    print("Incomplete Tasks:") #header for incomplete tasks list

    for task_ID, task_data in task_list.items():
        if task_data['task_status'] == STATUS_INCOMPLETE:
            print(f"{task_ID}: [ ] {task_data['task_name']}") #prints incomplete tasks with a blank checkbox

#-------------------------------------------------------------------------------------------------

#task management functions

def add_task(): #function to add a task to the list
    new_task = input("Enter New Task: ") #prompt for adding task to list
    
    global next_task_ID #declare next_task_ID as global to modify within function

    task_list[next_task_ID] = { #adds new task to the dictionary
        "task_name": new_task, 
        "task_status": STATUS_INCOMPLETE }
    
    next_task_ID += 1 #generates a new task ID for the next task



def update_task_name(): #function to edit an existing task in the list

    task_to_edit = int(input("Enter Task ID to Edit: ")) #prompt for task ID to edit

    if task_to_edit not in task_list: #checks if the task ID is in the list before trying to edit it
        print("Task ID not found, enter valid Task ID.") #error message if task ID is not found
        return
    
    new_task_name = input("Enter New Task Name: ") #prompt for new task name
    task_list[task_to_edit]["task_name"] = new_task_name #updates the task name in the dictionary



def update_task_status(): #function to edit the status of an existing task in the list

    task_to_edit = int(input("Enter Task ID to Edit: ")) #prompt for task ID to edit

    if task_to_edit not in task_list: #checks if the task ID is in the list before trying to edit it
        print("Task ID not found, enter valid Task ID.") #error message if task ID is not found
        return
        
    print('1. Complete') #option for complete status
    print('2. In Progress') #option for in progress status
    print('3. Incomplete') #option for incomplete status

    status_choice = int(input("choose new task status: ")) #prompt for new task status

    if status_choice == 1:
        updated_status = STATUS_COMPLETE #sets new task status to complete
    elif status_choice == 2:
        updated_status = STATUS_IN_PROGRESS #sets new task status to in progress
    elif status_choice == 3:
        updated_status = STATUS_INCOMPLETE #sets new task status to incomplete
    else:
        print("Invalid status choice, enter a number between 1 and 3.") #error message for invalid status choice
        return
    
    task_list[task_to_edit]["task_status"] = updated_status #updates the task status in the dictionary

#-------------------------------------------------------------------------------------------------

def remove_task(): #function to remove a task from the list

    task_to_delete = int(input("Enter Task ID to Remove: ")) #prompt for task ID to remove

    if task_to_delete not in task_list: #checks if the task ID is in the list
        print("Task ID not found, enter valid Task ID.") #error message if task ID is not found
        return False #returns false to indicate the task was not removed

    del task_list[task_to_delete] #removes the task from the dictionary
    return True #returns true to indicate the task was successfully removed



def clear_completed_tasks(): #function to clear all completed tasks from the list
    completed_tasks_list = [] #creates an empty list to hold completed task IDs

    for task_ID, task_data in task_list.items():
        if task_data['task_status'] == STATUS_COMPLETE:
            completed_tasks_list.append(task_ID)

    for task_ID in completed_tasks_list:
        del task_list[task_ID]
    return True
            
#-------------------------------------------------------------------------------------------------

def save_tasks(): #function to save tasks to a file
    with open(TASKS_FILE, "w") as file: #opens the tasks file in write mode
        json.dump(task_list, file) #saves the task_list dictionary to the file in JSON format

#-------------------------------------------------------------------------------------------------

load_tasks() #calls the load_tasks function to load tasks from the file when the program starts

if len(sys.argv) > 1: #checks if there are command line arguments provided
    command = sys.argv[1] #gets the first command line argument as the command


    if command == "view":
        view_tasks() #calls the view_tasks function to display all tasks
    elif command == "view_completed":
        view_completed_tasks() #calls the view_completed_tasks function to display only completed tasks
    elif command == "view_in_progress":
        view_in_progress_tasks() #calls the view_in_progress_tasks function to display only in progress tasks
    elif command == "view_incomplete":
        view_incomplete_tasks() #calls the view_incomplete_tasks function to display only incomplete tasks


    elif command == "add":
        add_task() #calls the add_task function to add a new task
        save_tasks() #calls the save_tasks function to save the new task to the file
    elif command == "update_name":
        update_task_name() #calls the update_task_name function to edit an existing task's name
        save_tasks() #calls the save_tasks function to save any changes made to the tasks after updating a task's name
    elif command == "update_status":
        update_task_status() #calls the update_task_status function to edit an existing task's status
        save_tasks() #calls the save_tasks function to save any changes made to the tasks after updating a task's status


    elif command == "remove":
        remove_task() #calls the remove_task function to remove a task from the list
        save_tasks() #calls the save_tasks function to save any changes made to the tasks after removing a task
    elif command == "clear_completed":
        clear_completed_tasks() #calls the clear_completed_tasks function to clear all completed tasks from the list
        save_tasks() #calls the save_tasks function to save any changes made to the tasks after clearing completed tasks


    else:
        print("Invalid command, please enter a valid command.") #error message for invalid command

#-------------------------------------------------------------------------------------------------