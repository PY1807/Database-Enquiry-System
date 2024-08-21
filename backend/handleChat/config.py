class ConfigData:
   
    OPEN_AI_KEY="MY OPEN_AI_KEY"
    TABLE_SCHEMA = '''
                    "username": "string",
                    "firstname": "string",
                    "lastname": "string",
                    "country": "string",
                    "Security Question": "string",
                    "Answer": "string",
                    "email": "string",
                    "password1": "string",
                    "password2": "string",
                    "password3": "string",
                    "Date": "string",
                    "Time": "string"
                    '''
    
    SCHEMA_DESCRIPTION = '''

                    Here is the description to determine what each key represents:
                    1. username:
                        - Description: Unique username of the user.
                    2. firstname:
                        - Description: First name of the user.
                    3. lastname:
                        - Description: Last name of the user.
                    4. country:
                        - Description: Country of residence of the user.
                    5. Security Question:
                        - Description: Security question set by the user.
                    6. Answer:
                        - Description: Answer to the security question.
                    7. email:
                        - Description: Email address of the user.
                    8. password1:
                        - Description: First password of the user.
                    9. password2:
                        - Description: Second password of the user.
                    10. password3:
                        - Description: Third password of the user.
                    11. Date:
                        - Description: Date of account creation.
                    12. Time:
                        - Description: Time of account creation.

                    '''
    FEW_SHOT_EXAMPLE_1 = [
                            {
                                "$match": {"country": "India"}
                            },
                            {
                                "$project": {
                                    "username": 1,
                                    "firstname": 1,
                                    "lastname": 1,
                                    "country": 1,
                                    "Security Question": 1,
                                    "Answer": 1,
                                    "email": 1,
                                    "password1": 1,
                                    "password2": 1,
                                    "password3": 1,
                                    "Date": 1,
                                    "Time": 1
                                }
                            }
                        ]
