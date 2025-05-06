import random
import re
from config import MODEL_PATH, DEFAULT_N_CTX, DEFAULT_N_THREADS
from llama_cpp import Llama


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
        self.n_ctx = n_ctx
        self.n_threads = n_threads

        self.llm = Llama(
            model_path=MailContentGenerator.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
        )

    def build_messages(self, idx: int | None = None) -> list[dict[str, str]]:
        """
        Builds a list of messages to be used as input for the language model.

        Args:
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

    def generate_email(self, user, link, idx: int | None = None) -> tuple[str, str]:
        """
        Generates a phishing email based on the specified user and link.

        Args:
            user (str): The recipient's email address or name to personalize the email.
            link (str): The link to include in the email.
            idx (int | None): The index of the scenario to use. If None, a random scenario is selected.

        Returns:
            tuple: A tuple containing the email subject and body.
        """

        messages = self.build_messages(idx)
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
        body = re.sub(r"\[LINK]", link, body_extracted, flags=re.IGNORECASE).strip()

        return subject, body


if __name__ == "__main__":
    generator = MailContentGenerator()
    subject, body = generator.generate_email('marek@example.com', 'www.example.com')
    print("\nGenerated Email\n" + "-" * 50)
    print(f'Subject: {subject}\n' + "-" * 50)
    print(f'Body: {body}')
