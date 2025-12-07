import random
import gradio as gr

# --------------------------------------
# Helper: generate presents (unsorted)
# --------------------------------------

def generate_presents(user_wish: str, num_presents: int):
    """
    Create a list of presents under the tree.

    - Each present is a string (gift name).
    - The list is intentionally UNSORTED.
    - There is a random chance that Santa includes the user's wish.

    Parameters:
        user_wish (str): The gift the user asked Santa for.
        num_presents (int): How many presents are under the tree.

    Returns:
        presents (list[str]): The unsorted list of gift names.
    """
    other_gifts = [
        "Toy Car",
        "Book",
        "Headphones",
        "Puzzle",
        "Lego Set",
        "Board Game",
        "Stuffed Animal",
        "Video Game"
    ]

    presents = []

    # Fill the list with random gifts from the pool.
    for _ in range(num_presents):
        random_gift = random.choice(other_gifts)
        presents.append(random_gift)

    # Randomly decide if Santa brings the user's wish this year.
    # 65% chance the gift is in the list, 35% chance it's not
    santa_brings_wish = random.random() < 0.65

    if santa_brings_wish and num_presents > 0:
        # Replace one random present with the user's wish.
        wish_index = random.randrange(num_presents)
        presents[wish_index] = user_wish

    # Shuffle to make the list clearly unsorted.
    random.shuffle(presents)

    return presents


# --------------------------------------
# Multi-step story logic for the UI
# --------------------------------------
# We use a simple "stage" variable to control what the card shows:
#   stage 1: Ask for wish (textbox visible)
#   stage 2: Bedtime / night passes
#   stage 3: Christmas morning + tree + presents
#   stage 4: Linear search visualization
#
# We store:
#   - stage_state: which part of the story we are in
#   - wish_state: the user's chosen gift
#   - presents_state: the list of generated presents (for later search steps)
#   - search_index_state: current index being checked in linear search (-1 = not started, -2 = finished)
# --------------------------------------

def advance_story(stage, wish_state, presents_state, wish_input):
    """
    This function is called every time the user clicks the main button.
    It advances the story depending on the current stage.

    Parameters:
        stage (int): Current stage of the story.
        wish_state (str): Previously stored wish (from earlier stages).
        presents_state (list): Previously stored presents list.
        wish_input (str): The current text in the wish textbox (user input).

    Returns:
        story_card (Markdown update): Text for the main story card.
        wish_textbox (Textbox update): Show/hide textbox and its value.
        button_update (Button update): New label for the main button.
        tree_output (Markdown update): Christmas tree + presents view.
        new_stage (int): Updated stage value.
        new_wish_state (str): Updated stored wish.
        new_presents_state (list): Updated stored presents list.
    """

    # ------- STAGE 1: Ask for the user's wish -------
    if stage == 1:
        # Clean up input from the textbox (could be empty or None)
        wish_input = (wish_input or "").strip()

        # User clicked "Save my wish" without typing anything:
        # Check this first - if input is empty, show error message
        if wish_input == "":
            story_text = (
                "### ⚠️ Please enter your gift\n\n"
                "You need to type the name of a gift before continuing."
            )
            # Keep textbox visible and interactive so user can type
            wish_box = gr.update(visible=True, value="", interactive=True)
            button = gr.update(value="Save my wish")
            tree_md = gr.update(value="")
            return story_text, wish_box, button, tree_md, 1, wish_state, presents_state

        # First time here (no wish stored, but this shouldn't happen if button was clicked with empty input)
        # This case is for initial page load
        if wish_state == "" and wish_input == "":
            story_text = (
                "### 🎁 What gift do you want Santa to bring you this Christmas?\n\n"
                "Type the name of a gift below (for example: **Basketball**, **Lego Set**, or **Headphones**),\n"
                "then click **`Save my wish`**."
            )
            # Show the textbox so the user can type immediately
            # Make sure to explicitly set visible=True and clear any previous value
            wish_box = gr.update(visible=True, value="", interactive=True)
            button = gr.update(value="Save my wish")
            tree_md = gr.update(value="")
            return story_text, wish_box, button, tree_md, 1, wish_state, presents_state

        # Otherwise, we have a valid wish -> move to bedtime stage.
        new_wish = wish_input
        story_text = (
            f"### 😴 Okay, time for bed!\n\n"
            f"You told Santa you want **{new_wish}** this Christmas.\n\n"
            "Now close your eyes and go to sleep...\n\n"
            "_Click **`Go to sleep`** to fast-forward through the night._"
        )
        # Hide the textbox now; we don't need more input at this stage
        wish_box = gr.update(visible=False)
        button = gr.update(value="Go to sleep")
        tree_md = gr.update(value="")

        return story_text, wish_box, button, tree_md, 2, new_wish, presents_state

    # ------- STAGE 2: Night passes (bedtime card) -------
    elif stage == 2:
        story_text = (
            "### 🕒 The night passes...\n\n"
            "The clock ticks forward, the snow falls outside, and Santa is busy visiting houses.\n\n"
            "**Morning is here!** Let's see if Santa brought your gift.\n\n"
            "_Click **`Wake up on Christmas morning`** to check under the tree._"
        )
        wish_box = gr.update(visible=False)
        button = gr.update(value="Wake up on Christmas morning")
        tree_md = gr.update(value="")

        # Next click will go to stage 3
        return story_text, wish_box, button, tree_md, 3, wish_state, presents_state

    # ------- STAGE 3: Christmas morning + tree + presents -------
    elif stage == 3:
        # Generate a random number of presents between 5 and 12.
        num_presents = random.randint(5, 12)

        # Use our helper to create the unsorted list of presents.
        presents = generate_presents(wish_state, num_presents)

        # Build a visual tree and presents display using HTML/CSS
        # Create present boxes with indices
        present_boxes = []
        for i, gift in enumerate(presents):
            # Create colored present boxes
            present_boxes.append(
                f'<div style="display: inline-block; margin: 5px; padding: 10px; background: linear-gradient(135deg, #ff6b6b, #ee5a6f); border: 2px solid #c92a2a; border-radius: 8px; text-align: center; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);"><div style="font-size: 24px;">🎁</div><div style="font-weight: bold; color: white; font-size: 12px;">[{i}]</div><div style="color: white; font-size: 11px; margin-top: 5px;">{gift}</div></div>'
            )
        
        presents_html = ''.join(present_boxes)
        
        # Create the tree visual with HTML/CSS (single line to avoid formatting issues)
        tree_view = f'<div style="text-align: center; padding: 20px; background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 100%); border-radius: 10px; margin: 20px 0;"><h3 style="color: #2d5016; margin-bottom: 20px;">🎄 Christmas Morning!</h3><p style="color: #333; margin-bottom: 20px;">You run to the living room and see the Christmas tree...</p><div style="margin: 20px auto; display: inline-block;"><div style="color: #2d5016; font-size: 60px; line-height: 1; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎄</div></div><div style="margin-top: 30px;"><p style="font-weight: bold; color: #2d5016; margin-bottom: 15px; font-size: 16px;">Presents under the tree (unsorted):</p><div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center;">{presents_html}</div></div></div>'

        story_text = (
            "### 🎄 It's Christmas morning!\n\n"
            "These are the presents under the tree.\n"
            "In the next step, we'll use **linear search** to check them one by one\n"
            f"and see if Santa brought your **{wish_state}**.\n\n"
            "**Linear search is perfect for this situation** because:\n"
            "1. The number of gifts in an average household is not that many, usually a small number like 5-12.\n"
            "2. The gifts are **unsorted**.\n\n"
            "These are two reasons why linear searching is perfect!\n\n"
            "Click **`Start searching`** to begin the linear search!"
        )

        wish_box = gr.update(visible=False)
        button = gr.update(value="Start searching")
        tree_md = gr.update(value=tree_view)

        # Store the presents list for future steps (search).
        return story_text, wish_box, button, tree_md, 3, wish_state, presents

    # ------- STAGE 4: Linear search visualization -------
    elif stage == 4:
        # This stage is handled by separate step and reset functions
        # Return current state unchanged
        return story_text, wish_box, button, tree_md, 4, wish_state, presents_state

    # ------- Fallback (should not normally reach here) -------
    story_text = "Something went wrong with the story flow."
    wish_box = gr.update(visible=False)
    button = gr.update(value="Restart")
    tree_md = gr.update(value="")
    return story_text, wish_box, button, tree_md, 1, "", []


# --------------------------------------
# Linear Search Functions
# --------------------------------------

def create_tree_with_search(presents, wish, current_index, found_index):
    """
    Create the visual tree display with highlighted current gift being checked.
    
    Parameters:
        presents (list): List of gift names
        wish (str): The gift we're searching for
        current_index (int): Current index being checked (-1 if not started, -2 if finished)
        found_index (int): Index where gift was found (-1 if not found)
    
    Returns:
        str: HTML string for the tree and presents display
    """
    present_boxes = []
    for i, gift in enumerate(presents):
        # Determine the styling based on search state
        if found_index != -1 and i == found_index:
            # Gift found - highlight in green
            bg_color = "linear-gradient(135deg, #51cf66, #40c057)"
            border_color = "#2f9e44"
            status = "✓ FOUND!"
        elif current_index == i:
            # Currently checking this gift - highlight in yellow
            bg_color = "linear-gradient(135deg, #ffd43b, #fcc419)"
            border_color = "#f59f00"
            status = "Checking..."
        elif current_index != -1 and current_index != -2 and i < current_index:
            # Already checked - gray out
            bg_color = "linear-gradient(135deg, #868e96, #495057)"
            border_color = "#343a40"
            status = "Checked"
        else:
            # Not yet checked
            bg_color = "linear-gradient(135deg, #ff6b6b, #ee5a6f)"
            border_color = "#c92a2a"
            status = ""
        
        present_boxes.append(
            f'<div style="display: inline-block; margin: 5px; padding: 10px; background: {bg_color}; border: 3px solid {border_color}; border-radius: 8px; text-align: center; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);"><div style="font-size: 24px;">🎁</div><div style="font-weight: bold; color: white; font-size: 12px;">[{i}]</div><div style="color: white; font-size: 11px; margin-top: 5px;">{gift}</div><div style="color: white; font-size: 10px; margin-top: 3px; font-weight: bold;">{status}</div></div>'
        )
    
    presents_html = ''.join(present_boxes)
    
    tree_view = f'<div style="text-align: center; padding: 20px; background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 100%); border-radius: 10px; margin: 20px 0;"><h3 style="color: #2d5016; margin-bottom: 20px;">🎄 Christmas Morning!</h3><p style="color: #333; margin-bottom: 20px;">You run to the living room and see the Christmas tree...</p><div style="margin: 20px auto; display: inline-block;"><div style="color: #2d5016; font-size: 60px; line-height: 1; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎄</div></div><div style="margin-top: 30px;"><p style="font-weight: bold; color: #2d5016; margin-bottom: 15px; font-size: 16px;">Presents under the tree (unsorted):</p><div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center;">{presents_html}</div></div></div>'
    
    return tree_view


def step_search(stage, wish_state, presents_state, search_index):
    """
    Advance the linear search by one step.
    
    Parameters:
        stage (int): Current stage (should be 4)
        wish_state (str): The gift we're searching for
        presents_state (list): List of presents
        search_index (int): Current index being checked
    
    Returns:
        Updated UI components and search state
    """
    if stage != 4 or not presents_state:
        return None, None, None
    
    # Initialize search if not started
    if search_index == -1:
        search_index = 0
    
    # Check if we've already finished
    if search_index == -2:
        return None, None, -2
    
    # Check if current gift matches (case-insensitive comparison)
    found_index = -1
    if search_index < len(presents_state):
        if presents_state[search_index].lower() == wish_state.lower():
            found_index = search_index
    
    # Update the visual display
    tree_html = create_tree_with_search(presents_state, wish_state, search_index, found_index)
    
    # Create status message
    if found_index != -1:
        # Found it!
        status_text = (
            f"### 🎉 Found it!\n\n"
            f"After using linear search to check the presents, "
            f"we see that you are on the **nice list** and Santa brought your gift, hurray!\n\n"
            f"**{wish_state}** was found at position [{found_index}]!\n\n"
            f"**Linear search found your gift after checking {search_index + 1} present(s).**"
        )
        new_search_index = -2  # Mark as finished
        button_text = "Play again"  # Change button to "Play again"
    elif search_index >= len(presents_state) - 1:
        # Reached the end, not found
        status_text = (
            f"### 😔 Not found\n\n"
            f"After using linear search and iterating through the entire list of presents, "
            f"we see that you are on the **naughty list** and Santa didn't bring your gift.\n\n"
            f"We checked all {len(presents_state)} presents, but **{wish_state}** wasn't there.\n\n"
            f"**Linear search checked all {len(presents_state)} presents.**"
        )
        new_search_index = -2  # Mark as finished
        button_text = "Play again"  # Change button to "Play again"
    else:
        # Still searching
        current_gift = presents_state[search_index]
        is_match = current_gift.lower() == wish_state.lower()
        match_text = "✓ It's a match!" if is_match else "✗ Not a match"
        
        status_text = (
            f"### 🔍 Checking present [{search_index}]...\n\n"
            f"Current gift: **{current_gift}**\n"
            f"Looking for: **{wish_state}**\n"
            f"Result: {match_text}\n\n"
            f"**Progress:** Checked {search_index + 1} of {len(presents_state)} presents"
        )
        new_search_index = search_index + 1
        button_text = "Step"  # Keep button as "Step"
    
    return status_text, tree_html, new_search_index, button_text


def reset_search(stage, wish_state, presents_state):
    """
    Reset the search to the beginning.
    
    Parameters:
        stage (int): Current stage
        wish_state (str): The gift we're searching for
        presents_state (list): List of presents
    
    Returns:
        Updated UI components with search reset
    """
    if stage != 4 or not presents_state:
        return None, None, None
    
    # Reset to start of search
    tree_html = create_tree_with_search(presents_state, wish_state, -1, -1)
    
    status_text = (
        f"### 🔍 Ready to search!\n\n"
        f"Let's use **linear search** to find **{wish_state}**.\n\n"
        f"Click **Step** to check each present one by one, starting from position [0].\n\n"
        f"**Total presents to check:** {len(presents_state)}"
    )
    
    return status_text, tree_html, -1


def start_search(stage, wish_state, presents_state):
    """
    Transition from stage 3 to stage 4 (start the search).
    
    Parameters:
        stage (int): Current stage (should be 3)
        wish_state (str): The gift we're searching for
        presents_state (list): List of presents
    
    Returns:
        Updated UI components to start search: (status_text, tree_html, new_stage, search_index)
    """
    if stage != 3 or not presents_state or len(presents_state) == 0:
        return None
    
    # Initialize search - create tree with all presents visible (not checked yet)
    tree_html = create_tree_with_search(presents_state, wish_state, -1, -1)
    
    status_text = (
        f"### 🔍 Ready to search!\n\n"
        f"Let's use **linear search** to find **{wish_state}**.\n\n"
        f"**Linear search is great to use here** because:\n"
        f"- The list of gifts is **small**. On average, families in Canada only have 5-12 gifts under their Christmas tree.\n"
        f"- The gifts are **unsorted**.\n\n"
        f"Click **Step** to check each present one by one, starting from position [0].\n\n"
        f"**Total presents to check:** {len(presents_state)}"
    )
    
    return (status_text, tree_html, 4, -1)


# --------------------------------------
# Build the Gradio interface
# --------------------------------------

with gr.Blocks() as demo:
    gr.Markdown("## 🎄 Christmas Linear Search Game")

    # Main story "card"
    story_card = gr.Markdown(
        "**Welcome to my Christmas linear search game!** You are a kid on the night before Christmas.\n\n"
        "### 🎁 What gift do you want Santa to bring you this Christmas?\n\n"
        "Type the name of a gift below (for example: **Basketball**, **Lego Set**, or **Headphones**),\n"
        "then click **`Save my wish`**.",
        elem_id="story-card"
    )

    # Textbox for the user's wish (visible by default, will be hidden/shown as needed)
    wish_input = gr.Textbox(
        label="What gift do you want Santa to bring you this Christmas?",
        placeholder="e.g., Basketball",
        visible=True
    )

    # Area to show the tree + presents later (using HTML for visual styling)
    tree_display = gr.HTML(
        ""
    )

    # Main button that advances the story
    advance_button = gr.Button("Save my wish")

    # Search control buttons (initially hidden)
    with gr.Row(visible=False) as search_controls:
        step_button = gr.Button("Step", variant="primary")
        reset_button = gr.Button("Reset", variant="secondary")

    # Hidden state variables to keep track of the story progress and data
    stage_state = gr.State(1)     # start at stage 1 (wish input)
    wish_state = gr.State("")     # will store the user's wish
    presents_state = gr.State([]) # will store the presents list
    search_index_state = gr.State(-1)  # current search index (-1 = not started, -2 = finished)

    # When the main button is clicked, we call advance_story(...)
    def handle_advance(stage, wish, presents, wish_in):
        """Handle the main advance button click."""
        result = advance_story(stage, wish, presents, wish_in)
        new_stage = result[4]
        
        # If we're in stage 3 and clicking "Start searching", transition to stage 4
        if stage == 3 and new_stage == 3:
            # User clicked "Start searching" - transition to search mode
            search_result = start_search(3, wish, presents)
            if search_result is not None and len(search_result) == 4:
                status_text, tree_html, new_stage_val, search_idx = search_result
                return (
                    status_text,  # story_card (status text)
                    result[1],  # wish_input
                    gr.update(visible=False),  # hide advance button
                    tree_html,  # tree_display (tree with presents)
                    new_stage_val,  # stage_state (4)
                    wish,  # wish_state
                    presents,  # presents_state
                    gr.update(visible=True),  # show search controls
                    search_idx  # search_index_state (-1)
                )
        
        # For other stages, hide search controls
        show_controls = (new_stage == 4)
        return (
            result[0],  # story_card
            result[1],  # wish_input
            result[2],  # advance_button
            result[3],  # tree_display
            result[4],  # stage_state
            result[5],  # wish_state
            result[6],  # presents_state
            gr.update(visible=show_controls),  # show/hide search controls
            -1  # search_index_state
        )
    
    advance_button.click(
        fn=handle_advance,
        inputs=[stage_state, wish_state, presents_state, wish_input],
        outputs=[story_card, wish_input, advance_button, tree_display,
                 stage_state, wish_state, presents_state, search_controls, search_index_state]
    )

    # Function to restart the game from the beginning
    def restart_game():
        """Reset the game to the initial state."""
        initial_story = (
            "**Welcome to my Christmas linear search game!** You are a kid on the night before giftmas.\n\n"
            "### 🎁 What gift do you want Santa to bring you this Christmas?\n\n"
            "Type the name of a gift below (for example: **Basketball**, **Lego Set**, or **Headphones**),\n"
            "then click **`Save my wish`**."
        )
        return (
            initial_story,  # story_card
            gr.update(visible=True, value=""),  # wish_input (show and clear)
            gr.update(value="Save my wish", visible=True),  # advance_button (show and set text)
            gr.update(value=""),  # tree_display (clear)
            1,  # stage_state (back to stage 1)
            "",  # wish_state (clear)
            [],  # presents_state (clear)
            gr.update(visible=False),  # search_controls (hide)
            -1,  # search_index_state (reset)
            gr.update(value="Step")  # step_button (reset to "Step")
        )
    
    # Step button - advance search by one step, or restart if search is finished
    def handle_step(stage, wish, presents, search_idx):
        """Handle step button click."""
        # If search is finished (search_idx == -2), restart the game
        if search_idx == -2:
            return restart_game()
        
        # Otherwise, continue with search
        if stage != 4:
            return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()
        
        result = step_search(stage, wish, presents, search_idx)
        if result and len(result) >= 4:
            return (
                result[0],  # story_card
                gr.update(),  # wish_input (no change)
                gr.update(),  # advance_button (no change)
                result[1],  # tree_display
                gr.update(),  # stage_state (no change)
                gr.update(),  # wish_state (no change)
                gr.update(),  # presents_state (no change)
                gr.update(),  # search_controls (no change)
                result[2],  # search_index_state
                gr.update(value=result[3])  # step_button (update text to "Play again" if finished)
            )
        return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()
    
    step_button.click(
        fn=handle_step,
        inputs=[stage_state, wish_state, presents_state, search_index_state],
        outputs=[story_card, wish_input, advance_button, tree_display,
                 stage_state, wish_state, presents_state, search_controls, search_index_state, step_button]
    )

    # Reset button - reset search to beginning
    def handle_reset(stage, wish, presents):
        """Handle reset button click."""
        if stage != 4:
            return None, None, None
        result = reset_search(stage, wish, presents)
        if result:
            return result[0], result[1], result[2]  # story_card, tree_display, search_index_state
        return None, None, None
    
    reset_button.click(
        fn=handle_reset,
        inputs=[stage_state, wish_state, presents_state],
        outputs=[story_card, tree_display, search_index_state]
    )

# Only run the app if this file is executed directly.
if __name__ == "__main__":
    demo.launch()
