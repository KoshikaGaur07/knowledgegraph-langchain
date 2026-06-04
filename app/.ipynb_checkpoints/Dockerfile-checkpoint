FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY interface.py .

# gradio default
EXPOSE 7860

CMD ["python", "interface.py"]