import tkinter as tk
from own_helper import Chatbot
from tkinter import ttk

chat = Chatbot()

root = tk.Tk()
root.title("Text Processing")
root.geometry("1000x900")

# Creating a Treeview widget for the table
table = ttk.Treeview(root, columns=("Sample", "Enjoyment", "Sentiment", "Score", "Recommended Recipe"), show="headings")
table.heading("Sample", text="Sample")
table.heading("Enjoyment", text="Enjoyment")
table.heading("Sentiment", text="Sentiment")
table.heading("Score", text="Score")
table.heading("Recommended Recipe", text="Recommended Recipe")

# Function to update the table with new data
def update_table(tags):
    if len(tags) == 6:
        # table.delete(*table.get_children())  # Clear existing data        
        sample = tags["sample"]
        enjoyment = tags["enjoyment"]
        sentiment = tags["sentiment"]
        score = tags["score"]
        recommended_recipe = tags["recommended_recipe"]
        table.insert("", "end", values=(sample, enjoyment, sentiment, score, recommended_recipe))

output_text_box = tk.Text(root, height=30, width=60)
output_text_box.pack()
output_text_box.insert("end", "SousBot: "+ chat.get_messages()[0] + "\n")
output_text_box.config(state="disabled")

input_text_box = tk.Text(root, height=2, width=60)

def on_enter(event):
    process_text()

input_text_box.bind("<Return>", on_enter)
input_text_box.pack()

def process_text():
    input_text = input_text_box.get("1.0", "end-1c")
    print(input_text)
    output_messages, tags = chat.chat(input_text)
    
    output_text_box.config(state="normal")
    output_text_box.delete("1.0", "end")
    
    for i, message in enumerate(output_messages):
        if i % 2 == 1:
            output_text_box.insert("end", "\nUser: " + message + "\n")
        else:
            output_text_box.insert("end", "\nSousBot: " + message + "\n")
    
    output_text_box.config(state="disabled")
    input_text_box.delete("1.0", "end")  # Clear the content of the input box
    
    update_table(tags)  # Update the table with new data

button = tk.Button(root, text="Process", command=process_text)  # Added line
button.pack()  # Added line
# Adding sample data to the table

table.pack(side="right", padx=10, pady=10)

root.mainloop()