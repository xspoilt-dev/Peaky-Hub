import requests
import argparse
import re
from fake_useragent import UserAgent
from rich.progress import Progress
from rich.console import Console
from rich.panel import Panel
from rich import box
ua = UserAgent()
def value(full_text, first_text, last_text):
    pattern = f'{re.escape(first_text)}(.*?){re.escape(last_text)}'
    match = re.search(pattern, full_text)
    if match:
        return match.group(1)
    else:
        return None

def convert_code(input_code, input_lang, output_lang):
    headers = {
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.codeconvert.ai/free-converter',
        'Content-Type': 'application/json',
        'Origin': 'https://www.codeconvert.ai',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'Priority': 'u=1'
    }

    json_data = {
        'inputCodeText': input_code,
        'inputLang': input_lang,
        'outputLang': output_lang,
        'customInstruction': '',
    }

    response = requests.post('https://www.codeconvert.ai/api/free-convert', headers=headers, json=json_data).json()
    try:
        return response['outputCodeText']
    except:
        return "print(\"Too many lines\")"

def encrypted(content):
    encrypted_code_pattern = r'[^\w\s]'
    matches = re.findall(encrypted_code_pattern, content)
    if len(matches) / len(content) > 0.5:
        return True
    else:
        return False
def marshal_to_byte(content):
    marshal_data = value(content, "exec(marshal.loads(", "))")
    data = f"""
import marshal
import dis
dis.dis(marshal.loads({marshal_data}))
"""
    return data

def main():
    parser = argparse.ArgumentParser(description='Code Converter')
    parser.add_argument('-dis', type=str, help='Input file containing code to be converted')
    parser.add_argument('-o', type=str, help='Output file to save the converted code')
    parser.add_argument('-marshal', type=str, help='Input file containing code to be marshaled')
    args = parser.parse_args()

    console = Console()
    console.print(Panel("Coded by: @x_spoilt", title="Info", box=box.ROUNDED, border_style="magenta"))

    if args.dis:
        with open(args.dis, 'r') as file:
            input_code = file.read()

        with Progress() as progress:
            task = progress.add_task("[cyan]Converting code...", total=100)
            for _ in range(100):
                progress.update(task, advance=1)

            output_code = convert_code(input_code, 'JavaScript', 'Python')

        console.print(Panel(output_code, title="Converted Code", box=box.ROUNDED, border_style="green"))

        if args.o:
            with open(args.o, 'w') as file:
                file.write(output_code)
            console.print(Panel(f"Code saved to {args.o}", title="Success", box=box.ROUNDED, border_style="blue"))

    if args.marshal:
        with open(args.marshal, 'r') as file:
            content = file.read()
        output_code = marshal_to_byte(content)
        console.print(Panel(output_code, title="Marshaled Code", box=box.ROUNDED, border_style="green"))

        if args.o:
            with open(args.o, 'w') as file:
                file.write(output_code)
            console.print(Panel(f"Code saved to {args.o}", title="Success", box=box.ROUNDED, border_style="blue"))

if __name__ == "__main__":
    main()
