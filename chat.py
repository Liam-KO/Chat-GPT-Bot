from tkinter import *
import customtkinter
import openai
import os
import pickle

# Create instance of custom tkinter
# Initiate App
root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry('600x600')
root.iconbitmap('ai_lt.ico')
# Set color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Submit to ChatGPT
def speak():
    # Did we type anything to chat
    if chat_entry.get():
        # Define our filename
        filename = "api_key"
        
        try:
            if os.path.isfile("api_key"):
                # Open the file
                input_file = open(filename, 'rb')
                # Load the data from a file
                stuff = pickle.load(input_file)
                # Query ChatGPT
                openai.api_key = stuff

                # Create an instancwe
                openai.Model.list()

                #Define our Query / Response
                response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = chat_entry.get(),
                    temperature = 0,
                    max_tokens = 60,
                    top_p = 1.0,
                    frequency_penalty = 0.0,
                    presence_penalty = 0.0,
                )

                my_text.insert(END, response["choices"][0]["text"].strip())
                my_text.insert(END, "\n\n")

            else:
                # Create the file
                input_file = open(filename, 'wb')
                input_file.close()
                # Error message - you need an api key
                my_text.insert(END, "\n\n You need an API Key. Get one here: https://platform.openai.com/account/api-keys \n")

        except Exception as e:
            my_text.insert(END, f"\n\n There was an error \n\n{e}")
        
    else:
        my_text.insert(END, "\n\n Hey! You forgot to type anything")

# Clear the screens
def clear():
    # Clear the main text box
    my_text.delete(1.0, END) # 1.0 (first position in text box to the end of the box)
    # Clear the query entry box
    chat_entry.delete(0, END) #Entry box starts at 0 instead of 1.0 ..why?

    pass

# Do API Stuff
def key():
    # Define our filename
    filename = "api_key"
    
    try:
        if os.path.isfile("api_key"):
            # Open the file
            input_file = open(filename, 'rb')
            # Load the data from a file
            stuff = pickle.load(input_file)
            # Output stuff to our entry box
            api_entry.insert(END, stuff)
        else:
            # Create the file
            input_file = open(filename, 'wb')
            input_file.close()

    except Exception as e:
        my_text.insert(END, f"\n\n There was an error \n\n{e}")
    
     # Resize app
    root.geometry('600x750')
    # Reshow api frame
    api_frame.pack(pady=30)


# Save the API Key
def save_key():
    # Define filename
    filename = "api_key"

    # Open file
    output_file = open(filename, 'wb')
    # Add data to file
    pickle.dump(api_entry.get(), output_file)

    # Delete Entry Box
    api_entry.delete(0, END)
    
    # Hide api frame
    api_frame.pack_forget()
    # Resize app smaller
    root.geometry('600x600')
    pass

# Create Text Frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add text widget for ChatGPT responses
my_text = Text(text_frame,
               bg="#343638",
               width=65,
               border=1,
               fg="#d6d6d6",
               relief="flat",
               wrap=WORD,
               selectbackground="#1f538d")

my_text.grid(row=0, column=0)

# Create Scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
                                         command = my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

#Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry widget to type stuff to chatGPT
chat_entry = customtkinter.CTkEntry(root,
                                    placeholder_text = "Type something to chatGPT..",
                                    width =535,
                                    height=50,
                                    border_width=1)
chat_entry.pack(pady=10)
# chat_entry.grid(row=1,column=0)

# Button Frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424",border_width=1)
button_frame.pack(pady=10)

# Create Buttons
submit_button = customtkinter.CTkButton(button_frame, 
                                        text="Speak To ChatGPT",
                                        command=speak)
submit_button.grid(row=0, column=0, padx=25)

clear_button = customtkinter.CTkButton(button_frame, 
                                       text="Clear Response",
                                        command=clear)
clear_button.grid(row=0, column=1, padx=35)

api_button = customtkinter.CTkButton(button_frame, 
                                     text="Update API Key",
                                     command=key)
api_button.grid(row=0, column=2, padx=25)

# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
                                   placeholder_text = "Enter your API Key",
                                   width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame, text="Save Key",
                                          command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()



