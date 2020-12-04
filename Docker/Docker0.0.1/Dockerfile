FROM jupyter/datascience-notebook

USER jovyan

RUN pip install jupyterlab-git
RUN pip install requests
RUN pip install scanpy
RUN pip install flask
RUN pip install dash
RUN pip install streamlit
RUN jupyter labextension install @jupyterlab/git @telamonian/theme-darcula
	
COPY @jupyterlab .jupyter/lab/user-settings/@jupyterlab

USER root

#RUN	usermod -l wusuowei jovyan && \
# 	usermod -d /home/wusuowei -m wusuowei && \
# 	usermod -u 60 wusuowei

RUN apt-get update && \
	apt-get upgrade -y --no-install-recommends && \
	apt-get install -y --no-install-recommends zsh


RUN chsh -s /bin/zsh

SHELL ["zsh", "-c"]

WORKDIR /home/jovyan

RUN	sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

#RUN chmod -R 777 /home/jovyan/.oh-my-zsh

WORKDIR /home/jovyan/.oh-my-zsh

RUN	git clone git://github.com/zsh-users/zsh-autosuggestions ./plugins/zsh-autosuggestions && \
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ./plugins/zsh-syntax-highlighting

WORKDIR /home/jovyan

USER jovyan

COPY .zshrc .

RUN source ~/.zshrc

CMD ["zsh"]
	