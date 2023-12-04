FROM python:3.9-alpine
WORKDIR /app

# Copia los archivos 'requirements.txt' y los instala para manejar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará tu aplicación FastAPI
EXPOSE 8000

# Ejecuta tu aplicación FastAPI utilizando uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]