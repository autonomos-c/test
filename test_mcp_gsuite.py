from smithery import MCP

# Configurar el cliente MCP
mcp_gsuite = MCP("mcp-gsuite")

# Intentar listar archivos en Google Drive
try:
    files = mcp_gsuite.list_files("/")
    print("Archivos encontrados:")
    for file in files:
        print(file)
except Exception as e:
    print(f"Error al listar archivos: {e}")
