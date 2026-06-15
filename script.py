import gradio as gr 

# In-Memory state
queue_data = {
    "current_ticket_number": 0,
    "waiting_list": [],
    "currently_serving": "-"
}

ADMIN_PASSWORD = "flaw"

# Core functions / logic
def take_ticket():
    queue_data["current_ticket_number"] += 1
    new_ticket = queue_data["current_ticket_number"]

    queue_data["waiting_list"].append(new_ticket)

    people_ahead = len(queue_data["waiting_list"]) - 1

    customer_msg = f"🎟️ Your ticket: #{new_ticket}\n👥 People ahead of you: {people_ahead}"
    waiting_count = str(len(queue_data["waiting_list"]))

    return customer_msg, queue_data["currently_serving"], waiting_count

def call_next():
    if len(queue_data["waiting_list"]) > 0:
        next_ticket = queue_data["waiting_list"].pop(0)
        queue_data["currently_serving"] = f"#{next_ticket}"
        teller_msg = f"✅ Now serving: #{next_ticket}"
    else:
        teller_msg = "⏸️ Queue is empty, No one to call."
        queue_data["currently_serving"] = "-"

    waiting_count = str(len(queue_data["waiting_list"]))

    return teller_msg, queue_data["currently_serving"], waiting_count

# Login functions

def go_to_login():
    """Hides Customer Kiosk, shows Login Screen."""
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

def cancel_login():
    """Cancels login, returns to Customer Kiosk."""
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def verify_login(password):
    """Checks password. On success, shows Admin Panel. On fail, shows error."""
    if password == ADMIN_PASSWORD:
        # Success: Show Admin, hide others, clear error
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(value="", visible=False)
    else:
        # Fail: Keep on Login, show error
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(value="❌ Incorrect password", visible=True)

def logout():
    """Logs out, clears password, returns to Customer Kiosk."""
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(value="")


# USER INTERFACE
fresh_theme = gr.themes.Soft(
    primary_hue="teal", 
    secondary_hue="sky", 
    neutral_hue="slate"
)

with gr.Blocks(theme=fresh_theme, title="LocalBank Queue") as app:
    gr.Markdown("# 🏦 LocalBank Queue Management System")
    
    # GLOBAL DISPLAY (Always visible at the top)
    with gr.Row():
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### Current Queue Status")
            with gr.Row():
                display_serving = gr.Textbox(label="Currently Serving", value="-", interactive=False, scale=1)
                display_waiting = gr.Textbox(label="Total People Waiting", value="0", interactive=False, scale=1)
                
    
    # CUSTOMER PANEL (Visible by default)
    with gr.Group(visible=True) as customer_view:
        with gr.Column(variant="panel"):
            gr.Markdown("## Customer Kiosk")
            gr.Markdown("Tap to get your number.")
            btn_take = gr.Button("Take a Ticket", variant="primary")
            customer_output = gr.Textbox(label="Your Ticket Information", interactive=False, lines=2)
            gr.HTML("<br>") 
            btn_go_login = gr.Button("Staff Login", size="sm")

    # LOGIN SCREEN (Hidden by default)
    with gr.Group(visible=False) as login_view:
        with gr.Column(variant="panel"):
            gr.Markdown("## 🔒 Staff Login")
            pwd_input = gr.Textbox(label="Password", type="password") 
            with gr.Row():
                btn_login_submit = gr.Button("Login", variant="primary")
                btn_login_cancel = gr.Button("Cancel", variant="secondary")
            login_error = gr.Markdown("", visible=False)

    # ADMIN DASHBOARD (Hidden by default)
    with gr.Group(visible=False) as admin_view:
        with gr.Column(variant="panel"):
            gr.Markdown("## Admin Dashboard")
            gr.Markdown("Call the person next in line.")
            btn_call = gr.Button("Call Next Customer", variant="primary")
            admin_output = gr.Textbox(label="Admin status", interactive=False, lines=2)
            gr.HTML("<br>")
            btn_logout = gr.Button("Log Out 🔒", size="sm", variant="secondary")

    
    # Queue Buttons
    btn_take.click(
        fn=take_ticket, 
        inputs=[], 
        outputs=[customer_output, display_serving, display_waiting]
    )
    btn_call.click(
        fn=call_next, 
        inputs=[], 
        outputs=[admin_output, display_serving, display_waiting]
    )

    # Navigation Buttons (Swapping logic)
    btn_go_login.click(
        fn=go_to_login, 
        inputs=[], 
        outputs=[customer_view, login_view, admin_view, login_error]
    )
    
    btn_login_cancel.click(
        fn=cancel_login, 
        inputs=[], 
        outputs=[customer_view, login_view, admin_view, login_error]
    )
    
    btn_login_submit.click(
        fn=verify_login, 
        inputs=[pwd_input], 
        outputs=[customer_view, login_view, admin_view, login_error]
    )
    
    btn_logout.click(
        fn=logout, 
        inputs=[], 
        outputs=[customer_view, login_view, admin_view, pwd_input]
    )

if __name__ == "__main__":
    app.launch()
    share=True