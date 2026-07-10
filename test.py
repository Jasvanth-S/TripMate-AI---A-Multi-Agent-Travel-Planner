from backend import run_travel_agent

user_input = input("Enter your travel query: ")

response = run_travel_agent(user_input, "test_user")

print("FINAL RESPONSE \n")
print(response["answer"])
