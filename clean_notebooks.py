import nbformat
import os

# Function to clean a single notebook
def clean_notebook(path):
    with open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    changed = False
    for cell in nb.cells:
        # Remove widget metadata only
        if "metadata" in cell and "widgets" in cell["metadata"]:
            del cell["metadata"]["widgets"]
            changed = True
        
        # Optional: remove other empty/null metadata fields
        if "metadata" in cell:
            original_meta = dict(cell["metadata"])
            cell["metadata"] = {k:v for k,v in cell["metadata"].items() if v is not None and v != {}}
            if cell["metadata"] != original_meta:
                changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Cleaned metadata in: {path}")

# Walk through all notebooks in the repo folder
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".ipynb"):
            notebook_path = os.path.join(root, file)
            clean_notebook(notebook_path)

print("All notebooks cleaned safely! Outputs preserved.")
