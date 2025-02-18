# README: Wikipedia Fact Annotation for InfoGap Pipeline Evaluation

## Introduction
This annotation task aims to evaluate knowledge gaps in Wikipedia across different languages. You will annotate facts based on their presence in Wikipedia articles using a **terminal-based annotation tool**.

Your contributions will help assess how well factual information is transferred across languages in Wikipedia.

---

## Setup Instructions
### Prerequisites
Ensure that you have the following installed:
- **Python >= 3.7+**
- **pip** (Python package manager)

### Install Required Packages
Before running the annotation tool, install the necessary dependencies:
```bash
pip install polars==0.19.6 loguru tqdm
```

---

## Annotation Instructions
### Task Overview
- You will be verifying whether a given **fact in one language (English or Korean)** is present in a **Wikipedia article in the other language**.
- The tool presents a **fact** and **Wikipedia snippets** in another language.
- You will select an appropriate **annotation category (A, B, C, D, or E)**.

### Annotation Categories
Choose the best option based on the presence of the fact:

| Option | Condition |
|------------|--------------|
| **A** | The fact is **fully conveyed** by the given snippets. |
| **B** | The fact is **mostly conveyed** by the given snippets. |
| **C** | The fact is **fully present** in the Wikipedia article (after manual verification). |
| **D** | The fact is **mostly (but not fully) present** in the Wikipedia article. |
| **E** | The fact is **not present** in the Wikipedia article. |

**Notes:**
- If the fact is **not sufficiently conveyed** by the provided snippets (**A or B do not apply**), **check the full Wikipedia article manually**.
- Use your **best judgment** to determine whether a fact is "mostly" present.

---

## Running the Annotation Script
### Navigate to the Annotation Folder
Extract the provided annotation package and navigate to the directory:
```bash
cd /path/to/annotation_package
```

### Run the Annotation Tool
Start the annotation process using the following command:
```bash
python main_perform_annotation.py
```
- Follow the terminal prompts to annotate facts.
- Input **A, B, C, D, or E** based on the defined criteria.
- Your responses will be **automatically saved**.

---

## Submitting Your Annotations
### Verify Saved Annotations
Ensure your annotations are saved in the output file provided in the package.

### Submit Your Work
After completing the annotation task:
1. **Zip the annotation package** (including the dataset and saved annotation file).
2. **Send it back** via the designated method (email, Google Drive, etc.).

---

## Troubleshooting & Support
- If you face **installation errors**, try reinstalling dependencies:
  ```bash
  pip install --upgrade polars loguru
  ```
- If the script fails to run, check if Python is properly installed:
  ```bash
  python --version
  ```


