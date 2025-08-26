import cohere
import pdfkit
import markdown
import config
import os
import sys

# Get the absolute path of the script's directory
# This will correctly resolve to "C:\Users\somna\PYTHON\PROJECT\"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, 'pdf_templates')

# Initialize Cohere client with API key from config.py
co = cohere.Client(config.COHERE_API_KEY)

def generate_ebook(topic, chapters):
    """
    Generates eBook content in Markdown format using the Cohere API.
    """
    prompt = f"Write an eBook about {topic} with {chapters} chapters. Each chapter should have a title and content. Format the output in Markdown."

    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=10000,  # Adjust the output as necessary based on expected length
        temperature=1,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE'
    )

    return str(response.generations[0].text).strip()

def save_markdown(content, filename):
    """
    Saves the generated Markdown content to a file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def markdown_to_html(markdown_content):
    """
    Converts Markdown content to HTML.
    """
    html_content = markdown.markdown(markdown_content)
    return html_content

def embed_html_template(html_content, template_filename):
    """
    Reads an HTML template file and embeds the generated HTML content into it.
    """
    # Read the selected template HTML file from the templates folder
    template_path = os.path.join(TEMPLATES_DIR, template_filename)
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_filename}' not found in '{TEMPLATES_DIR}'.")
        sys.exit(1)

    # Replace the placeholder with actual HTML content
    styled_html_content = template.replace('{{MARKDOWN_CONTENT}}', html_content)
    return styled_html_content

def convert_html_to_pdf(html_content, pdf_filename):
    """
    Converts HTML content to a PDF file using wkhtmltopdf.
    Includes error handling for wkhtmltopdf not being found.
    """
    try:
        # Configure wkhtmltopdf path based on OS
        if sys.platform == "win32":
            # IMPORTANT: This path must point to the actual wkhtmltopdf.exe executable.
            # After installing wkhtmltopdf (from the .exe you downloaded), it's typically
            # found in "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe".
            # If you installed it elsewhere, please update this path accordingly.
            wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            # If you installed it directly into your project folder and the executable is there:
            # wkhtmltopdf_path = os.path.join(SCRIPT_DIR, 'wkhtmltopdf.exe')
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            # Default path for Linux/macOS installations (e.g., via Homebrew or apt)
            config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

        # Convert HTML to PDF using pdfkit with configuration
        pdfkit.from_string(html_content, pdf_filename, configuration=config, options={"encoding": "UTF-8"})
    except OSError as e:
        print("\n" + "="*70)
        print("Error: wkhtmltopdf is not installed or not found at the configured path.")
        print("Please ensure wkhtmltopdf is correctly installed and its executable path is set:")
        if sys.platform == "win32":
            print(f"  For Windows, verify that '{wkhtmltopdf_path}' points to wkhtmltopdf.exe.")
            print("  If you installed it to the default location, it should be correct.")
            print("  If you installed it elsewhere, update the 'wkhtmltopdf_path' variable in the script.")
        else:
            print("  For Linux/macOS, ensure it's in /usr/local/bin/wkhtmltopdf or update the script.")
        print("You can download wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html")
        print("="*70 + "\n")
        sys.exit(1)

# Entry point of the script
if __name__ == '__main__':
    topic = input("Enter the eBook topic: ")
    chapters = int(input("Enter the number of chapters: "))

    print("Available templates:")
    print("1. Classic")
    print("2. Modern")
    print("3. Minimalist")
    print("4. Elegant")
    print("5. Dark")

    template_choice = int(input("Choose a template (1-5): "))

    template_files = {
        1: 'classic.html',
        2: 'modern.html',
        3: 'minimalist.html',
        4: 'elegant.html',
        5: 'dark.html'
    }

    template_filename = template_files.get(template_choice, 'classic.html') # Default to classic if choice is invalid

    print("Generating eBook content...")
    ebook_content = generate_ebook(topic, chapters)

    # Sanitize topic for filenames
    markdown_filename = topic.replace(" ", "-").replace("/", "-").replace("\\", "-") + ".md"
    pdf_filename = topic.replace(" ", "-").replace("/", "-").replace("\\", "-") + ".pdf"

    print(f"Saving eBook as Markdown ({markdown_filename})...")
    save_markdown(ebook_content, markdown_filename)

    print(f"Converting Markdown to HTML...")
    html_content = markdown_to_html(ebook_content)

    print(f"Embedding HTML content into HTML template ({template_filename})...")
    html_template_content = embed_html_template(html_content, template_filename)

    print(f"Converting HTML to PDF ({pdf_filename})...")
    convert_html_to_pdf(html_template_content, pdf_filename)

    print(f"eBook '{pdf_filename}' generation complete!")
