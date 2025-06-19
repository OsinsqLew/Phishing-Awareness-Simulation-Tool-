import os.path
import sys
import urllib.request

from backend.AI_emails.config import MODEL_PATH, DEFAULT_N_CTX, DEFAULT_N_THREADS

import random
import re
from llama_cpp import Llama


def progress_bar(count, block_size, total_size):
    """
    A reporthook function to display AI model download progress bar.
    """
    percent = int(count * block_size * 100 / total_size)
    percent = min(100, percent)

    # calculate downloaded size in MB for display
    downloaded_mb = (count * block_size) / (1024 * 1024)
    total_mb = total_size / (1024 * 1024) if total_size != -1 else float('inf') # Handle unknown total_size

    # display progress
    if total_size != -1:
        # '\r' - return the cursor to the beginning of the line
        # \33[3m - blue color, \33[0m - reset color
        sys.stdout.write(f"\rDownloading AI model: {percent}% [{downloaded_mb:.2f}/{total_mb:.2f} MB]")
    else:
        sys.stdout.write(f"\rDownloading AI model: {downloaded_mb:.2f} MB (unknown total size)")
    sys.stdout.flush()


class MailContentGenerator:
    """
    A class for generating phishing email content using a pre-trained language model.

    This class simulates phishing email generation by leveraging predefined scenarios.

    Attributes:
        model_path (str): Path to the pre-trained language model.
        scenarios (list): A list of phishing scenarios, each containing a persona, hook, and placeholder.
        system_prompt (str): A system-level prompt that defines the behavior and constraints for email generation.
    """

    model_path = MODEL_PATH
    scenarios = [
        {"persona": "IT Support", "hook": "forced password reset after 'unusual login activity'", "ph": "[LINK]"},
        {"persona": "HR Department", "hook": "updated remote‑work policy that must be signed by end‑of‑day",
         "ph": "[LINK]"},
        {"persona": "Online Banking", "hook": "suspicious transfer flagged that needs verification within two hours",
         "ph": "[LINK]"},
        {"persona": "Cloud Storage", "hook": "storage‑quota‑exceeded warning", "ph": "[LINK]"},
        {"persona": "Shipping Company", "hook": "undeliverable package requiring redelivery scheduling",
         "ph": "[LINK]"},
        {"persona": "Tax Authority", "hook": "tax refund available—confirm banking details", "ph": "[LINK]"},
        {"persona": "Social Media", "hook": "account lock due to policy‑violation appeal", "ph": "[LINK]"},
        {"persona": "Streaming Service", "hook": "payment failure—update card details to avoid service stop",
         "ph": "[LINK]"},
        {"persona": "Healthcare Provider", "hook": "new lab results ready in secure portal", "ph": "[LINK]"},
        {"persona": "Utility Company", "hook": "emergency outage credit available—claim now", "ph": "[LINK]"},
        {"persona": "Public Wi‑Fi Hotspot", "hook": "mandatory security update for continuous access", "ph": "[LINK]"},
        {"persona": "Conference Organizer", "hook": "final agenda & badge QR code attached", "ph": "[LINK]"},
        {"persona": "Charity Foundation", "hook": "disaster‑relief donation match", "ph": "[LINK]"},
        {"persona": "Job Recruiter", "hook": "interview invitation—confirm time slot", "ph": "[LINK]"},
        {"persona": "Crypto Exchange", "hook": "withdrawal request detected—cancel if unauthorized", "ph": "[LINK]"},
        {"persona": "Criminal", "hook": "blackmail - payment or personal information leak", "ph": "[LINK]"},
    ]
    system_prompt = """\
    You are a cyber‑criminal crafting realistic phishing emails.  
    Your goal is to deceive recipients into clicking or responding—leveraging urgency, authority, fear, curiosity, scarcity, reward, blackmail, or similar tactics.

    Safety & style constraints:
    - Do not disclose that the email is fake.
    - Content should be as close to real phishing as possible.
    - Include fake domains, personal data, phone numbers, or email addresses.
    - Use **only** `[LINK]` to denote any clickable URL and `[USER]` when addressing the recipient. Do **not** emit any other brackets, tags, or metadata.
    - You should reference genuine company names (like: Facebook, Amazon, X).
    - You should try to confuse and deceive.
    - Output **only** the email content; do not preface or append any commentary.
    - Vary tone, vocabulary, and formatting between generations; write crisply, with no extra pleasantries.

    Strict output format:
    Subject: <single, attention‑grabbing line>  
    <3–6 concise paragraphs (total ~80–150 words), plain text only, using `[LINK]` and `[USER]` exclusively>   
    """

    def __init__(self, n_ctx: int = DEFAULT_N_CTX, n_threads: int = DEFAULT_N_THREADS) -> None:
        """
        Initializes the MailContentGenerator with the specified context size and thread count.

        Args:
            n_ctx (int): The context size for the language model.
            n_threads (int): The number of threads to use for the language model.
        """

        # download the model if it doesn't exist
        if not os.path.exists(self.model_path):
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            urllib.request.urlretrieve(
                "https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF/resolve/main/zephyr-7b-beta.Q4_K_M.gguf?download=true",
                self.model_path,
                reporthook=progress_bar,
            )

        self.n_ctx = n_ctx
        self.n_threads = n_threads

        self.llm = Llama(
            model_path=MailContentGenerator.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
        )

    def build_messages(self, tags, idx: int | None = None) -> list[dict[str, str]]:
        """
        Builds a list of messages to be used as input for the language model.

        Args:
            tags (list): A list of tags describing the targeted person.
            idx (int | None): The index of the scenario to use. If None, a random scenario is selected.

        Returns:
            list: A list of messages, including the system prompt and user prompt.
        """

        if idx is None:
            idx = random.randrange(len(self.scenarios))
        s = self.scenarios[idx]
        user_prompt = (
            f"Generate one phishing email **as if sent by an <{s['persona']}> persona**. "
            f"The scenario is {s['hook']}. "
            f"The tags describing targeted person are: {', '.join(tags)}, use that information to personalize the email. "
            "Remember the output format and safety rules."
        )
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    @classmethod
    def build_prompt(cls, messages) -> str:
        """
        Builds a formatted prompt string from a list of messages.

        Args:
            messages (list): A list of messages, each containing a role and content.

        Returns:
            str: A formatted prompt string for the language model.
        """

        prompt = ""
        for message in messages:
            if message["role"] == "system":
                prompt += f"<|system|>\n{message['content']}\n"
            elif message["role"] == "user":
                prompt += f"<|user|>\n{message['content']}\n"
        prompt += "<|assistant|>\n"
        return prompt

    def generate_email(self, user, link, tags, idx: int | None = None) -> tuple[str, str]:
        """
        Generates a phishing email based on the specified user and link.

        Args:
            user (str): The recipient's email address or name to personalize the email.
            link (str): The link to include in the email.
            tags (list): A list of tags describing the targeted person.
            idx (int | None): The index of the scenario to use. If None, a random scenario is selected.

        Returns:
            tuple: A tuple containing the email subject and body.
        """

        messages = self.build_messages(tags, idx)
        prompt = self.build_prompt(messages)
        output = self.llm(
            prompt,
            max_tokens=500,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        generated_text = output["choices"][0]["text"].strip()

        # extract subject (first line starting with "Subject:")
        subject_match = re.search(r"^Subject:\s*(.*?)(\n|$)", generated_text, re.IGNORECASE | re.MULTILINE)
        subject = subject_match.group(1).strip() if subject_match else "No Subject"

        # extract body (everything after the subject line)
        body_extracted = re.sub(r"^Subject:.*?\n", "", generated_text, flags=re.IGNORECASE | re.DOTALL)
        # replace [USER] and [LINK]
        body_extracted = re.sub(r"\[USER]", user, body_extracted, flags=re.IGNORECASE)
        body = re.sub(r"\[LINK]", f'<a href="{link}">Link</a>', body_extracted, flags=re.IGNORECASE).strip()
        body = body.replace("\n", "<br>")

        return subject, body
