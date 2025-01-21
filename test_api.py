import requests
import time
import sys

BASE_URL = 'http://localhost:8000/api'

def print_response(title, response):
    print(f"\n=== {title} ===")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:", response.json())
    except:
        print("Response:", response.text)
    print("=" * (len(title) + 8))
    return response.json() if response.ok else None

def test_apis():
    try:
        # Test server connection
        response = requests.get('http://localhost:8000/api/')
        if response.status_code != 200:
            print("Server is not running! Please start the server first.")
            return
    except requests.exceptions.ConnectionError:
        print("Cannot connect to server! Please start the server first.")
        return

    # 1. Register users
    player1_data = {"username": "testplayer1", "password": "testpass123"}
    player2_data = {"username": "testplayer2", "password": "testpass123"}
    
    response = requests.post(f"{BASE_URL}/register/", json=player1_data)
    player1 = print_response("Register Player 1", response)
    
    response = requests.post(f"{BASE_URL}/register/", json=player2_data)
    player2 = print_response("Register Player 2", response)

    # 2. Login and get tokens
    response = requests.post(f"{BASE_URL}/token/", json=player1_data)
    tokens1 = print_response("Login Player 1", response)
    if not tokens1:
        print("Failed to get token for player 1")
        return
    
    response = requests.post(f"{BASE_URL}/token/", json=player2_data)
    tokens2 = print_response("Login Player 2", response)
    if not tokens2:
        print("Failed to get token for player 2")
        return

    headers1 = {'Authorization': f'Bearer {tokens1["access"]}'}
    headers2 = {'Authorization': f'Bearer {tokens2["access"]}'}

    # 3. Create a game
    game_data = {"player2_id": 2}  # Player 2's ID should be 2
    response = requests.post(f"{BASE_URL}/games/", json=game_data, headers=headers1)
    game = print_response("Create Game", response)
    if not game:
        print("Failed to create game")
        return

    game_id = game['id']

    # 4. Make moves
    # Player 1 move
    move_data = {"position_x": 0, "position_y": 0}
    response = requests.post(f"{BASE_URL}/games/{game_id}/make_move/", json=move_data, headers=headers1)
    print_response("Player 1 Move", response)

    # Player 2 move
    move_data = {"position_x": 1, "position_y": 1}
    response = requests.post(f"{BASE_URL}/games/{game_id}/make_move/", json=move_data, headers=headers2)
    print_response("Player 2 Move", response)

    # Player 1 move
    move_data = {"position_x": 0, "position_y": 1}
    response = requests.post(f"{BASE_URL}/games/{game_id}/make_move/", json=move_data, headers=headers1)
    print_response("Player 1 Second Move", response)

    # 5. Get game history
    response = requests.get(f"{BASE_URL}/games/my_games/", headers=headers1)
    print_response("Get Game History", response)

    # 6. Get specific game
    response = requests.get(f"{BASE_URL}/games/{game_id}/", headers=headers1)
    print_response("Get Game Details", response)

    print("\nAll tests completed!")

if __name__ == "__main__":
    test_apis()
