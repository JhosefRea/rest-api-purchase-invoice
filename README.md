# 🚀 PROYECTO BACK-END. Sistema de gestión de facturas de compra!!

Este es un proyecto de gestión de facturas de compra utilizando **FastAPI** como framework web y **MongoDB ATLAS** como base de datos, en Ubuntu 22.04. Se utiliza **Arquitectura Hexagonal** **SOLID** **Clean Code** para garantizar un código modular, escalable y fácil de mantener.⚡️

## 📋 Requisitos

- **Python 3+**
- **MongoDB 8+** (en ejecución local o en la nube)

## 🔧 Instalación
# 📖 Pasos para instalar y ejecutar el proyecto

1. **Clonar el repositorio**

2. **Crear un entorno virtual**

Para crear un entorno virtual y evitar conflictos con otras dependencias globales, usa el siguiente comando:

```bash
python -m venv venv
```

3. **Activar el entorno virtual**
En distros gnu/linux S.O.
```bash
source venv/bin/activate
```
En Windows S.O.
```bash
venv\Scripts\activate
```

4. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

5. **Crea tu archivo .env**
Guíate en el archivo .env.example

6. **Ejecutar el servidor FastAPI**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```
![image](https://github.com/user-attachments/assets/dc57431c-ba80-4710-a8c0-b128ae6abd3e)


## Créditos 👨🏻‍💻
&copy; Copyright 2025. Todos los derechos reservados.
