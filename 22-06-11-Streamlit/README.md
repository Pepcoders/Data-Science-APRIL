Live at https://obscure-reef-27133.herokuapp.com/

create new environment
`python -m venv env`

activate env
linux `source ./env/bin/activate`
windows `env\Scripts\activate`

`pip install streamlit`
`pip install sklearn`

create app.py

Run file
`streamlit run app.py`

###Create Input fields
(Streamlit docs)[https://docs.streamlit.io/library/api-reference/widgets/st.number_input]

###Deploy in Heroku
https://devcenter.heroku.com/articles/getting-started-with-python

`pip freeze > requirements.txt`

`git init`
`git checkout -b main`
`heroku create`

Whenever file is modified run this command
`git add file_name`
`git commit -m 'init'`
`git push heroku main`

###Procfile
command to run, this is python app

###runtime.txt
python version to use