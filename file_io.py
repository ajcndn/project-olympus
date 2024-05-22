from datetime import datetime

def save_markdown(task_output):
    # Get today's date in the format YYYY-MM-DD
    today_date = datetime.now().strftime('%Y-%m-%d')
    # Set the filename with today's date
    filename = f"{today_date}.md"
    # Check if task_output has a result attribute
    if hasattr(task_output, 'result'):
        # Check if result is callable (i.e., a method) and call if necessary
        if callable(task_output.result):
            result_content = task_output.result()  # Call the method
        else:
            result_content = task_output.result  # Use the attribute directly
        
        # Write the task output to the markdown file
        with open(filename, 'w') as file:
            file.write(result_content)
        print(f"Summary saved as {filename}")
    else:
        raise AttributeError("task_output object does not have a 'result' attribute.")


