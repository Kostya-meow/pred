# 
FROM python:3.9

# 
WORKDIR /workdir

# 
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

# 
COPY ./requirements.txt /workdir/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /workdir/requirements.txt

#
RUN echo "cache bust"

# 
COPY ./app /workdir/app

#
COPY ./model/ /workdir/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1234"]
