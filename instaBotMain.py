from InstaBot import IgBot
import time
import pandas as pd
from pandas import Series, DataFrame
import os
import getpass
import openpyxl


class IgBotApp:
    def __init__(self):
        self.bots_dict = {'Bot Name': Series([]), 'Password': Series([]), 'Start Follow Time': Series([])}
        self.followers_check = {'Recent Followers Check': Series([])}
        self.client_bot_file, self.path = self.get_client_bot_data()
        client_path = f'{self.path}/{self.client_bot_file}.xlsx'
        if os.path.isfile(client_path):
            bots_dict_pd = pd.read_excel(client_path, sheet_name='Bot Followers')
            followers_check_pd = pd.read_excel(client_path, sheet_name='Client\'s Followers')
            self.bots_dict['Bot Name'] = self.bots_dict['Bot Name'].append(bots_dict_pd['Bot Name'], ignore_index=True)
            self.bots_dict['Password'] = self.bots_dict['Password'].append(bots_dict_pd['Password'], ignore_index=True)
            self.bots_dict['Start Follow Time'] = self.bots_dict['Start Follow Time'].append(bots_dict_pd['Start Follow Time'], ignore_index=True)
            self.followers_check['Recent Followers Check'] = self.followers_check['Recent Followers Check'].append(
                followers_check_pd['Recent Followers Check'], ignore_index=True)

    def get_client_bot_data(self):
        # This function returns values entered by the operator to the __init__ function
        client_name = input('Please enter a client name:\n')
        path = './'
        return client_name, path

    def options_menu(self):
        # this function prints the available options to the user.
        # Nothing is returned.
        print('\n' + '-' * 100 + '''\nWelcome To The Client Menu! Please choose one of the following options.
        [1] Save your work and end Bot-Client Service.
        [2] Add bot to client.
        [3] Remove bot from client.
        [4] Like all posts of client with a specific bot of your choice 
        [5] Like all posts of client with all bots added
        [6] Print current bot followers
        [7] Check recent unfollowers\n ''')
        print('\n' + '-' * 100 + '\n')

    def menu_choice(self):
        # This function gets user input and returns it only if the input is valid.
        while True:
            user_input = input('Please type your choice and press ENTER\n')
            try:
                choice = int(user_input)
                if 1 <= choice <= 7:
                    return choice
                else:
                    print('Choice is illegal. Please choose a number between 1 and 7\n')
            except ValueError:
                print('Choice is illegal. Please choose a number between 1 and 7\n')

    def run(self):
        # Runs an "infinite" dialog loop and executes operator's requests. Nothing is returned.
        # The loop breaks when the operator chooses 1 (save and exit app)
        while True:
            time.sleep(1.5)
            self.options_menu()
            choice = self.menu_choice()
            if choice == 1:
                print('Saving....\n')
                bots_df = DataFrame(self.bots_dict)
                bots_df = bots_df.reset_index(drop=True)
                recent_check_df = DataFrame(self.followers_check)
                file_name = f'{self.client_bot_file}.xlsx'
                if os.path.isfile(file_name):
                    wb = openpyxl.load_workbook(file_name)
                    del wb['Bot Followers']
                    del wb['Client\'s Followers']
                    wb.create_sheet()
                    wb.save(file_name)
                    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                    bots_df.to_excel(writer, sheet_name='Bot Followers')
                    recent_check_df.to_excel(writer, sheet_name='Client\'s Followers')
                    writer.save()
                else:
                    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                    bots_df.to_excel(writer, sheet_name='Bot Followers')
                    recent_check_df.to_excel(writer, sheet_name='Client\'s Followers')
                    writer.save()
                time.sleep(0.5)
                print('Saving is done!\n')
                print('Thank you for using IgBot! Have a great day :)\n')
                break

            else:
                if choice == 2:
                    bot_username = input("Please provide bot's username\n")
                    if bot_username in self.bots_dict['Bot Name'].values:
                        print('Bot already exist, please try again')
                        continue
                    else:
                        print("Please provide bot's password\n")
                        bot_password = getpass.getpass()
                        try:
                            bot_password = int(bot_password)
                            bot = IgBot(driver, bot_username, bot_password)
                            bot.login()
                            bot_username_pd = Series([bot_username])
                            bot_pass_pd = Series([bot_password])
                            time_added_pd = Series([time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())])
                            self.bots_dict['Bot Name'] = self.bots_dict['Bot Name'].append(bot_username_pd, ignore_index=True)
                            self.bots_dict['Password'] = self.bots_dict['Password'].append(bot_pass_pd, ignore_index=True)
                            self.bots_dict['Start Follow Time'] = self.bots_dict['Start Follow Time'].append(time_added_pd, ignore_index=True)
                            bot.follow_user(self.client_bot_file)
                            continue
                        except ValueError:
                            print('Cannot log in! please check client\'s username or bot\'s username and password and try again...\n')
                            continue

                elif choice == 3:
                    bot_name_remove = input('Please type the name of the bot you wish to remove.\n')
                    if bot_name_remove in self.bots_dict['Bot Name'].values:
                        bot_index = self.bots_dict['Bot Name'][self.bots_dict['Bot Name'] == bot_name_remove].index[0]
                        bot = IgBot(driver, self.bots_dict['Bot Name'][bot_index],
                                       str(self.bots_dict['Password'][bot_index]))
                        bot.login()
                        bot.unfollow_client(self.client_bot_file)
                        print('Bot removal was successful!')
                        self.bots_dict['Bot Name'] = self.bots_dict['Bot Name'].drop(bot_index)
                        self.bots_dict['Password'] = self.bots_dict['Password'].drop(bot_index)
                        self.bots_dict['Start Follow Time'] = self.bots_dict['Start Follow Time'].drop(bot_index)
                        continue
                    else:
                        print('Bot does not exist! Please try again\n')
                        continue

                elif choice == 4:
                    bot_name_likes = input('Please enter bot\'s name you wish to like all client\'s posts\n')
                    if bot_name_likes not in self.bots_dict['Bot Name'].values:
                        print('This bot does not follow the client! Please check its name\n')
                        continue
                    else:
                        bot_index = self.bots_dict['Bot Name'][self.bots_dict['Bot Name'] == bot_name_likes].index[0]
                        bot = IgBot(driver, self.bots_dict['Bot Name'][bot_index],
                                       str(self.bots_dict['Password'][bot_index]))
                        bot.login()
                        bot.like_posts(self.client_bot_file)
                        print(f'All recent posts are liked by {bot_name_likes}')
                        continue

                elif choice == 5 or choice == 6:
                    if len(self.bots_dict['Bot Name']) > 0:
                        if choice == 6:
                            print(f'The current bots who follow {self.client_bot_file} are:\n')
                        bot_lst = self.bots_dict['Bot Name'].values
                        for bot_name in bot_lst:
                            if choice == 5:
                                bot_index = self.bots_dict['Bot Name'][self.bots_dict['Bot Name'] == bot_name].index[0]
                                bot = IgBot(driver, self.bots_dict['Bot Name'][bot_index], str(self.bots_dict['Password'][bot_index]))
                                bot.login()
                                bot.like_posts(self.client_bot_file)
                            else:
                                print(f'{bot_name}\n')
                        continue
                    else:
                        print(f'No bots added yet for {self.client_bot_file}!\n')
                        continue

                elif choice == 7:
                    print('Please enter client\'s password\n')
                    client_password = getpass.getpass()
                    client = IgBot(driver, self.client_bot_file, str(client_password))
                    try:
                        client.login()
                        recent_check = list(self.followers_check['Recent Followers Check'].values)
                        self.followers_check['Recent Followers Check'] = client.check_unfollowers(recent_check)
                        continue
                    except ValueError:
                        print('Wrong password. Please try again')
                        continue


print('***** This program uses Chrome driver! *****')
driver = input('Please enter Chrome driver path\n')
app = IgBotApp()
app.run()


