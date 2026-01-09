import bcrypt

# Escribe aquí la contraseña que quieras usar
password = "Educacion2026"

# Generar el Hash
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print("\n--- COPIA EL CODIGO DE ABAJO ---")
print(hashed.decode('utf-8'))
print("--------------------------------\n")