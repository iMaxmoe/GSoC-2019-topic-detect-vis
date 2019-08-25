Bootstrap: docker
From: ubuntu

%labels
    AUTHOR maxmoe0105@gmail.com
    
%environment
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8

%post 
    apt-get update && apt-get -y install python python3 python3-pip git wget mongodb
    pip3 install wikipedia spacy nltk
    pip3 install pymongo Flask-PyMongo pipenv 
    
    python3 -m spacy download en_core_web_md
    


