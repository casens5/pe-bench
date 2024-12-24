import os
import re
from argparse import ArgumentParser

# make a function which returns the extension of the language files for each language
def get_extension(language):
    if language == 'c': return 'c'
    elif language == 'r': return 'r'
    elif language == 'go': return 'go'
    elif language == 'c++': return 'cpp'
    elif language == 'lua': return 'lua'
    elif language == 'java': return 'java'
    elif language == 'lisp': return 'lisp'
    elif language == 'rust': return 'rs'
    elif language == 'ruby': return 'rb'
    elif language == 'perl': return 'pl'
    elif language == 'python': return 'py'
    elif language == 'prolog': return 'pl'
    elif language == 'matlab': return 'matlab'
    elif language == 'kotlin': return 'kt'
    elif language == 'fortran': return 'f'
    elif language == 'javascript': return 'js'
    else:
        raise Exception(f"Unsupported language: {language}")

def extract_code_block(markdown_content, language, extension):
    # Regular expression to find code blocks between triple backticks
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)

    # Find all code blocks in the markdown content
    code_blocks = code_block_pattern.findall(markdown_content)

    # we only need the first block
    code_block = code_blocks[0] if len(code_blocks) > 0 else ""

    # remove first line from code block if it contains only one word, the name of the language
    if code_block == extension or code_block == language:
        # just get a substring starting from the first newline
        code_block = code_block[code_block.find('\n') + 1:]

    # in case that code_blocks is empty we considert that the whole content is code
    if len(code_block) == 0:
        code_block = markdown_content

    return code_block

def process_markdown_files(model_name, language):
    language_dir = os.path.join('solutions', model_name, language)

    if not os.path.exists(language_dir):
        raise Exception(f"Response directory {language_dir} does not exist.")

    markdown_files = sorted(os.listdir(language_dir))

    for markdown_file in markdown_files:
        if markdown_file.endswith('.md'):
            markdown_path = os.path.join(language_dir, markdown_file)

            with open(markdown_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()

            extension = get_extension(language)
            code_block = extract_code_block(markdown_content, language, extension)

            # Extract the problem number from the filename
            problem_number = os.path.splitext(markdown_file)[0]
            language_dir_file_path = os.path.join(language_dir, f"{problem_number}.{extension}")

            with open(language_dir_file_path, 'w', encoding='utf-8') as language_file:
                language_file.write(code_block)

            print(f"Processed {markdown_file} and saved code to {language_dir_file_path}")

def main():
    parser = ArgumentParser(description="Extract code blocks from Markdown files.")
    parser.add_argument('--model_name', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python', help='Name of the language to use, default is python')

    args = parser.parse_args()
    model_name = args.model_name
    language = args.language
    process_markdown_files(model_name, language)

if __name__ == "__main__":
    main()