# trec-eval

The purpose of this application is to provide a tool that lets researchers evaluate how good their search system is and how it compares to other systems (already submitted).

# GitHub Accounts

dilkas: Paulius Dilkas 2146879d

gerardward3: Gerard Ward 2131783w

ffindlay: Fiona Findlay 2138452f

# How to Run

1. Download the necessary files.

        git clone https://github.com/ffindlay/trec-eval.git
        wget http://trec.nist.gov/trec_eval/trec_eval_latest.tar.gz
2. Compile trec_eval and copy it to its place.

        tar -zxvf trec_eval_latest.tar.gz
        cd trec_eval.9.0/
        make
        cp trec_eval ../trec-eval/
3. Set up a virtual environment.

        cd ../trec-eval/
        mkvirtualenv -p /usr/bin/python2 trec
        pip install -r requirements.txt
4. Set up the database.

        python manage.py migrate
        python populate_trec.py
5. Run the server.

        python manage.py runserver
