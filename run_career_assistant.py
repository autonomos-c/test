import os
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def run_notebook(notebook_path):
    # Leer el notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Configurar el ejecutor de notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    try:
        # Ejecutar el notebook
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
    except Exception as e:
        print(f"Error al ejecutar el notebook: {e}")
        sys.exit(1)

    # Guardar el notebook ejecutado
    output_path = notebook_path.replace('.ipynb', '_executed.ipynb')
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Notebook ejecutado exitosamente. Resultado guardado en {output_path}")

if __name__ == "__main__":
    notebook_path = "/workspaces/test/career_assistant.ipynb"
    run_notebook(notebook_path)
