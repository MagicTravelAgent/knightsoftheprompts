# import libraries
"""Example usage of the 'llm' module to create a personalized chatbot."""

from llm import get_chat_completion, Message
from loguru import logger
from bs4 import BeautifulSoup


class Chatbot:
    messages = []
    chat_history = []

    def __init__(self, model="gpt-35-turbo-16k", max_tokens=1024):
        self.model = model
        self.max_tokens = max_tokens
        self.start_chat()

    def extract_tags_and_content(self, html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        
        tags_content_dict = {}
        for tag in soup.find_all(True):
            tags_content_dict[tag.name] = tag.text
        print(tags_content_dict)
        return tags_content_dict

    def start_chat(self):
        self.messages.append(
            Message(
                role="system",
                content=f"You are a chatbot helping chefs."
                    f"Your role is as a sous-chef, helping to make recommendations based on samples."
                    f"When responding to the user, put your message including any recipes between the html tags <message> your message, food recipe </message>."
                    f"Include any cooking instructions between the message html tags. Example: <message> your message, food recipe cooking instructions</message>."
                    f"You remain in character at all times, not breaking immersion."
                    f"Your goal is to help the user find a recipe they will enjoy."
                    f"Your responses should be helpful and informative."
                    f"You should be knowledgeable about different types of food and cooking techniques."
                    f"You should be able to provide advice about recipes and cooking techniques."
                    f"You should be able to recommend recipes based on the user's preferences and dietary restrictions."
                    f"You should be able to provide information about the ingredients and cooking instructions for a recipe."
                    f"In the case a user does not like a sample, you should recommend a recipe without that ingredient."
                    f"The text of your messages to the chef you are helping must be captured between the html tags <message> your message </message>."
                    f"If you recommend a recipe before you answer you must put the following information between html tags: <sample>sample name</sample>, <enjoyment>enjoyment level</enjoyment>, <sentiment>sentiment of the enjoyment level</sentiment>, <score>score from 0 to 10 of the enjoyment level</score>, <recommended_recipe>recommended recipe</recommended_recipe>."
                    f"Make sure if you recommend a recipe to include the sample name between the html tags <sample>sample name</sample>"
                    f"initiate the conversation like this: <message>Hello, I am your sous-chef. What did you think of your truffle mayonaise sample?</message>."
                    f"An example conversation is provided below:"
                    f"After reading the example below, start the conversation."
            )
        )
        self.messages.append(
            Message(
                role="assistant",
                content="<message>Hello, I am your sous-chef. What did you think of your truffle mayonaise sample?</message>")
        )
        self.messages.append(
            Message(
                role="user",
                content="<message>I thought it was delicious!</message>"
            )
        )
        
        self.messages.append(
            Message(
                role="assistant",
                content="<sample>truffle mayonaise</sample><enjoyment>delicious</enjoyment><sentiment>positive</sentiment><score>9</score><recommended_recipe>truffle aioli burger</recommended_recipe><message>Great! I'm glad you enjoyed it. Would you like a recipe truffle aioli burgers based on this sample?</message>")
        )

        self.messages.append(
            Message(
                role="user",
                content="<message>Yes please!</message>"
            )
        )
        
        self.messages.append(
            Message(
                role="assistant",
                content="""<message>Ingredients:
- 1 lb ground beef
- 1/4 cup breadcrumbs
- 1/4 cup grated Parmesan cheese
- 1/4 cup chopped fresh parsley
- Salt and pepper to taste
- 4 hamburger buns
- Truffle mayonnaise (to taste)
- Lettuce, tomato, and any other desired burger toppings

Instructions:
1. In a large mixing bowl, combine the ground beef, breadcrumbs, grated Parmesan cheese, chopped parsley, salt, and pepper. Mix well until all the ingredients are evenly incorporated.
2. Divide the mixture into four equal portions. Shape each portion into a patty, making sure they are about the same size as the hamburger buns.
3. Preheat your grill or stovetop skillet to medium-high heat. Cook the burger patties for about 4-5 minutes per side, or until they reach your desired level of doneness.
4. While the burgers are cooking, lightly toast the hamburger buns on the grill or in a toaster.
5. Assemble the burgers by spreading a generous amount of truffle mayonnaise on both halves of each toasted bun.
6. Place a cooked burger patty on the bottom half of each bun. Add lettuce, tomato slices, and any other desired burger toppings.        
7. Top with the other half of the bun and enjoy your delicious Truffle Aioli Burgers!

Feel free to customize your burgers with additional toppings or seasonings to suit your taste. Let me know if you need any further assistance or if there is anything else I can help you with!</message>""")
        )
        self.messages.append(
            Message(
                role="system",
                content="Now begin your interaction with the user based on the example conversation provided."
            )
        )

        completion = get_chat_completion(
            self.messages, model=self.model, max_tokens=self.max_tokens
        )

        tags = self.extract_tags_and_content(completion.choices[0].message.content)
        self.chat_history.append(tags["message"])

    def get_messages(self):
        return self.chat_history

    def chat(self, input_text):
        
        self.messages.append(Message(role="user", content="<message>"+input_text+"</message>"))

        # main loop: get answer from model, ask user for reply, repeat.
        completion = get_chat_completion(
            self.messages, model=self.model, max_tokens=self.max_tokens
        )
        logger.info("\n" + completion.choices[0].message.content)

        self.messages.append(
            Message(
                role=completion.choices[0].message.role,
                content=completion.choices[0].message.content,
            )
        )
        self.chat_history.append(input_text)
        tags = self.extract_tags_and_content(completion.choices[0].message.content)
        self.chat_history.append(tags["message"])

        return self.chat_history, tags

        # open question: how can you make sure the model doesn't run out of context
        # when the chat history grows, with the `messages` object having too much info?

# chatbot = Chatbot()
# chatbot.start_chat()
