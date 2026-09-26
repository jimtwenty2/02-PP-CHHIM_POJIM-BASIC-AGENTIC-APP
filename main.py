from app.agent import run_agent
from app.config import VALID_ROLES

def main():

    print("="*100)
    role = input("Role (customer/admin): ").strip().lower()
    if role not in VALID_ROLES:
        print("Invalid role. Use 'customer' or 'admin'.")
        return

    print(f"Logged in as {role}. Type 'quit' to exit.")

    while True:
        try:
            print("="*100)
            request = input("\nYour request: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if request.lower() == "quit":
            print("Goodbye!")
            break
        if not request:
            print("Request cannot be empty.")
            continue

        answer = run_agent(request, role)

        print("\nFinal answer:", answer)

if __name__ == "__main__":
    main()
