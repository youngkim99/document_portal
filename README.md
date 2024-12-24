- Steps to start the services - how can we run your project?
  1) `git clone https://github.com/youngkim99/document_portal.git
  2)  `cd document_portal`
  3) I didn't work in a virtual environment so I couldn't pip freeze a requirements.txt file, but I made an incomplete one that you can install from with 
  `python -m pip install -r requirements.txt`.
  4) From the top level directory (document_portal/), run `python manage.py migrate` to migrate database schemas
  5) Start the Django dev server `python manage.py runserver`
  
- Design - how is your project structured and what are some key design decisions that you made?
    My project is a Django project that encapsulates a frontend folder for the HTML/CSS/JS files, a main project directory "document_portal/document_portal", and an app directory "document_portal/documents". Most of the logic for the backend, including scripts for data extraction, database models, APIViews, and url configurations lies in the "documnet_portal/documents" app folder. The front end consists of a simple HTML home page that prompts a form submission for a pdf. script.js contains an event handler for the submission form and makes POST requests to the backend for extracting data. It also makes GET requests for viewing a document and its extracted data in an iframe when a user clicks on a completed process in the process list. A successfully processed document will show up in the process list below the submission form (but currently a bug prevents successful processing). File uploads are stored in document_portal/media/uploads to be later shown in the iframe.

- Assumptions - did you make any assumptions that we should be aware of?
    Not that I am aware of.

- Improvements - what would you do differently if you had more time?
  I would have not spent so much time trying to get the LLMs to work. I ran into strange errors like module import failures for packages I definitely had, and rate limits for all version of my extract_fields_* attempts, even after buying the paid version of chatGPT and having used it at most once before. This led to a desperate last minute attempt to hard code the extracted_data, which ended up incomplete in the submission anyway. 

  I essentially spend the last couple hours debugging the same few functionalities. I think I could have debugged smarter, but being unfamiliar with some parts of the framework as well as the errors I was encountering slowed me down considerably. 

  At some point, the "documents" app directory, where most of the backend code was written, was overwritten by my app's upload folder, and I could not run the necessary Django commands despite having restored the directory. This caused me to spend about 45 minutes resetting and rewriting the Django app.

  I wrote code for viewing a processed file submission and showing the extracted data as a JSON, but never got to test it or render it. Were I to do this again, I would move on from working on buggy parts and try to get as many of these other features to work as possible.

  I didn't get to implement the highlighting feature on the extracted fields of the uploaded documents, but would have wanted to do so with more time.

  