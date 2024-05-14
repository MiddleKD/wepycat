import argparse
import anthropic
from dotenv import load_dotenv
from crawler import load_driver, kill_driver, crawl_website
from utils import save_html

def parse_argument():
    parser = argparse.ArgumentParser(description="Copy webpage source from webwave")
    parser.add_argument("--url", type=str, help="reference url")
    parser.add_argument("--max_input_letter", type=int, help="maximum text length to claude", default=30000)
    parser.add_argument("--output_max_token", type=int, help="maximum token claude answer", default=250)

    return parser.parse_args()

def query_to_claude(
        system_prompt, 
        message_contexts,
        max_tokens=1000,
        temperature=0,
        model_name="claude-3-sonnet-20240229",
):  
    message = client.messages.create(
        model=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=message_contexts
    )  
    return message
    
system_prompt = """You are a website designer. Please provide an analysis of the provided HTML code for a website. 
Discuss the color palette used and the potential meaning or mood conveyed by those color choices. 
Examine the page layout structure and how content is arranged across sections. 
Comment on the readability and visual appeal of the typography and font choices used for headings, body text, etc. 
Identify the overall design style and highlight specific design elements that establish that aesthetic. 
Based on the design decisions, explain the apparent purpose of the website and how well it aligns with the intended target audience.
Use plain, easy-to-understand language instead of technical jargon.
Do not include any actual code snippets in your response. **Don't go over 1000 letters. Get straight to the point.** This is very important to me."""

if __name__ == "__main__":
    args = parse_argument()
    load_dotenv()
    client = anthropic.Anthropic()

    load_driver()
    html_content = crawl_website(args.url)[:args.max_input_letter]
    kill_driver()

    message = query_to_claude(
        system_prompt,
        message_contexts=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": html_content
                    }
                ],
            }
        ],
        max_tokens=args.output_max_token)

    prompt = message.content[0].text
    print(f"html prompt: {prompt}\ntext length: {len(prompt)}")

    save_html(prompt, save_path="./reference_html_prompt.txt")
