from InstagramAPI import InstagramAPI
import os


def unfollowers(username: str, password: str):
    # create an InstagramAPI object and log in to the account
    api = InstagramAPI(username, password)
    api.login()

    # check if there was an error logging in
    if api.LastJson['status'] != 'ok':
        return api.LastJson

    # create an empty list to store all of the users you follow
    following = []

    # retrieve the full list of users you follow in batches
    next_max_id = True
    while next_max_id:
        # get a batch of users
        _ = api.getSelfUsersFollowing(maxid=next_max_id)
        # add the retrieved users to the list
        following.extend(api.LastJson['users'])
        # get the ID of the next batch of users, if available
        next_max_id = api.LastJson.get('next_max_id', '')

    # create an empty list to store users who don't follow you back
    not_following_back = []

    # iterate through the list of users you follow
    for user in following:
        # check if the user follows you back
        user_info = api.getUsernameInfo(user['pk'])
        if isinstance(user_info, bool):
            # if api.getUsernameInfo returns a boolean value, the user does not follow you back
            not_following_back.append(user)
        elif not user_info['user']['following']:
            # if the user does not follow you back, add them to the list
            not_following_back.append(user)

    # return the list of users who don't follow you back
    return not_following_back


# Get username from user
usn = input("Username: ")
# Get Password from user
pw = input("Password : ")


try:
    # clear the terminal screen on Windows
    os.system("cls")
except:
    pass

try:
    # clear the terminal screen on Unix-based systems
    os.system("clear")
except:
    pass
# call the unfollowers function and print the result
unfollowers_list = unfollowers(usn, pw)
if isinstance(unfollowers_list, dict):
    # if there was an error logging in, print the error message
    print(unfollowers_list['message'])
else:
    # print the list of users who don't follow you back
    print(unfollowers_list)
