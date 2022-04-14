FROM conda/miniconda3

WORKDIR /app

COPY conda.yml .
RUN conda env create -f conda.yml
RUN conda init bash

RUN echo conda activate json_parser_bspump >> /root/.bashrc

COPY . .
CMD bash -lc 'python json_parser.py -c site.conf'