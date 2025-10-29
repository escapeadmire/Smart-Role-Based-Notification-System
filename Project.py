user_database = [
    {
        "gamer_tag": "EpicBobA",
        "is_subscribed": True,     # (Role: Subscribed) 
        "is_online": True,         # (Login Status) 
        "preferred_notification_type": "Mobile Notification",
        "enabled_notifications": ["Email", "Mobile Notification", "Text"]
    },
    {
        "gamer_tag": "TF2Merc",
        "is_subscribed": False,    # (Role: Free)
        "is_online": True,         # (Login Status)
        "preferred_notification_type": "Chrome", 
        "enabled_notifications": ["Email", "Chrome"]
    },
    {
        "gamer_tag": "XxSwagLord69xX",
        "is_subscribed": True,     # (Role: Subscribed)
        "is_online": False,        # (User is offline)
        "preferred_notification_type": "Mobile Notification", 
        "enabled_notifications": ["Email", "Mobile Notification"] 
    }
]

# Helper to retrieve a user
def find_user(gamer_tag):
    """Finds a user dictionary in the database by their gamer_tag."""
    for user in user_database:
        if user["gamer_tag"] == gamer_tag:
            return user
    return None

# -a. Account Login Function
def handle_login(gamer_tag):
    """Simulates a user logging in and updates their status."""
    user = find_user(gamer_tag)
    if user is not None:
        user["is_online"] = True
        print(f"SYSTEM: {user['gamer_tag']} is now online.")
        return True
    else:
        print(f"SYSTEM: Login failed for {gamer_tag}")
        return False

# -b. Account Type Checking Function
def check_account_type(user):
    """Checks the 'role' (Subscribed or Free) of the user."""
    if user["is_subscribed"]:
        return "Subscribed"
    else:
        return "Free"

# -c. Notification Checking Function
def determine_notification_channel(user):
    """
    This is the 'smart' logic. It determines which channel to use 
    based on role, preferences, and login status.
    """
    account_type = check_account_type(user) # "Subscribed" or "Free"
    preferred = user.get("preferred_notification_type") # Use .get() for safety
    enabled = user.get("enabled_notifications", [])
    is_online = user.get("is_online", False)
    
    channel_to_use = None # Attempting to find one valid channel

    # Rule 1: Determine channel based on the account type (role)
    if account_type == "Subscribed":
        # Subscribed users get their preferred type, *if* it is enabled
        if preferred in enabled:
            channel_to_use = preferred
        # If preference is disabled, go back to Email (if enabled)
        elif "Email" in enabled:
            channel_to_use = "Email"
    
    else: # account_type == "Free"
        # Free users only get Email or Chrome, regardless of preference
        if "Email" in enabled:
            channel_to_use = "Email"
        elif "Chrome" in enabled:
            channel_to_use = "Chrome"

    # Rule 2: Filter channel based on login status
    # A user cannot receive Mobile or Chrome notifications if they are offline.
    if not is_online:
        if channel_to_use in ["Mobile Notification", "Chrome"]:
            # User is offline
            # Attempt to send an email as backup, if enabled
            if "Email" in enabled:
                 channel_to_use = "Email"
            # Or Text as a second backup
            elif "Text" in enabled:
                 channel_to_use = "Text"
            else:
                 channel_to_use = None # No valid fallback
    
    return channel_to_use

# 3. Notification Sending Function
def send_notification(user, message, channel):
    """Takes the determined channel and simulates notification sending."""
    if channel is None:
        print(f"  -> Cannot notify {user['gamer_tag']}: No valid channel found.")
        return
    
    print(f"  -> Sending to {user['gamer_tag']} via: {channel}")
    print(f"  -> Message: {message}")
    
    if channel == "Email":
        print("     (Simulating Email send...)")
    elif channel == "Text" or channel == "SMS": # Added SMS for flowchart
        print("     (Simulating Text SMS send...)")
    elif channel == "Mobile Notification":
        print("     (Simulating Mobile Push...)")
    elif channel == "Chrome":
        print("     (Simulating Chrome browser push...)")


# 2. BATCH NOTIFICATION JOB 
# -------------------------------------------------
def run_batch_notification_job():
    """
    Processes and sends a notification to all users in the database,
    as shown in the main execution block of the pseudocode.
    """
    print("STARTING NOTIFICATION BATCH")
    print("=======================================")
    message = "Your friend 'TF2Merc' just came online!"
    
    # Process notifications for all users 
    for current_user in user_database:
        print("----------------------------------------")
        print(f"Processing: {current_user['gamer_tag']} (Role: {check_account_type(current_user)})")
        print(f" (Status: Online={current_user['is_online']}, Prefers: {current_user.get('preferred_notification_type')})")
        
        # 1. Check which channel to use
        channel = determine_notification_channel(current_user)
        
        # 2. Send the notification
        send_notification(current_user, message, channel)
    
    print("=======================================")
    print("BATCH NOTIFICATION JOB COMPLETE")


# 3. INTERACTIVE LOGIN FLOW (from flowchart)
# -------------------------------------------
def process_interactive_login():
    """
    Simulates the interactive user login and account setup
    process depicted in the flowchart.
    """
    print("\n\nSTARTING INTERACTIVE LOGIN FLOW")
    print("=======================================")
    
    # Flowchart: Start -> User Login
    gamer_tag = input("Enter your gamer tag: ")
    user = find_user(gamer_tag)
    
    # Flowchart: If User exists?
    if user:
        # Flowchart: Yes -> Fetch to retrieve existing user data
        # (We already did this with find_user)
        handle_login(gamer_tag)
        print(f"Fetching data for {gamer_tag}...")
    
    else:
        # Flowchart: No -> Account Creation prompt
        print(f"User '{gamer_tag}' not found. Starting account creation...")
        
        # Flowchart: Account Type check (Request Payment Details)
        sub_choice = input("Do you want to subscribe (yes/no)? ")
        
        new_user_data = {
            "gamer_tag": gamer_tag,
            "is_online": True,
            "enabled_notifications": ["Email"] # Start with a default
        }

        # Flowchart: User Given Payment Details?
        if sub_choice.lower() == 'yes':
            payment = input("Please enter simulated payment details: ")
            if payment:
                # Flowchart: Yes -> Update User Account (Monthly)
                print("Payment received. Updating user account to send INVOICE (MONTHLY).")
                new_user_data["is_subscribed"] = True
                new_user_data["enabled_notifications"].extend(["Mobile Notification", "Text"])
            else:
                # Flowchart: No -> Update User Account (Daily)
                print("No payment details given. Account will be Free.")
                print("Updating user account to send PAYMENT DUE (DAILY).")
                new_user_data["is_subscribed"] = False
                new_user_data["enabled_notifications"].append("Chrome")
        else:
            # Flowchart: No -> Update User Account (Daily)
            print("No subscription selected. Account will be Free.")
            print("Updating user account to send PAYMENT DUE (DAILY).")
            new_user_data["is_subscribed"] = False
            new_user_data["enabled_notifications"].append("Chrome")

        # Add new user to the "database"
        user_database.append(new_user_data)
        user = new_user_data # Set the 'user' variable for the next step
        
        # Flowchart: Fetch to retrieve existing user data
        print(f"Account for {gamer_tag} created. Fetching data...")

    # Both "Yes" and "No" paths converge here
    # Flowchart: Queue Login Notification
    print("Queueing login notification...")

    # Flowchart: Is preferred notification type setup?
    if user.get("preferred_notification_type"):
        # Flowchart: Yes -> Forward pending notifications to correct function
        print(f"Preferred notification '{user['preferred_notification_type']}' is already set up.")
        print("Forwarding any pending notifications to the smart notification function...")
        
        # We use the "smart" function from the pseudocode
        # This function handles the logic for "App installed?", "SMS preferred?", etc.
        channel = determine_notification_channel(user)
        send_notification(user, "Welcome! You have 2 pending alerts.", channel)
        
    else:
        # Flowchart: No -> Show preferred notification menu
        print("Your preferred notification type is not set up.")
        print("Showing preferred notification menu...")
        print(f"Your available options: {user['enabled_notifications']}")
        new_pref = input("Please select your preferred type: ")
        
        if new_pref in user["enabled_notifications"]:
            # Flowchart: Update User Preferred Notification
            user["preferred_notification_type"] = new_pref
            print(f"Preference updated to: {new_pref}")
            # Flowchart: Queue a notification about the account update
            print("Queueing a notification about the account update...")
            send_notification(user, "Your notification preferences have been updated.", new_pref)
        else:
            print(f"'{new_pref}' is not in your list of enabled notifications. Preference not set.")

    # Flowchart: End
    print("=======================================")
    print("INTERACTIVE LOGIN FLOW COMPLETE")


# 4. MAIN EXECUTION
# -----------------
if __name__ == "__main__":
    
    # First, run the batch job
    run_batch_notification_job()
    
    # Then, simulate the interactive login 
    process_interactive_login()
    
    # Optional: Run the interactive login again to see the 'user exists' path
    # process_interactive_login()
