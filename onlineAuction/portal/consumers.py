from channels import Group

# Connected to websocket.connect
def ws_add(message):
    Group("bids").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    """Group("bids").send({
        "text": "%s" % message.content['text'],
        })"""
    pass


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("bids").discard(message.reply_channel)