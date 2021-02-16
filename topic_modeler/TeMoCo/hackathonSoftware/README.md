# TeMoCo Version Repo

## Embeddia Hackathon

Code available in the Hackathon folder

You can run the example by cloning this repo and starting a local server in the hackathon folder.

Using python this can be achieved by running the following from command line in the hackathon folder.

2.7
```python -m SimpleHTTPServer 8080```

3+
```python3 -m http.server```

The hackathon folder also contains examples of converting articles and model outputs to the input files needed
to run the visualisation.

### Usage
To use the visualisation with new data you should first partition your dataset into topics and time intervals.

Then identify keywords associated with those temporal topics.

You could use embeddia or third party tools for topic modeling and keyword extraction. 

Metadata availabe for your dataset could also be used as topics.

If you can calculate topic size per time slice you can use that to build the visualisation otherwise set the topic size such that
the topic sizes for each time slot add to 1 e.g. for 4 topics in a time slice set the topic size to 0.25

From this information you should then build an input file similar to hackathonSoftware/articles1.csv and a JSON file containing the article text similar to
the file hackathonSoftware/articles.json 

hackathonSoftware/convertinDataExample contains two directorys with example python scripts and data.

hackathonSoftware/convertinDataExample/articlesToJSON shows how to convert a folder of .txt articles to a single .json file to use as input for the visualisation.

hackathonSoftware/convertinDataExample/articlesToJSON contains an example of converting a model output .json file to the visualisation input.csv format.

These examples are provided to help get you started converting your data and model outputs to the visualisation inputs. You will need to edit them to match the data and models you are using.
