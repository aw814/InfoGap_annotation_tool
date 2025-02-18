# README: Wikipedia Fact Annotation for InfoGap Pipeline Evaluation

## Introduction
This annotation task aims to evaluate knowledge gaps in Wikipedia across different languages. You will annotate facts based on their presence in Wikipedia articles using a **terminal-based annotation tool**.


---

## Setup Instructions
### Prerequisites
Ensure that you have the following installed:
- **Python 3.7+**
- **pip** (Python package manager)
- **Git** (for submitting your annotations)

### Activating the Virtual Environment
A virtual environment (`.venv`) is included in the annotation package. You must activate it before running the script:

#### On macOS/Linux:
```bash
source .venv/bin/activate
```

#### On Windows (Command Prompt):
```cmd
.venv\Scripts\activate
```

#### On Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Once activated, the terminal should indicate that the virtual environment is in use.

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
### Navigate to the Correct Language Directory
You must navigate to the appropriate **language directory** before running the annotation script. For example:
```bash
cd annotations/english  # or cd annotations/korean
```

### Run the Annotation Tool
Start the annotation process using the following command:
```bash
python main_perform_annotation.py
```
- Follow the terminal prompts to annotate facts.
- Input **A, B, C, D, or E** based on the defined criteria.
- Your responses will be **automatically saved** in a JSON file within the same directory.

---

## Submitting Your Annotations
Since this project is hosted on GitHub, you will need to push your changes after completing the annotation task.

### Steps to Submit Your Annotations
1. **Verify that your annotations are saved** in the JSON file in the respective language directory.
2. **Ensure that all examples are annotated** before submission.
3. **Commit and push your changes**:
   ```bash
   git add annotations/english/annotations.json  # or annotations/korean/annotations.json
   git commit -m "Annotated facts for [language]"
   git push origin main  # Or the branch you were assigned
   ```

Once you push your changes, I will be able to collect your results from the repository.

---

## Troubleshooting & Support
- If you face **issues activating the virtual environment**, ensure that you are in the correct directory.
- If the script fails to run, check if Python is properly installed:
  ```bash
  python --version
  ```
- For **Git-related issues**, ensure that you have the correct push permissions.


