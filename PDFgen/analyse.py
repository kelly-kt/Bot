def process_messages(messages):
    print('Processing messages for report')
    message_details = {'all': {'messages': []}}

    for msg in messages:
        user = msg['user_name']
        channel = msg['channel_name']

        if channel not in message_details:
            message_details[channel] = {'messages': []}
        message_details[channel]['messages'].append(msg['message_content'])

        message_details['all']['messages'].append(msg['message_content'])

    return message_details


def process_bad_messages(bad_messages):
    print('Processing bad messages for report per user and per channel')
    bad_users = {}
    bad_channels = {}

    for msg in bad_messages:
        user = msg['user_name']
        channel = msg['channel_name']

        if user not in bad_users:
            bad_users[user] = {'messages': [], 'count': 0}
        bad_users[user]['messages'].append(msg['message_content'])
        bad_users[user]['count'] += 1

        if channel not in bad_channels:
            bad_channels[channel] = {'messages': [], 'count': 0}
        bad_channels[channel]['messages'].append(msg['message_content'])
        bad_channels[channel]['count'] += 1

    return (bad_users, bad_channels)
