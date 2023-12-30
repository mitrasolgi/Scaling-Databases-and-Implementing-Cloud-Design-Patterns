
# Cloud Computing Final Project
# Instructions
1. Start the lab in AWS Academy

2. Paste all your AWS cretentials into the `config.py` file

        security_group_name     - The name of your secturity group
        key_name                - The name of your key pair (e.g. vockey)
        key_path                - The path to your key (e.g. path/to/vockey.pem)
        region_name             - E.g. us-east-1
        aws_access_key_id       - Found in AWS Academy
        aws_secret_access_key   - Found in AWS Academy
        aws_session_token       - Found in AWS Academy

3. Create the instances by running `create_instances.py`

   
python3 app.py direct 

python3 app.py randomized

python3 app.py customized

For sending the write requests and test the app:

python3 test_app.py

