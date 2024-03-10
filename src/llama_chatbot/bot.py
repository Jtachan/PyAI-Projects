"""Bot"""
import os
from typing import Optional

import dotenv
import replicate


class ChatBot:
    def __init__(self, api_token: Optional[str] = None):
        """
        Initializes the chatbot.

        Parameters
        ----------
        api_token : str
            Provided API token or key by Replicate. If not provided, the token is
            searched as an environment variable with the name 'REPLICATE_TOKEN' or
            'API_TOKEN'.
            Users can generate it at: https://replicate.com/account
        """
        if api_token is None:
            if os.path.exists(".env"):
                dotenv.load_dotenv(".env")
            api_token = os.getenv("API_TOKEN", os.getenv("REPLICATE_TOKEN"))

        if api_token is None:
            raise ValueError(
                "The bot needs of a Replicate token to work. Please, provide it"
                " manually or as an environment variable under the name 'API_TOKEN'"
                " or 'REPLICATE_TOKEN'."
            )

        self._model = "meta/llama-2-70b-chat"
        self._client = replicate.Client(api_token=api_token)

        system_prompt = (
            "You are a helpful, ans witty assistant, always answering with a joke. "
            "Your answers should not include any harmful, unethical, racist, sexist, "
            "toxic, dangerous, or illegal content."
        )
        self._params = {
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": "",
            "temperature": 0.5,
            "system_prompt": system_prompt,
            "max_new_tokens": 500,
            "min_new_tokens": -1,
        }

    def get_response(self, prompt: str):
        self._params["prompt"] = prompt
        response = self._client.run(
            self._model,
            input={"prompt": prompt, "system_prompt": self._params["system_prompt"]},
        )
        return "".join(response)

    @staticmethod
    def fit_length_response(response: str, limit_nof_characters: int = 88) -> str:
        nof_inline_chars = 0
        fit_response = ""
        for word in response.split(" "):
            fit_response += word
            nof_inline_chars += len(word)
            if nof_inline_chars >= limit_nof_characters:
                fit_response += "\n"
                nof_inline_chars = 0
            else:
                fit_response += " "
        return fit_response

    @property
    def models(self):
        return self._client.models.list()

    def run_on_terminal(self):
        while True:
            user_msg = input("\nHow may I assist you? Write 'exit' to close.\n")
            if user_msg == "exit":
                break

            response = self.get_response(user_msg)
            print()
            print(self.fit_length_response(response))
            print("-" * 60)


if __name__ == "__main__":
    bot = ChatBot()
    bot.run_on_terminal()
