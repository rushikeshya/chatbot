from tkinter import *
import speech_recognition as sr
import requests
import json
import openai
openai.api_key = "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"

# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Send function
def send():
    send = "You -> " + e.get()
    txt.insert(END, "\n" + send)
    user_input(e.get().lower())

def user_input(user):
    if (user == "hello"):
        txt.insert(END, "\n" + "Bot -> Hi there, how can I help?")
    elif (user == "hi" or user == "hii" or user == "hiiii"):
        txt.insert(END, "\n" + "Bot -> Hi there, what can I do for you?")
    elif (user == "how are you"):
        txt.insert(END, "\n" + "Bot -> Fine! And you?")
    elif (user == "fine" or user == "i am good" or user == "i am doing good"):
        txt.insert(END, "\n" + "Bot -> Great! How can I help you?")
    elif (user == "thanks" or user == "thank you" or user == "now its my time"):
        txt.insert(END, "\n" + "Bot -> My pleasure!")
    elif (user == "what do you sell" or user == "what kinds of items are there" or user == "have you something"):
        txt.insert(END, "\n" + "Bot -> We have coffee and tea.")
    elif (user == "tell me a joke" or user == "tell me something funny" or user == "crack a funny line"):
        txt.insert(END, "\n" + "Bot -> What did the buffalo say when his son left for college? Bison!")
    elif (user == "goodbye" or user == "see you later" or user == "see yaa"):
        txt.insert(END, "\n" + "Bot -> Have a nice day!")
    else:
        # Call API for more information
        response = get_additional_info(user)
        if response:
            txt.insert(END, "\n" + f"Bot -> {response}")
        else:
            txt.insert(END, "\n" + "Bot -> Sorry! I didn't understand that.")
    e.delete(0, END)

def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        user_input(r.recognize_google(audio).lower())
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
    except sr.RequestError:
        print("Sorry, my speech service is not available.")

def get_additional_info(query):
    try:
        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            engine="davinci-codex",  # Choose the appropriate language model
            prompt=query,
            max_tokens=100,  # Adjust the number of tokens based on your desired response length
            n=1,  # Specify the number of completions to generate
            stop=None,  # Specify a custom stop sequence if needed
        )
        # Extract the generated response from the API's output
        generated_text = response.choices[0].text.strip()

        return generated_text
    except openai.OpenAIError as e:
        print("OpenAI API error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

label1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

voice_button = Button(root, text="Voice Input", font=FONT_BOLD, bg=BG_GRAY, command=voice_input).grid(row=3, column=0, columnspan=2)

root.mainloop()
