import os

rootDirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sourceDirectory = os.path.join(rootDirectory, 'src')

reportDirectory = os.path.join(rootDirectory, 'report')

cacheDirectory = os.path.join(rootDirectory, 'cache')

promptDirectory = os.path.join(rootDirectory, 'prompt')

llmApiEndpoint = 'http://localhost:11434/api/generate'
llmModelName = 'codellama:7b'
