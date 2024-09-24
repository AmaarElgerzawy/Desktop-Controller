import telebot  # Importing the telebot library for Telegram bot functionalities.
from enum import Enum  # Importing Enum for creating enumerations.
import pyautogui  # Importing pyautogui for controlling the mouse and keyboard.
from PIL import Image  # Importing the Image class from PIL (Pillow) for image processing.
import os  # Importing the os module for interacting with the operating system.
import tkinter as tk  # Importing tkinter for creating a graphical user interface.
import json  # Importing json for working with JSON data.
import threading  # Importing threading for running tasks in separate threads.
from tkinter import messagebox  # Importing messagebox from tkinter for showing pop-up dialogs.
import traceback  # Importing traceback for handling and logging exceptions.

global bot  # Declaring a global variable 'bot'.
bot = None  # Initializing 'bot' with a value of None.

pyautogui.FAILSAFE = False  # Disabling the fail-safe feature of pyautogui.

# Creating a class named 'DesktopController' that inherits from 'telebot.TeleBot'.
class DesktopController(telebot.TeleBot):
    # Inner class for defining constant values using enumerations.
    class Constants(Enum):
        START:str = "START"  # Constant for the START command.

        RIGTH_CLICK:str = "RIGTH_CLICK"  # Constant for the RIGHT_CLICK command.
        LEFT_CLICK:str = "LEFT_CLICK"  # Constant for the LEFT_CLICK command.
        DOUPLE_CLICK:str = "DOUPLE_CLICK"  # Constant for the DOUBLE_CLICK command.

        SCROLL_END:str = "SCROLL_END"  # Constant for the SCROLL_END command.
        SCROLL_START:str = "SCROLL_START"  # Constant for the SCROLL_START command.
        SCROLL_UP:str = "SCROLL_UP"  # Constant for the SCROLL_UP command.
        SCROLL_DOWN:str = "SCROLL_DOWN"  # Constant for the SCROLL_DOWN command.

        TYPE:str = "TYPE"  # Constant for the TYPE command.
        ENTER:str = "ENTER"  # Constant for the ENTER command.
        ESC:str = "ESC"  # Constant for the ESC command.
        SELECT_ALL:str = "SELECT_ALL"  # Constant for the SELECT_ALL command.
        BACKSPACE:str = "BACKSPACE"  # Constant for the BACKSPACE command.

        DELETE:str = "DELETE"  # Constant for the DELETE command.
        SCREEN_SHOT:str = "SCREEN_SHOT"  # Constant for the SCREEN_SHOT command.

        CTRL_UP:str = "CTRL_UP"  # Constant for the CTRL_UP command.
        CTRL_DOWN:str = "CTRL_DOWN"  # Constant for the CTRL_DOWN command.
        ALT_UP:str = "ALT_UP"  # Constant for the ALT_UP command.
        ALT_DOWN:str = "ALT_DOWN"  # Constant for the ALT_DOWN command.

        SHIFT_UP:str = "SHIFT_UP"  # Constant for the SHIFT_UP command.
        SHIFT_DOWN:str = "SHIFT_DOWN"  # Constant for the SHIFT_DOWN command.
        TAB:str = "TAB"  # Constant for the TAB command.

        RIGTH_ARROW:str = "RIGTH_ARROW"  # Constant for the RIGHT_ARROW command.
        LEFT_ARROW:str = "LEFT_ARROW"  # Constant for the LEFT_ARROW command.

    # Constructor method initializing the 'DesktopController' class.
    def __init__(self, token, target_width, target_height):
        super().__init__(token)  # Initializing the superclass 'telebot.TeleBot' with a token.
        self.target_width = target_width  # Setting the target width for scaling.
        self.target_height = target_height  # Setting the target height for scaling.

        self.setup_handlers()  # Setting up message handlers for the bot.
    
    # Method for converting positions from one resolution to another.
    def convert_positions_to_resolution(self, positions, original_width, original_height):
        scale_width = self.target_width / original_width  # Calculating the scale factor for width.
        scale_height = self.target_height / original_height  # Calculating the scale factor for height.
        
        scaled_positions = [int(positions[0] * scale_width), int(positions[1] * scale_height)]  # Scaling the positions.

        print(scaled_positions)  # Printing the scaled positions for debugging.
        return scaled_positions  # Returning the scaled positions.

    # Method for finding the center of a circle with a specified color in an image.
    def find_circle_center(self, image, target_color=(245,15,245), tolerance=30):
        image = image.convert('RGB')  # Converting the image to RGB format.
        
        width, height = image.size  # Getting the width and height of the image.
        
        sum_x = 0  # Initializing the sum of x-coordinates.
        sum_y = 0  # Initializing the sum of y-coordinates.
        count = 0  # Initializing the count of matching pixels.
        
        # Looping through each pixel in the image.
        for x in range(width):
            for y in range(height):
                pixel_color = image.getpixel((x, y))  # Getting the color of the current pixel.
                # Checking if the pixel color matches the target color within the specified tolerance.
                if all(abs(pixel_color[i] - target_color[i]) <= tolerance for i in range(3)):
                    sum_x += x  # Adding the x-coordinate to the sum.
                    sum_y += y  # Adding the y-coordinate to the sum.
                    count += 1  # Incrementing the count.
        
        # If matching pixels are found, return the average position as the center.
        if count > 0:
            center_x = sum_x // count
            center_y = sum_y // count
            return (center_x, center_y)
        else:
            return None  # Return None if no matching pixels are found.
    
    # Method for setting up message handlers for the bot.
    def setup_handlers(self):
        @self.message_handler(commands=[self.Constants.START.value])
        def send_start(message):
            cmds = "\n".join([f"/{x.value}" for x in self.Constants])  # Creating a list of available commands.
            self.reply_to(message, cmds)  # Sending the list of commands as a reply.

        @self.message_handler(content_types=['photo'])
        def LEFT_CLICK(message): 
            file_id = message.photo[-1].file_id  # Getting the file ID of the uploaded photo.
            file_info = bot.get_file(file_id)  # Getting file information from Telegram.
            downloaded_file = bot.download_file(file_info.file_path)  # Downloading the photo from Telegram.
            
            temp_image_path = "temp_image.jpg"  # Temporary file path for saving the photo.
            with open(temp_image_path, 'wb') as new_file:
                new_file.write(downloaded_file)  # Saving the downloaded photo to the temporary file.
            
            image = Image.open(temp_image_path)  # Opening the saved image using PIL.
            
            center_position = self.find_circle_center(image)  # Finding the center of the circle in the image.
            x, y = self.convert_positions_to_resolution(center_position, image.size[0], image.size[1])  # Scaling the center position.
            
            os.remove(temp_image_path)  # Removing the temporary image file.
            
            if center_position:
                print(f"Clicking at position: ({x}, {y})")  # Printing the click position.
                pyautogui.click(x, y)  # Performing a click at the scaled position.
            else:
                print("No circle with the specified color found.")  # Printing a message if no circle is found.

        @self.message_handler(commands=[self.Constants.LEFT_CLICK.value])
        def LEFT_CLICK(message):
            pyautogui.click()  # Performing a left click.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.RIGTH_CLICK.value])
        def RIGTH_CLICK(message):
            pyautogui.rightClick()  # Performing a right click.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.DOUPLE_CLICK.value])
        def DOUPLE_CLICK(message):
            pyautogui.doubleClick()  # Performing a double click.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SCROLL_START.value])
        def SCROLL_START(message):
            pyautogui.scroll(10000)  # Scrolling up.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SCROLL_END.value])
        def SCROLL_END(message):
            pyautogui.scroll(-10000)  # Scrolling down.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SCROLL_DOWN.value])
        def SCROLL_DOWN(message):
            pyautogui.scroll(-1000)  # Scrolling down.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SCROLL_UP.value])
        def SCROLL_UP(message):
            pyautogui.scroll(1000)  # Scrolling up.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.TYPE.value])
        def TYPE(message):
            pyautogui.typewrite(message.text[6:], interval=0.2)  # Typing the message after the command with a delay.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.ENTER.value])
        def ENTER(message):
            pyautogui.press("enter")  # Pressing the Enter key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.
        
        @self.message_handler(commands=[self.Constants.ESC.value])
        def ESC(message):
            pyautogui.press("esc")  # Pressing the Escape key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.DELETE.value])
        def DELETE(message):
            pyautogui.press("delete")  # Pressing the Delete key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SHIFT_DOWN.value])
        def SHIFT_DOWN(message):
            pyautogui.keyDown("shift")  # Holding down the Shift key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.TAB.value])
        def TAB(message):
            pyautogui.keyDown("tab")  # Pressing the Tab key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SHIFT_UP.value])
        def SHIFT_UP(message):
            pyautogui.keyUp("shift")  # Releasing the Shift key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.CTRL_DOWN.value])
        def CTRL_DOWN(message):
            pyautogui.keyDown("ctrl")  # Holding down the Ctrl key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.ALT_DOWN.value])
        def ALT_DOWN(message):
            pyautogui.keyDown("alt")  # Holding down the Alt key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.CTRL_UP.value])
        def CTRL_UP(message):
            pyautogui.keyUp("ctrl")  # Releasing the Ctrl key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.ALT_UP.value])
        def ALT_UP(message):
            pyautogui.keyUp("alt")  # Releasing the Alt key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.
        
        @self.message_handler(commands=[self.Constants.BACKSPACE.value])
        def BACKSPACE(message):
            pyautogui.press("backspace")  # Pressing the Backspace key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.
        
        @self.message_handler(commands=[self.Constants.RIGTH_ARROW.value])
        def RIGTH_ARROW(message):
            pyautogui.press("right")  # Pressing the Right Arrow key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.
            
        @self.message_handler(commands=[self.Constants.LEFT_ARROW.value])
        def LEFT_ARROW(message):
            pyautogui.press("left")  # Pressing the Left Arrow key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.
        
        @self.message_handler(commands=[self.Constants.SELECT_ALL.value])
        def SELECT_ALL(message):
            pyautogui.keyDown("CTRL")  # Holding down the Ctrl key.
            pyautogui.press("a")  # Pressing the "a" key to select all.
            pyautogui.keyUp("CTRL")  # Releasing the Ctrl key.
            self.reply_to(message, message.text + " Done")  # Replying with a success message.

        @self.message_handler(commands=[self.Constants.SCREEN_SHOT.value])
        def SCREEN_SHOT(message):
            try:
                self.send_photo(message.chat.id, pyautogui.screenshot(), reply_to_message_id=message.id)  # Taking a screenshot and sending it.
                self.reply_to(message, message.text + " Done")  # Replying with a success message.
            except FileNotFoundError:
                self.reply_to(message, "Sorry, I couldn't take an image!")  # Replying with an error message if screenshot fails.

    # Method to start the bot with infinite polling.
    def run(self):
        self.infinity_polling()
 
# Class for creating a GUI application with a dark theme.
class DarkThemeApp:
    def __init__(self, root):
        self.path = os.path.abspath(os.path.dirname(__file__))+'/data.json'  # Path to the JSON file for storing data.
        self.error = os.path.abspath(os.path.dirname(__file__))+'/errorlogs.txt'  # Path to the error log file.
        self.root = root  # Reference to the Tkinter root window.
        self.root.title("Desktop Controller")  # Setting the window title.
        self.root.configure(bg="#2E2E2E")  # Setting the background color to dark.
        self.root.report_callback_exception = self.handle_exception  # Setting the custom exception handler.

        self.screen_width = self.root.winfo_screenwidth()  # Getting the screen width.
        self.screen_height = self.root.winfo_screenheight()  # Getting the screen height.
        
        self.set_window_center(300, 200)  # Centering the window on the screen.

        self.create_widgets()  # Creating the GUI widgets.
    
    # Custom exception handler to log errors to a file.
    def handle_exception(self,exception, value, the_traceback):
        with open(self.error,'a') as file:
            file.write(f"Exception:{repr(exception)}\n")  # Logging the exception.
            file.write(f"Exception:{exception.__class__.__name__}\n")  # Logging the exception class.
            file.write(f"Error message:{str(value)}\n")  # Logging the error message.

            file.write("Traceback (most recent call last)\n")
            if the_traceback is not None:
                traceback_entries = traceback.format_tb(the_traceback)  # Formatting the traceback.
                for entry in traceback_entries:
                    file.write(str(entry.strip())+'\n')  # Writing each traceback entry to the log.
            file.write("\n\n"+"#"*80+'\n\n')  # Adding a separator in the log file.

    # Method for centering the window on the screen.
    def set_window_center(self, width, height):
        # Get screen width and height
        x = (self.screen_width // 2) - (width // 2)  # Calculating the x-coordinate for centering.
        y = (self.screen_height // 2) - (height // 2)  # Calculating the y-coordinate for centering.
        # Set the geometry of the window
        self.root.geometry(f"{width}x{height}+{x}+{y}")  # Setting the window size and position.
        
    # Method for creating the GUI widgets.
    def create_widgets(self):
        # Create a label
        self.label = tk.Label(self.root, text="Enter Telegram Bot Token:", bg="#2E2E2E", fg="#FFFFFF")  # Creating a label with the prompt.
        self.label.pack(pady=10)  # Packing the label with padding.

        # Create an entry widget
        self.entry = tk.Entry(self.root, bg="#3E3E3E", fg="#FFFFFF", insertbackground="#FFFFFF", width=40)  # Creating an entry widget for token input.
        self.entry.pack(pady=5)  # Packing the entry widget with padding.

        # Create a button
        self.print_button = tk.Button(self.root, text="Start Control", command=self.print_input, bg="#555555", fg="#FFFFFF", width=20)  # Creating a button to start control.
        self.print_button.pack(pady=10)  # Packing the button with padding.

        self.load_button = tk.Button(self.root, text="Last Session", command=self.load_last, bg="#555555", fg="#FFFFFF", width=20)  # Creating a button to load the last session.
        self.load_button.pack(pady=10)  # Packing the button with padding.
    
    # Method for loading the last saved token and starting the bot.
    def load_last(self):
        with open(self.path, 'r') as file:
            data = json.load(file)  # Loading the JSON data from the file.

        # Function to run the bot with the last saved token.
        def last_run():
            try:
                global bot  # Using the global 'bot' variable.
                bot = DesktopController(data['token'], self.screen_width, self.screen_height)  # Creating a new instance of 'DesktopController'.
                bot.run()  # Running the bot.
            except Exception as e:
                messagebox.showerror("Error", f"There is no saved token!!")  # Showing an error dialog if the token is missing.

        # Create and start a new thread for the bot
        bot_thread = threading.Thread(target=last_run)  # Creating a new thread to run the bot.
        bot_thread.start()  # Starting the bot thread.

        # Optionally, you can destroy the root window here if you want to close the app
        self.root.destroy()  # Destroying the root window to close the app.

    # Method for starting the bot with the user-provided token.
    def print_input(self):
        # Get user input from the entry widget
        user_input = self.entry.get()  # Getting the user input from the entry widget.
        
        # Check if the input is not empty
        if not user_input:
            messagebox.showerror("Error", f"The token field is empty!")  # Showing an error dialog if the input is empty.
            return
        
        try:
            # Load existing data from the JSON file
            with open(self.path, 'r') as file:
                data = json.load(file)  # Loading the JSON data from the file.
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error" ,"Error loading the JSON file. Please check the file path and format.")  # Showing an error dialog if the file is not found or invalid.
            return
        
        # Update the 'token' in the loaded data
        data['token'] = user_input  # Updating the token in the JSON data.

        try:
            # Write the updated data back to the JSON file
            with open(self.path, 'w') as file:
                json.dump(data, file, indent=4)  # Saving the updated data back to the file.
        except Exception as e:
            messagebox.showerror("Error", f"Error file saving {e}")  # Showing an error dialog if there is an error saving the file.
            return

        # Function to run the bot in a separate thread
        def run_bot():
            try:
                global bot  # Using the global 'bot' variable.
                bot = DesktopController(user_input, self.screen_width, self.screen_height)  # Creating a new instance of 'DesktopController'.
                bot.run()  # Running the bot.
            except Exception as e:
                messagebox.showerror("Error", f"Thsi is AN Internal error please call support")  # Showing an error dialog for internal errors.
                return

        # Create and start a new thread for the bot
        bot_thread = threading.Thread(target=run_bot)  # Creating a new thread to run the bot.
        bot_thread.start()  # Starting the bot thread.

        # Optionally, you can destroy the root window here if you want to close the app
        self.root.destroy()  # Destroying the root window to close the app.


root = tk.Tk()  # Creating the root Tkinter window.
app = DarkThemeApp(root)  # Creating an instance of the 'DarkThemeApp' class.
root.mainloop()  # Running the Tkinter event loop.
