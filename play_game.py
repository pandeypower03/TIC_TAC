import os
import requests
from colorama import init, Fore, Style

# Initialize colorama for Windows
init()

BASE_URL = 'http://localhost:8000/api'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def register_user():
    """Register a new user"""
    print(f"\n{Style.BRIGHT}User Registration{Style.RESET_ALL}")
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        
        if password != confirm_password:
            print(f"{Fore.RED}Passwords don't match! Try again.{Style.RESET_ALL}")
            continue
            
        response = requests.post(f"{BASE_URL}/register/", json={
            "username": username,
            "password": password
        })
        
        if response.ok:
            print(f"{Fore.GREEN}Registration successful!{Style.RESET_ALL}")
            return username, password
        else:
            print(f"{Fore.RED}Registration failed: {response.json()}{Style.RESET_ALL}")
            retry = input("Try again? (y/n): ").lower()
            if retry != 'y':
                return None, None

def login_user():
    """Login user"""
    print(f"\n{Style.BRIGHT}User Login{Style.RESET_ALL}")
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        response = requests.post(f"{BASE_URL}/token/", json={
            "username": username,
            "password": password
        })
        
        if response.ok:
            print(f"{Fore.GREEN}Login successful!{Style.RESET_ALL}")
            return username, response.json()["access"]
        else:
            print(f"{Fore.RED}Login failed! Check your credentials.{Style.RESET_ALL}")
            retry = input("Try again? (y/n): ").lower()
            if retry != 'y':
                return None, None

def authenticate_user(player_num):
    """Authenticate a player"""
    print(f"\n{Style.BRIGHT}Player {player_num} Authentication{Style.RESET_ALL}")
    while True:
        choice = input("\n1. Register new user\n2. Login existing user\nChoice (1/2): ")
        if choice == "1":
            username, password = register_user()
            if username:
                # Auto login after registration
                return login_user()
        else:
            username, token = login_user()
            if token:
                return username, token
        
        retry = input("\nTry again? (y/n): ").lower()
        if retry != 'y':
            return None, None

class TicTacToe:
    def __init__(self, player1_token, player2_token, player1_name, player2_name):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.player1_token = player1_token
        self.player2_token = player2_token
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.game_id = None
        
        # Create game in database
        if not self.create_game():
            raise Exception("Failed to initialize game")

    def create_game(self):
        """Create a new game in the database"""
        headers = {'Authorization': f'Bearer {self.player1_token}'}
        
        # Get player2's user ID
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if not response.ok:
            print(f"{Fore.RED}Failed to get users list{Style.RESET_ALL}")
            return False
            
        users = response.json()
        player2_id = None
        for user in users:
            if user['username'] == self.player2_name:
                player2_id = user['id']
                break
                
        if not player2_id:
            print(f"{Fore.RED}Could not find player 2's ID{Style.RESET_ALL}")
            return False
            
        # Create the game
        response = requests.post(
            f"{BASE_URL}/games/",
            json={'player2_id': player2_id},
            headers=headers
        )
        
        if response.ok:
            self.game_id = response.json()['id']
            print(f"{Fore.GREEN}Game created with ID: {self.game_id}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}Failed to create game{Style.RESET_ALL}")
            return False

    def print_board(self):
        """Print the current state of the board with colors"""
        print("\nCurrent board:")
        for i, row in enumerate(self.board):
            colored_row = []
            for cell in row:
                if cell == 'X':
                    colored_row.append(f"{Fore.BLUE}X{Style.RESET_ALL}")
                elif cell == 'O':
                    colored_row.append(f"{Fore.RED}O{Style.RESET_ALL}")
                else:
                    colored_row.append(' ')
            print(" | ".join(colored_row))
            if i < 2:
                print("---------")
        print()

    def print_board_guide(self):
        """Print the board position guide"""
        print("\nBoard positions:")
        for i in range(3):
            row = [f"{i},{j}" for j in range(3)]
            print(" | ".join(row))
            if i < 2:
                print("---------")
        print()

    def make_move(self, x, y):
        """Make a move on the board"""
        if not self.game_id:
            return False, "Game not initialized properly"
            
        current_token = self.player1_token if self.current_player == 'X' else self.player2_token
        
        # Make move in the API
        headers = {'Authorization': f'Bearer {current_token}'}
        response = requests.post(
            f"{BASE_URL}/games/{self.game_id}/make_move/",
            json={'position_x': x, 'position_y': y},
            headers=headers
        )
        
        if not response.ok:
            return False, response.json().get('error', 'Invalid move')
            
        # Get updated game state
        response = requests.get(f"{BASE_URL}/games/{self.game_id}/", headers=headers)
        if not response.ok:
            return False, "Failed to get game state"
            
        game_state = response.json()
        
        # Update local board from game state
        self.board = game_state['board']
        
        # Check game status
        if game_state['status'] == 'completed':
            self.game_over = True
            if game_state.get('winner'):
                self.winner = self.current_player
                return True, "win"
            return True, "draw"
        
        # Switch players
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True, "continue"

def play_game():
    clear_screen()
    print(f"{Style.BRIGHT}Welcome to Tic-Tac-Toe!!!!{Style.RESET_ALL}")
    
    # Authenticate both players
    print("\nPlayer 1 (X) Setup:")
    player1_name, player1_token = authenticate_user(1)
    if not player1_token:
        print(f"{Fore.RED}Player 1 authentication failed. Exiting game.{Style.RESET_ALL}")
        return False
        
    print("\nPlayer 2 (O) Setup:")
    player2_name, player2_token = authenticate_user(2)
    if not player2_token:
        print(f"{Fore.RED}Player 2 authentication failed. Exiting game.{Style.RESET_ALL}")
        return False
    
    if player1_name == player2_name:
        print(f"{Fore.RED}Both players cannot be the same user! Please use different accounts.{Style.RESET_ALL}")
        return False
    
    try:
        game = TicTacToe(player1_token, player2_token, player1_name, player2_name)
    except Exception as e:
        print(f"{Fore.RED}Failed to initialize game: {str(e)}{Style.RESET_ALL}")
        return False
        
    game.print_board_guide()
    
    while not game.game_over:
        clear_screen()
        print(f"\nPlayer 1 ({Fore.BLUE}X{Style.RESET_ALL}): {player1_name}")
        print(f"Player 2 ({Fore.RED}O{Style.RESET_ALL}): {player2_name}")
        game.print_board()
        
        current_player_name = player1_name if game.current_player == 'X' else player2_name
        current_color = Fore.BLUE if game.current_player == 'X' else Fore.RED
        print(f"{current_color}{current_player_name}'s turn ({game.current_player}){Style.RESET_ALL}")
        
        try:
            x, y = map(int, input("Enter your move (row column): ").split())
            success, result = game.make_move(x, y)
            
            if not success:
                print(f"{Fore.RED}{result}{Style.RESET_ALL}")
                input("Press Enter to continue...")
                continue
                
            if result == "win":
                clear_screen()
                game.print_board()
                winner_color = Fore.BLUE if game.winner == 'X' else Fore.RED
                winner_name = player1_name if game.winner == 'X' else player2_name
                print(f"{Style.BRIGHT}{winner_color}{winner_name} wins!{Style.RESET_ALL}")
                break
                
            elif result == "draw":
                clear_screen()
                game.print_board()
                print(f"{Style.BRIGHT}Game Over! It's a draw!{Style.RESET_ALL}")
                break
                
        except ValueError:
            print(f"{Fore.RED}Invalid input! Please enter two numbers separated by space.{Style.RESET_ALL}")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
            input("Press Enter to continue...")

    # Show match history option
    print("\nWould you like to see your match history?")
    show_history = input("Enter 'y' for yes, any other key to continue: ").lower()
    if show_history == 'y':
        headers = {'Authorization': f'Bearer {player1_token}'}
        response = requests.get(f"{BASE_URL}/match-history/", headers=headers)
        if response.ok:
            history = response.json()
            print("\nMatch History:")
            print("="*50)
            for game in history:
                print(f"\nGame {game['id']}")
                print(f"Players: {game['player1_name']} vs {game['player2_name']}")
                if game['winner_name']:
                    print(f"Winner: {game['winner_name']}")
                else:
                    if game['result'] == 'ongoing':
                        print("Status: Game in progress")
                    else:
                        print("Result: Draw")
                print(f"Played on: {game['created_at']}")
                print("-"*50)
        else:
            print(f"{Fore.RED}Failed to fetch match history{Style.RESET_ALL}")

    print("\nThanks for playing!")
    while True:
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again in ['y', 'n']:
            return play_again == 'y'
        print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    # Make sure the Django server is running first
    try:
        response = requests.get('http://localhost:8000/api/')
        if response.status_code != 200:
            print(f"{Fore.RED}Server is not running! Please start the server first.{Style.RESET_ALL}")
            exit(1)
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Cannot connect to server! Please start the server first.{Style.RESET_ALL}")
        exit(1)
        
    while play_game():
        pass
