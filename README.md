# DNA-Sample-Server-API
A FastAPI-based web service for uploading ancient remains data, generating DNA sequences using metadata, comparing genetic similarity between samples, and answering natural language queries about the system.
---First save the files(server.py, func.py) and data set (dirty_sample_data.csv) in one folder

1. Running the server

     1.1  Prerequisites:
             (a) Python 3.7+ installed.  (If not installed, install from official site)
            (b) Install FastAPI and Uvicorn (and other libraries as specified in the code)

            To install FastAPI and Uvicorn--- open cmd, go to the scripts folder of your python folder and run the command:
                                    pip install fastapi uvicorn
             
     1.2 To run the server

          1.2.1 open cmd and go to the folder where the python file is saved  (u can go to any folder in cmd using 'cd ' command e.g cd Desktop)
                      then run the following command in cmd: 
                                           uvicorn server:app --reload

                if this commands runs successfully, you should see the following in cmd:
  
               ←[32mINFO←[0m:     Will watch for changes in these directories: [location of the folder]
                ←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
               ←[32mINFO←[0m:     Started reloader process [←[36m←[1m14180←[0m] using ←[36m←[1mStatReload←[0m
               ←[32mINFO←[0m:     Started server process [←[36m9060←[0m]
               ←[32mINFO←[0m:     Waiting for application startup.
                ←[32mINFO←[0m:     Application startup complete.
  
     1.2.2  After running this command successfully, open any browser and search for this address:
                                  http://127.0.0.1:8000//docs
                This will open the interface of the server where you can:
                              i) upload your csv file 
                             ii)  generate a dna sequence for any sample 
                            iii)  compare the dna sequences of any two samples
                           iv)  interact with the server using different queries

2.  Executing operations

      2.1  upload your csv file (file should be your data file with the attributes: id, region ,age and seed):
                         a)click upload file in the browser screen
                         b) click Try it out
                         c) click Execute
           If the file is uploaded, it should print "File uploaded successfully" in response body

     2.2  generate dna sequence for a sample:
                a) click generate sequence
                b) click Try it out
                c) enter the sample id  (it should be a valid id in data file)
                d) click Execute   
           you will get the dna sequence of sample of this id in response body of the console.

     2.3 compare the dna sequences of any two samples
               a) click compare sequence
               b) click Try it out
               c) enter the sample id of two samples 
               d) click Execute   
       you will get the similarity score of dna sequences of two samples

      2.4 interact with the server
            a) click ask me anything
            b)  click Try it out
            c) enter your question in request body as:
                            you will see something like this  -------   "question": "string" -------in request body
                     replace the string with your question.
           d) click execute

         you will get the answer inside the response body there.
