# Sierra_Rega
This project makes it able to call the Stanford service to perform algorithm comparisons

How to use the new project?

1. Install the SierraPy project from https://github.com/hivdb/sierra-client/tree/master/python: 

in short: 
```pip install sierrapy```

2. Prepare your fasta file (input.fasta) and run the following command from your command line:
```python looper.py -i input.fasta -q rega_query.gql```

where
* input.fasta is the file you just prepared
* rega_query.gql is the graphiql file which we use to request our needs from Stanford (this file is also available on Github, under https://github.com/rega-cev/Sierra_Rega/blob/master/rega_query.gql)
