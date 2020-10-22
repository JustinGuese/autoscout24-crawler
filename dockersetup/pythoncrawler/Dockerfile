FROM pythonautoscout:1.1
COPY /src/autoscouter_docker.py /
COPY /src/copyschedule.py /
COPY /src/scriptexec.sh /
RUN chmod a+x scriptexec.sh
CMD [ "./scriptexec.sh" ] 

