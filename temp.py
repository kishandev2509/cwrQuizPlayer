
# def parse_questions_from_html(html_content):
#     """
#     Parses the HTML content to extract question data.
#     Args:
#         html_content (str): The HTML content of the page.
#     Returns:
#         list: A list of dictionaries, where each dictionary represents a question.
#               This structure will need to be refined based on the actual HTML structure.
#     """
#     if not html_content:
#         print("No HTML content provided for parsing.")
#         return []

#     soup = BeautifulSoup(html_content, "html.parser")
#     extracted_questions = []

#     # --- IMPORTANT: THIS IS A PLACEHOLDER. YOU MUST INSPECT THE ACTUAL HTML ---
#     # Find all elements that contain individual questions.
#     # Common patterns for coding challenges: div with specific classes like
#     # 'challenge-item', 'question-card', 'problem-statement', etc.
#     question_elements = soup.find_all(
#         "div", class_=["challenge-item", "question-card", "problem-container"]
#     )

#     if not question_elements:
#         print(
#             "No question elements found with the current CSS selectors. Please inspect HTML."
#         )
#         # As a fallback, try to find common heading structures that might indicate questions
#         for h_tag in soup.find_all(["h2", "h3", "h4"]):
#             if (
#                 "question" in h_tag.get_text(strip=True).lower()
#                 or "problem" in h_tag.get_text(strip=True).lower()
#             ):
#                 extracted_questions.append(
#                     {
#                         "title_fallback": h_tag.get_text(strip=True),
#                         "html_snippet": str(h_tag),
#                     }
#                 )
#         if extracted_questions:
#             print("Found some questions using a fallback (h2/h3/h4 tags).")
#         return extracted_questions

#     for q_element in question_elements:
#         question_data = {}
#         # Example extraction: Adjust based on actual HTML structure
#         # Look for question title
#         title_tag = (
#             q_element.find("h2")
#             or q_element.find("h3")
#             or q_element.find("h4")
#             or q_element.find("div", class_="question-title")
#             or q_element.find("p", class_="question-title")
#         )
#         if title_tag:
#             question_data["title"] = title_tag.get_text(strip=True)

#         # Look for question description/problem statement
#         description_tag = (
#             q_element.find("div", class_="question-description")
#             or q_element.find("p", class_="problem-statement")
#             or q_element.find("div", class_="description")
#         )
#         if description_tag:
#             question_data["description"] = description_tag.get_text(strip=True)

#         # Look for options (if multiple choice) or input/output examples
#         options_list = []
#         for option_tag in q_element.find_all(
#             "li", class_="option-item"
#         ) or q_element.find_all("div", class_="radio-option"):
#             options_list.append(option_tag.get_text(strip=True))
#         if options_list:
#             question_data["options"] = options_list

#         # You might also need to extract input/output formats, constraints, code snippets etc.
#         # Add more specific finds based on your site's structure
#         code_block = q_element.find("pre")  # Example for code blocks
#         if code_block:
#             question_data["code_example"] = code_block.get_text(strip=True)

#         extracted_questions.append(question_data)

#     print(f"Parsed {len(extracted_questions)} questions from HTML.")
#     return extracted_questions