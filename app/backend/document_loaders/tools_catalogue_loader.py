# This code is moved from a jupyter notebook
# For now, execute the script just once to create github_documents.pkl

import os
import re
import pickle
from collections import defaultdict
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader

# Define absolute paths
BON_AI_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_PATH = os.path.join(BON_AI_ROOT, "app/backend/data/tools_docs.pkl")

def tool_catalogue_extractor(html):
    """Extracts tool details from HTML content."""
    match = re.search(r'<!-- Tool Detail -->(.*?)<!-- Related Tools -->', html, re.DOTALL)
    if not match:
        return "Content not found between the specified markers."
    
    soup = BeautifulSoup(match.group(1).strip(), 'html.parser')
    result = []

    def extract_text(class_name, label):
        tag = soup.find(class_=class_name)
        if tag:
            result.append(f"{label}: {tag.get_text(strip=True)}")

    extract_text("tool-detail-name", "Tool Name")
    extract_text("tool-detail-company", "Tool Company")

    last_update = soup.find(string=re.compile(r"Last Update:", re.IGNORECASE))
    if last_update:
        update_text = last_update.find_next(string=True).strip()
        result.append(f"Last Update: {update_text}")

    link = soup.find('a', href=True)
    if link:
        link_text, link_url = link.get_text(strip=True), link['href']
        result.append(f"[{link_text}]({link_url})" if link_text != link_url else link_url)

    badges = defaultdict(list)
    for badge in soup.find_all(class_=lambda c: c and c.startswith("badge-tool-")):
        category = next((cls.replace("badge-tool-", "") for cls in badge["class"] if cls.startswith("badge-tool-")), None)
        if category:
            badges[category].append(badge.get_text(strip=True))

    if badges:
        result.append("Tool Badges:")
        for category, items in badges.items():
            result.append(f"{category}:")
            result.extend(items)

    description_section = soup.find(id="description")
    if description_section:
        result.append("\nTool Description:\n" + description_section.get_text(strip=True, separator=" "))

    additional_info_section = soup.find(id="additional-information")
    if additional_info_section:
        additional_info = [
            f"{row.find_all(['th', 'td'])[0].get_text(strip=True).rstrip(':')}: {row.find_all(['th', 'td'])[1].get_text(strip=True)}"
            for row in additional_info_section.find_all("tr") if len(row.find_all(["th", "td"])) == 2
        ]
        result.append("\nAdditional Information:")
        result.extend(additional_info)

    return "\n".join(result)


def create_tools_metadata(docs):
    """Extracts metadata from tools_documents."""
    for doc in docs:
        content = doc.page_content
        metadata = {
            "source": doc.metadata.get("source"),
            "language": doc.metadata.get("language"),
            "source_type": "BON in a Box Tools"
        }
        
        patterns = {
            "tool_title": r"Tool Name:\s*(.+)",
            "tool_company": r"Tool Company:\s*(.+)",
            "last_update": r"Last Update:\s*(\d{4})",
            "contact_person": r"Contact person:\s*(.+)",
            "contact_email": r"Contact e-mail:\s*\[(.*?)\]",
            "contact_organization": r"Contact Organization:\s*(.+)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                metadata[key] = match.group(1).strip()
        
        if "last_update" in metadata:
            metadata["last_update"] = int(metadata["last_update"])

        badges_section = re.search(r"Tool Badges:(.*?)Tool Description:", content, re.DOTALL)
        if badges_section:
            badges = re.findall(r"\n(\S.*)", badges_section.group(1))
            if badges:
                metadata["tool_badges"] = [badge.strip() for badge in badges if ":" not in badge]

        doc.metadata = metadata


def load_tools():
    """Fetches tools from URLs, extracts metadata, and saves them as a pickle file."""
    tools_documents = []
    for i in range(243):
        loader = RecursiveUrlLoader(
            f"https://boninabox.geobon.org/tool-detail?id={i+1}",
            max_depth=1,
            extractor=tool_catalogue_extractor
        )
        tools_documents.extend(loader.load())

    tools_documents = [doc for doc in tools_documents if doc.page_content != 'Content not found between the specified markers.']
    print("Number of tools:", len(tools_documents))

    create_tools_metadata(tools_documents)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "wb") as file:
        pickle.dump(tools_documents, file)

    print(f"Saved tools data to {DATA_PATH}")


if __name__ == "__main__":
    load_tools()
