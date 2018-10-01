### Game of nuts ###
### Name: Thai Doan

import random
def main():
    ### Variables ###
    min_nuts = 10 #Minimum number of nuts
    max_nuts = 100  #Maximum number of nuts
    min_take_nuts = 1 #Minimum number of nuts to take
    max_take_nuts = 3 #Maximum number of nuts to take
    intro_line = "Welcome to the game of nuts!"
    ask_nuts = "How many nuts are there on the table initially ({0}-{1})?: ".format(min_nuts,max_nuts) #Asking for the number of nuts
    re_nuts = "Please enter a number between {0}-{1}".format(min_nuts,max_nuts)
    intro_option = "Options: \n Play against a friend (1) \n Play against the computer (2) \n Play against the trained computer (3)"
    a_option = "Which option do you take (1-3)?: " #Asking for choosing one of these given options
    re_op = "Your option is not available. Please try again"
    ask_take_nuts = "How many nuts do you take ({0}-{1})?: ".format(min_take_nuts, max_take_nuts)
    re_take_nuts = "Please enter a number between {0} and {1}".format(min_take_nuts, max_take_nuts)
    mess_again = "Do you want play again (1 = YES, 0 = NO)?"
    mess_wait = "Please wait, AI is being trained..."
    AI_data = [] #Storing data for AI
    AI_data_beside = []
    still_loop = True

    def play_again(mes, rej_option):        
        ''' Checking if user wants to play again '''
        ## mes: A message is displayed to ask if player wants to play again 
        ## rej_option: A message asks player to take an available option
        while (True):
            ask_play = input(mes)
            if ask_play == "1": 
                return True
            elif ask_play == "0": 
                return False
            else: #If player did not choose an available option, ask to choose again
                print(rej_option)

    def is_play_again(option, mes, rej_option):
        ''' Break if user does not want to play or pass and turn back that option '''
        keep_loop, ask_option = True, None
        if play_again(mes, rej_option):
            ask_option = option #Prevent user from being asked to choose number of nuts and option again
        else:
            keep_loop = False
        return keep_loop, ask_option

    def statistic(cur_nuts):       
        ''' Returning the current nuts on the board '''
        ## cur_nuts: the current number of nuts on the board     
        statistic = "\nThere are {0} nuts on the board.".format(cur_nuts)
        print(statistic)

    ##### Player vs Player #####        
    def user_and_user(cur_nuts, rej_take_nuts, a_take_nuts):        
        ''' Main function for user vs user mode '''
        ## cur_nuts: The current number of nuts on the board
        ## rej_take_nuts: A message asks player to enter an available number
        ## a_take_nuts: A message asks player the number of nuts to take        
        id_player = 1 
        while (True):
            statistic(cur_nuts) # Print the statistic
            player_lose = "Player {0}: You lose !".format(id_player) 
            while (True):
                ask_player = "Player {0}: {1}".format(id_player,a_take_nuts)
                take_nuts = int(input(ask_player)) # The number of nuts player takes
                if 1 <= take_nuts <= 3 : # If the taken number of nuts is in range of [1,3]
                    cur_nuts -= take_nuts
                    if cur_nuts <= 0: # The player loses
                        print(player_lose)
                        return #Breaking the whole loop
                    break
                else: # If the player did not choose the number of nuts between [1,3]
                    print(rej_take_nuts) 
            # Updating the id_player
            if id_player == 2: 
                id_player = 1
            else: 
                id_player = 2

    ##### Player vs AI #####                
    def data_setup(data, data_beside, total_nuts): 
        ''' Setting up the lists to store data of AI '''
        ## data: The AI's data list to store balls
        ## data_beside: The AI's second list to compare and update the first list (data)
        ## total_nuts: The initial number of nuts
        for i in range(total_nuts): 
            arr_data = [1,1,1] #Creating a children list with default value is 1
            data += [arr_data] #Adding new data to the parent list
            data_beside += [[0,0,0]] #Creating another list beside the first one

    def ai_choose(data,cur_nuts): 
        ''' Return the number of nuts that AI takes '''
        ## data: The AI's data list to store balls
        ## cur_nuts: The current number of nuts on the board   
        cur_list = data[cur_nuts-1] 
        sum_data = sum(cur_list) 
        rand_num = random.randint(1,sum_data)
        if rand_num <= cur_list[0]: 
            nut_taken = 1
        elif rand_num <= cur_list[0] + cur_list[1]: 
            nut_taken = 2
        else: 
            nut_taken = 3
        return nut_taken

    def add_data_beside(data, data_beside,cur_nuts,num_nuts_taken):
        ''' Add the ball next to the current hat at respective position '''        
        ## data: The AI's data list to store balls
        ## data_beside: The AI's second list to compare and update the first list (data)
        ## cur_nuts: The current number of nuts on the board
        ## num_nuts_taken: The current ball (number of nuts taken)       
        p_ball = num_nuts_taken - 1 #Position of that ball in that hat
        cur_pos = cur_nuts - 1 
        cur_list = data[cur_pos]
        cur_list[p_ball] -= 1 #Take out 1 ball that has the number of nuts chose
        data_list = data_beside[cur_pos] #Position of the hat in data_beside
        data_list[p_ball] = 1 #Add 1 to the respective position of the ball in the hat in data_beside

    def update_list(data, data_beside, is_win):
        ''' Update the list after the game is over '''        
        ## data: The AI's data list to store balls
        ## data_beside: The AI's second list to compare and update the first list (data)
        ## is_win: To determine if the computer wins        
        for a,b in enumerate(data_beside):
            for n,i in enumerate(b):
                if i == 1: #Check if any element in list data_beside is 1
                    cur_hat = data[a]
                    cur_ball = cur_hat[n]
                    if is_win: #Computer wins
                        new_data = 2*i #The ball and additional ball of the same type    
                        cur_ball += new_data #Add the balls back to the old position
                        cur_hat[n] = cur_ball #Save the data 
                    elif not is_win and cur_ball == 0: #Computer loses and the hat hat doesn't have any type of that ball
                        cur_hat[n] = 1 #Add that ball back to the hat
                    b[n] = 0 #Remove that ball in the current hat in data_beside

    def ai_vs_ai(data, data_beside , ini_nuts):
        ''' Two computer will play to each other and update the "data" list (Training AI) '''
        ## ini_nuts: The initial number of nuts on the table
        ## data: The AI's data list to store balls (For updating the list)
        AI_1, AI_2 = [],[]
        AI_1_beside, AI_2_beside = [],[]
        data_setup(AI_1, AI_1_beside, ini_nuts)
        data_setup(AI_2, AI_2_beside, ini_nuts)
        AI_list = [AI_1,AI_2]
        AI_beside_list = [AI_1_beside,AI_2_beside]
        is_win = None #To check if any AI wins
        cur_nuts = ini_nuts  #The initial number of nuts on the board
        print(mess_wait)
        for i in range (100000):
            keep_loop = True
            while (keep_loop):
                for k in range(2):
                    if is_win != None: #If the previous AI lost, this AI has to update its list
                        is_win, keep_loop = True, False #This AI wins and break the while loop
                        update_list(AI_list[k], AI_beside_list[k], is_win)
                        is_win = None
                        break #Break the for loop
                    nuts_taken = ai_choose(AI_list[k], cur_nuts)
                    add_data_beside(AI_list[k], AI_beside_list[k], cur_nuts, nuts_taken)
                    cur_nuts -= nuts_taken
                    if cur_nuts <= 0: #Current AI loses, update the list
                        is_win = False 
                        update_list(AI_list[k], AI_beside_list[k], is_win)
                        cur_nuts = ini_nuts #Reset the current number of nuts to the initial one
        data[:] = AI_1[:] #Update the data list

    def user_vs_ai(data, data_beside, cur_nuts, rej_take_nuts, a_take_nuts):
        ''' Main function for user vs ai mode '''
        id_player = 1 #Always is 1 in user vs AI mode
        while (True):
            statistic(cur_nuts) #Show the statistic
            while (True):
                ask_player = "Player {0}: {1}".format(id_player,a_take_nuts)
                user_take_nuts = int(input(ask_player))
                if 1 <= user_take_nuts <= 3: #If the number of nuts taken in [1,3]
                    cur_nuts -= user_take_nuts #Update the number of nuts
                    ### Computer's turn
                    if cur_nuts <= 0: #Player loses - AI wins
                        is_win = True
                        update_list(data, data_beside, is_win)
                        print("You lose")
                        return
                    else:
                        num_nut_taken = ai_choose(data, cur_nuts) #The number of nuts compute chooses
                        print(">> AI selects: {}".format(num_nut_taken)) #Print the number was chosen
                        add_data_beside(data, data_beside, cur_nuts, num_nut_taken) 
                        cur_nuts -= num_nut_taken
                        if cur_nuts <= 0: #AI loses - Player wins
                            is_win = False
                            update_list(data, data_beside, is_win)
                            print("Computer loses")
                            return 
                    break
                else:
                    print(rej_take_nuts)

    while (still_loop):
        print(intro_line) #Print the introduction line
        num_nuts = int(input(ask_nuts))
        ask_option = None
        if min_nuts <= num_nuts <= max_nuts: #If the number of nuts is in the given range
            print(intro_option) #Print the instruction for these options
            data_setup(AI_data, AI_data_beside, num_nuts) #Setting the data first
            while (still_loop): #Second loop for asking for which option user wants to choose
                if ask_option == None:
                    option = int(input(a_option))
                else:
                    option = ask_option #Continue playing with current option without being asked again
                if option == 1: #Player chose to play with another players
                    user_and_user(num_nuts, re_take_nuts, ask_take_nuts)
                    still_loop, ask_option = is_play_again(option, mess_again, re_op)
                elif option == 2: #Player chose to play with naive AI
                    user_vs_ai(AI_data, AI_data_beside, num_nuts, re_take_nuts, ask_take_nuts)
                    still_loop, ask_option = is_play_again(option, mess_again, re_op)
                elif option == 3: #Player chose to play with trained AI
                    if ask_option == None: #To avoid training AI again when player wants to play again) 
                        ai_vs_ai(AI_data, AI_data_beside, num_nuts) #Trains AI
                    user_vs_ai(AI_data, AI_data_beside, num_nuts, re_take_nuts, ask_take_nuts)
                    still_loop, ask_option = is_play_again(option, mess_again, re_op)
                else:
                    print(re_op)
        else:
            print(re_nuts)

main()