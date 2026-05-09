import requests
import os
import time

ETH = os.environ["ETH_ADDRESS"]
AGENT = os.environ["AGENT_NAME"]
API = "https://bqrapnlqqtjedjyhlfci.supabase.co/functions/v1/submit-solution"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxcmFwbmxxcXRqZWRqeWhsZmNpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNzUyNjQsImV4cCI6MjA5Mzg1MTI2NH0.mf0fz6kAnK0yeAXrb-XT6yikbdRmeAq5jsikVPPhaFE"

HEADERS = {"apikey": KEY, "Content-Type": "application/json"}

def get_puzzle():
    r = requests.get(API, params={"eth": ETH}, headers=HEADERS)
    data = r.json()
    return data.get("puzzle")

def solve(prompt):
    p = prompt.strip().lower()

    if "what is" in p and "+" in p:
        parts = p.replace("what is", "").strip().split("+")
        try:
            return str(int(parts[0].strip()) + int(parts[1].strip()))
        except:
            pass

    if "what is" in p and "-" in p:
        parts = p.replace("what is", "").strip().split("-")
        try:
            return str(int(parts[0].strip()) - int(parts[1].strip()))
        except:
            pass

    if "what is" in p and "*" in p:
        parts = p.replace("what is", "").strip().split("*")
        try:
            return str(int(parts[0].strip()) * int(parts[1].strip()))
        except:
            pass

    return p

def submit(puzzle_id, answer):
    payload = {
        "eth_address": ETH,
        "agent_name": AGENT,
        "puzzle_id": puzzle_id,
        "answer": answer
    }
    r = requests.post(API, json=payload, headers=HEADERS)
    return r.json()

def main():
    print(f"Agent: {AGENT}")
    print(f"Wallet: {ETH}")
    print("Mining started...")

    while True:
        try:
            puzzle = get_puzzle()

            if not puzzle:
                print("No puzzles left. Waiting 60s...")
                time.sleep(60)
                continue

            print(f"\nPuzzle ID: {puzzle['id']}")
            print(f"Prompt: {puzzle['prompt']}")
            print(f"Category: {puzzle['category']}")
            print(f"Difficulty: {puzzle['difficulty']}")

            answer = solve(puzzle["prompt"])
            print(f"Answer: {answer}")

            result = submit(puzzle["id"], answer)
            print(f"Result: {result}")

            time.sleep(2)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
