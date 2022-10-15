FROM ubuntu:18.04

RUN apt update
RUN apt install python3 -y  
RUN apt install g++ -y 
RUN apt install cmake -y 
RUN apt install nano -y
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  
RUN mkdir a1_a2_rnbp 
RUN mkdir bp 
RUN mkdir framework-main-2 
RUN mkdir LWFWSW 
RUN mkdir matrices 
RUN mkdir paar 
RUN mkdir yosysTools 
RUN mkdir XZLBZ

copy a1_a2_rnbp /a1_a2_rnbp
copy bp /bp
copy framework-main-2 /framework-main-2
copy LWFWSW /LWFWSW
copy matrices /matrices
copy XZLBZ /XZLBZ
copy paar /paar
copy yosysTools /yosysTools
copy main.py /
copy matrices/matrix.txt /matrices/matrix.txt
copy parameter.txt / 

CMD [ "python3", "main.py"]
