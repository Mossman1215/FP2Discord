from chalice import Chalice,BadRequestError,UnauthorizedError,ChaliceViewError
from urllib.parse import urlparse, parse_qs
import requests
import os

app = Chalice(app_name='FPtoDiscord')

@app.route('/')
def index():
    raise BadRequestError("Get not implemented")

@app.route('/{authstring}', methods=['POST'],
            content_types=['application/json'])
def forwardFreshPingMessage(authstring):
    if(os.environ['FP2D_TOKEN'] == authstring):
    # This is the JSON body the user sent in their POST request.
        freshpingMessage = app.current_request.json_body
        message = "{} is {} with status code {}".format(freshpingMessage['webhook_event_data']['check_name'],freshpingMessage['webhook_event_data']['check_state_name'],freshpingMessage['webhook_event_data']['http_status_code'])
        discord_payload = {'username': 'minecraft-status', 'content': message}
        r = requests.post(os.environ['DISCORD_URL'], json=discord_payload)
        if(r.status_code == 204):
            return {"status": "good"}
        else:
            raise ChaliceViewError("Post request failed status"+ str(r.status_code))
    else:
        raise UnauthorizedError()
    
