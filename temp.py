import pyreadline

# Function to provide auto-complete options
def complete(text, state):
    options = ['apple', 'banana', 'cherry', 'date', 'grape']  # Your list of options
    matches = [option for option in options if option.startswith(text)]
    if state < len(matches):
        return matches[state]
    else:
        return None

# Set the autocomplete function
pyreadline.parse_and_bind('tab: complete')
pyreadline.set_completer(complete)

# Test your autocomplete functionality
while True:
    user_input = input('Enter your choice: ')
    print('You entered:', user_input)
