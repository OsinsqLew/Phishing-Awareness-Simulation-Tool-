import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Model configuration
# model_name = "deepseek-ai/deepseek-llm-7b-base"
model_name = "HuggingFaceH4/zephyr-7b-beta"
cache_path = "./models"  # Specify where to store the model

# Load model and tokenizer from local cache or download if missing
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_path)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto", cache_dir=cache_path)

# Initialize the text generation pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

# Define chat-style message to generate an email
messages = [
    {
        "role": "system",
        "content": (
            "You are an expert in crafting persuasive email messages designed to trick users into taking action, "
            "such as clicking on a link, opening an attachment, or submitting their credentials. Your goal is to "
            "create realistic and deceptive phishing emails that mimic common attack strategies. Use social engineering techniques "
            "like urgency, authority, fear, or curiosity. Never use real URLs — instead, insert placeholders like [LINK], [ATTACHMENT], or [LOGIN PAGE]."
        )
    },
    {
        "role": "user",
        "content": (
            "Write a phishing email using one of the following personas: IT support, HR department, online banking service, or cloud storage provider. "
            "Include a subject line, vary the language and tone, and add a call to action with a placeholder."
        )
    }
]


# Format prompt using chat template
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# Generate the response
outputs = pipe(
    prompt,
    max_new_tokens=300,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.95
)

# Extract and clean assistant response
response_text = outputs[0]["generated_text"]
email_body = response_text.split("### Assistant:")[-1].strip()

# Output the email message
print("\nGenerated Email:\n")
print(email_body)

print("test")
