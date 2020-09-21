"""
blackjack.py

Full game of blackjack.
Uses a single 52 card deck that is recreated after every round.
Number of dealer and player wins are tallied and printed after each round.
Number cards are worth the corresponding number of points
Face cards are worth 10 points
Ace is worth 11 points but is changed to 1 point if bust is exceeded
"""
from random import randint
from time import sleep
from os import system


def build_deck():
    """
    Creates the standard 52 card deck

    The number of points for each card is stored as an interger in a dictionary
    where the key is the a string containing the name of the card - card_points
    A list of the 52 cards is also created - deck_list
    """
    face_card_values = {'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    card_points = {}
    deck_list = []
    for card in range(2, 11):
        # adds the number cards and their number of points to the deck dictionary
        face_card_values[str(card)] = card
    for suit in suits:
        for value in face_card_values:
            #creates a card of each rank for each suit
            card_points[f'{value} of {suit}'] = face_card_values[str(value)]
            deck_list.append(f'{value} of {suit}')
    return card_points, deck_list

def draw_card(num_card, deck, hand, player=False):
    """
    Draws random cards from the deck list, then deletes that card.

    Args:
    num_card: The desired integer number of cards to be drawn
    deck: The list of cards crrently in the deck
    hand: The list containing the player's cards or the dealer's cards
    player: Boolean. Default False for dealer, change to True for player.
    Returns a list containing all of the cards drawn to that hand.
    """
    if player:
        for draw in range(num_card):
            #loop through the number of cards required
            random_number = randint(0, len(deck)-1)
            #a random integer is generated from the range 0 - 51
            hand.insert(draw, deck[random_number])
            #pulls a random card from the card deck and places it in the player's hand
            deck.pop(random_number)
            #removes that card from the deck so it can't be drawn again
        return hand
    for draw in range(num_card):
        random_number = randint(0, len(deck)-1)
        hand.insert(draw, deck[random_number])
        deck.pop(random_number)
    return hand

def card_total(cards, points_dict, player=False):
    """
    Calculates the sum of the card values.

    Args:
    cards: The list of the player's or the dealer's cards
    points_dict: The dictionary containing the point value of each card.
    player: Boolean. Default False for dealer, change to True for player.
    Returns two item tuple. First is an integer for the total points in the hand
    and second is a list of integers which are the point values of each card.
    """
    if player:
        points_sum = 0
        #the player's number of points
        points_list = []
        #the points gained from each card in the player's hand
        for _, value in enumerate(cards):
            #loops through the player's cards
            points_sum += points_dict[value]
            #deck_key[value] is the number of points for the current card
            points_list.append(points_dict[value])
            #stores the list of points gained from each card (needed for ace_switch)
        return points_sum, points_list
    points_sum = 0
    points_list = []
    for _, value in enumerate(cards):
        points_sum += points_dict[value]
        points_list.append(points_dict[value])
    return points_sum, points_list

def ascii_card(print_card):
    """
    Generates the list 'card'. Each item of the list is a different row
    of the card. Print each item of the list 'card' to a new line to generate
    an image of the playing card requested by the variable 'print_card'
    """
    top_border = f'{"":*^13}'
    filler_line = f'{"*":<12}*'
    suit_to_symbol = {'ts':'♥',
                      'es':'♠',
                      'bs':'♣',
                      'ds':'♦'}
    if print_card[:2] == '10':
        top_num = f'*{print_card[0:2]}{suit_to_symbol[print_card[-2:]]:<9}*'
        middle_symbol = f'*{suit_to_symbol[print_card[-2:]]:^11}*'
        bottom_num = f'*{suit_to_symbol[print_card[-2:]]:>9}{print_card[0:2]}*'
    else:
        top_num = f'*{print_card[0]}{suit_to_symbol[print_card[-2:]]:<10}*'
        middle_symbol = f'*{suit_to_symbol[print_card[-2:]]:^11}*'
        bottom_num = f'*{suit_to_symbol[print_card[-2:]]:>10}{print_card[0]}*'

    card = [top_border,
            top_num,
            filler_line,
            filler_line,
            middle_symbol,
            filler_line,
            filler_line,
            bottom_num,
            top_border]

    return card

def card_printer(hand, option):
    """
    prints an image of a card to the console.

    Args:
    hand: The player's or the dealer's cards
    option = 1 prints the first two cards in the list side-by-side
    option = 2 prints the first card and a face down card side-by-side
    option = 3 prints the first card
    """
    card = []
    draw_speed = 0.25 #seconds
    if option == 1:
        for row in range(9):
            card.append(f'{ascii_card(hand[0])[row]}  {ascii_card(hand[1])[row]}')
        for row in card:
            print(row)
            sleep(draw_speed)
    if option == 2:
        hidden_card = []
        for row in range(9):
            hidden_card.append(f'{"":*^13}')
        for row in range(9):
            card.append(f'{ascii_card(hand[0])[row]}  {hidden_card[row]}')
        for row in card:
            print(row)
            sleep(draw_speed)
    if option == 3:
        for row in ascii_card(hand[0]):
            print(row)
            sleep(draw_speed)

def start_dealing():
    """
    Asks for the player's input to begin dealing and checks that their
    entry is valid.

    Returns a boolean. True to start dealing and False to stop.
    """
    affirm = ['d', 'deal']
    negate = ['n', 'no thanks']

    deal = input("\nPlease enter 'deal' to begin or 'no thanks' to exit: \n").lower()
    while deal not in affirm and deal not in negate:
        deal = input("\nYour input was invalid. Please enter 'd' or 'n': \n").lower()

    if deal in affirm:
        deal = True
        print("\nLet's Play!\n")

    if deal in negate:
        deal = False
        print("\nGoodbye!\n")

    return deal

def hit_or_stand(player_points):
    """
    Asks the player whether they would like another card and checks that their
    answer is valid.

    Returns a boolean. True for hit and False for stand.
    """
    hit = ['h', 'hit']
    stand = ['s', 'stand']

    player_response = input('\nWould you like to hit or stand (h/s)?: \n').lower()
    while player_response not in hit and player_response not in stand:
        player_response = input("\nYour input was invalid. Please enter 'h' or 's': \n").lower()

    if player_response in hit:
        player_response = True
        print(f"\nYou hit on {player_points} points!\n")

    if player_response in stand:
        player_response = False
        print(f"\nYou stand on {player_points} points.\n")

    return player_response

def ace_switch(which_sum, whose_hand, points):
    """
    Searches a set of cards for aces, if points exceed 21 the number of aces
    required to bring the total under 21 are converted to a value of 1 point.

    Args:
    which_sum: pass the integer number of player's or dealer's points
    whose_hand: pass the list of player's cards or dealer's cards
    hand_values: list of integers, the number of points gained from each card.
    Returns the new total.
    """
    aces = ['Ace of Hearts', 'Ace of Clubs', 'Ace of Spades', 'Ace of Diamonds']
    for card in whose_hand:
        #loops through each card in the hand
        for ace in aces:
            #loops through each of the four aces
            if which_sum > 21:
                #checks that the total points is greater than 21
                if ace == card:
                    #checks if the hand contains an ace
                    which_sum = 0
                    points.pop(points.index(11))
                    #removes the '11' associated with the ace
                    points.append(1)
                    #places a '1' in the list of points
                    for _, value in enumerate(points):
                        which_sum += value
                        #determines the new point total by summing the list of points
    return which_sum

def dealers_turn(bust, cards, deck_list, card_points):
    """
    Performs the dealer's turn.

    Args:
    bust: integer 21,
    cards: the list of cards currently in the dealer's hand,
    deck_list: the list of cards still in the deck,
    card_points: the dictionary containing number of points each card is worth.
    Returns the number of points acquired by the dealer.
    """
    print("\nThe dealer will now take their turn.\n")
    dealers_cutoff = 17
    dealer_total = ace_switch(which_sum=card_total(cards, card_points)[0],
                              whose_hand=cards,
                              points=card_total(cards, card_points)[1])
    card_printer(cards, option=1)
    print(f"\nThe dealer reveals the {cards[1]} and has a total of {dealer_total} points.\n")
    while dealer_total < dealers_cutoff:
        print(f"\nThe dealer hits on {dealer_total} points.\n")
        dealer_cards = draw_card(1, deck_list, cards)
        dealer_total = ace_switch(which_sum=card_total(dealer_cards, card_points)[0],
                                  whose_hand=dealer_cards,
                                  points=card_total(dealer_cards, card_points)[1])
        card_printer(dealer_cards, option=3)
        print(f"\nThe dealer drew the {cards[0]} and has a total of {dealer_total} points.\n")

        if dealer_total > bust:
            print("\nThe dealer busts!\n")
            break
    print(f"\nThe dealer stands on {dealer_total} points.\n")
    return dealer_total

def winner(dealer, player, bust):
    """
    Returns the game's winner.

    Args:
    dealer: the integer number of points for the dealer
    player: the integer number of points for the player
    bust: the integer 21
    Returns a string proclaiming the winner of the game.
    """
    the_winner = ''
    if player > bust:
        the_winner = ' The dealer wins! '
    elif dealer == player:
        the_winner = ' The dealer wins! '
    elif player < dealer:
        if dealer <= bust:
            the_winner = ' The dealer wins! '
        else:
            the_winner = ' You win! '
    else:
        the_winner = ' You win! '
    return the_winner

def games_won(player_wins, dealer_wins, the_winner):
    """
    Adds a 1 to the winner's record.

    Args:
    player_wins: the integer number of times the player has won
    dealer_wins: the integer number of times the dealer has won
    the_winnner: a string indicating who won that round
    Returns a two integer tuple (player_wins, dealer_wins)
    """
    if the_winner == ' You win! ':
        player_wins += 1
    else:
        dealer_wins += 1
    return player_wins, dealer_wins

def main():
    """
    The main routine for the game blackjack
    """
    system('cls')
    greeting = 'Welcome to Blackjack!'
    print(f'{"":♣^80}\n{greeting:^80}\n{"":♠^80}\n')
    bust = 21
    player_wins = 0 #number of rounds won by the player
    dealer_wins = 0 #number of rounds won by the dealer
    while start_dealing():
        player_cards = []
        dealer_cards = []
        deck_points_and_list = build_deck()
        card_points = deck_points_and_list[0]
        deck_list = deck_points_and_list[1]

        #First draw for the player
        player_cards = draw_card(2, deck_list, player_cards, True)
        player_total = ace_switch(which_sum=card_total(player_cards, card_points, True)[0],
                                  whose_hand=player_cards,
                                  points=card_total(player_cards, card_points, True)[1])
        card_printer(player_cards, option=1)
        print(f'\nYou drew the {player_cards[0]} and the {player_cards[1]}.\n')
        print(f'\nYou have {player_total} points.\n')

        #First draw for the dealer
        dealer_cards = draw_card(2, deck_list, dealer_cards)
        dealer_total = ace_switch(which_sum=card_total(dealer_cards, card_points)[0],
                                  whose_hand=dealer_cards,
                                  points=card_total(dealer_cards, card_points)[1])
        card_printer(dealer_cards, option=2)
        print(f'\nThe dealer drew the {dealer_cards[0]} and a hidden card.\n')

        #The player's turn
        if player_total < bust:
            while hit_or_stand(player_total):
                player_cards = draw_card(1, deck_list, player_cards, True)
                player_total = ace_switch(which_sum=card_total(player_cards, card_points, True)[0],
                                          whose_hand=player_cards,
                                          points=card_total(player_cards, card_points, True)[1])
                card_printer(player_cards, option=3)
                print(f"\nYou drew the {player_cards[0]} and now have {player_total} points.\n")

                if player_total > bust:
                    print("\nYou bust!\n")
                    break
                if player_total == bust:
                    #The dealer's turn when the player obtains 21 points
                    dealer_total = dealers_turn(bust, dealer_cards, deck_list, card_points)
                    break

        #The dealer's turn when the player chooses to stand
        while player_total < bust:
            dealer_total = dealers_turn(bust, dealer_cards, deck_list, card_points)
            break

        print(f"\nThe dealer has {dealer_total} points and you have {player_total} points.\n")
        who_won = winner(dealer_total, player_total, bust)
        print(f"\n{who_won:♠^80}\n")

        #Tally to keep track of how many games each partipant has won
        player_wins = games_won(player_wins, dealer_wins, who_won)[0]
        dealer_wins = games_won(player_wins, dealer_wins, who_won)[1]
        print(f"Dealer Wins | Player Wins\n{'':*^25}")
        print(f"{dealer_wins:^12}|{player_wins:^12}")

        print("\nWould you like to play again?\n")


if __name__ == '__main__':
    main()
