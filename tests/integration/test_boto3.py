from gofannon.open_notify_space.iss_locator import IssLocator
import json
import sys

# Pass in as a param
build = True 

if build:
    agent_app_config = {
        "app_id": "gofannon_demo",
        "agent_name": "ISSLocator",
        "agent_session_timeout": 600,
        "instruction": "You are an agent skilled at tracking and reporting the location of the International Space Station. Your role is to help users understand where the ISS is currently located by providing its geographic coordinates and other relevant location details.",
        "agent_description": "This agent helps to locate the location of the ISS.",
        "target_model": "anthropic.claude-3-sonnet-20240229-v1:0",  # this needs to be picked from a list
        "python_runtime_version": "python3.13",
        "temp_build_root": "/tmp/build",  # this must not exist
    }

    iss_locator = IssLocator()
    try:
        bedrock_config = iss_locator.export_to_bedrock(
            agent_app_config=agent_app_config
        )
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

    print(json.dumps(bedrock_config, indent=3))
else:
    account_id = "<aws account id>"
    region = "<aws region>"
    bedrock_config = {
        "lambdaARN": f"arn:aws:lambda:{region}:{account_id}:function:gofannon_demo_iss_locator",
        "lambdaRoleName": "gofannon_demo_bedrock_lambda_execution_role",
        "agentId": "I9CGGKG3X8",
        "agentRoleName": "gofannon_demo_bedrock_agent_execution_role",
        "agentPolicyARN": f"arn:aws:iam::{account_id}:policy/gofannon_demo_bedrock_agent_allow_model",
        "agentActionGroup": "FBWX2MIEZJ",
    }

    iss_locator = IssLocator()
    burn_down = iss_locator.delete_app(bedrock_config=bedrock_config)

# TODO: API call to newly created agent....
