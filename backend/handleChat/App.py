from .config import ConfigData
from g4f.client import Client
from .models import person
# from .models import person
import json

def give_query(query):
  print(query)
  table_schema = ConfigData.TABLE_SCHEMA
  schema_description = ConfigData.SCHEMA_DESCRIPTION
  json_ex_1 = ConfigData.FEW_SHOT_EXAMPLE_1
  json_ex_string = json.dumps(json_ex_1)



  prompt_template_for_creating_query = """
    You are an expert in crafting NoSQL queries for MongoDB with 10 years of experience, particularly in MongoDB. 
    I will provide you with the table_schema and schema_description in a specified format. 
    You have to return me just the query and no explanation with it.Please !!
    I have done all imports and the collection name is 'person'.I am using pymongo package to connect my python app with MongoDb.

    The query should be like person.find or person. any function.

    Following is the example of how should the query be:
    """+json_ex_string+""""
    

    Table schema:""" +  table_schema + """
    Schema Description: """ + schema_description + """
    
    Input: """+query+"""
    
    
    
    """
  print(prompt_template_for_creating_query)

  client = Client()
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt_template_for_creating_query}],
)
  ans=response.choices[0].message.content
  print(ans)
  return ans

# def execute_query(pipeline):

#     # Execute the aggregation pipeline
#     result = person.aggregate(pipeline)
#     print(result)
#     return list(result)

# Here are some examples:
#     Input: name of users where the country is 'India'
#     Output: {json_ex_string_1} 

# yes=give_query("Give me the details of username Priyanshu23")
# execute_query(yes)

