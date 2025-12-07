<h1>Linear Search Visualization</h1>

<h2>Demo video/gif/screenshot of test</h2>

<p><b>Demo:</b></p>
<video src="videos/demo.mp4" width="600" controls></video>

<br>

<p><b>Testing and Verification:</b></p>

<p>To verify that my Christmas Linear Search program works correctly and meets the project
requirements, I tested the program with a variety of inputs, including normal cases, best-case
and worst-case behavior, and user-input edge cases. I also recorded video evidence of each
test to clearly demonstrate correct functionality, UI behavior, and algorithm correctness.
Below is a description of each test and a link to the corresponding recording.</p> <br>

<p>Video 1: Normal Case (Gift Found): https://drive.google.com/file/d/1tepatJMtQOptC5nQGV8xKMZwzLvz7ZOS/view?usp=sharing
</p>

<p>In this test, I entered a normal gift request. The randomly generated presents included the gift,
and the linear search successfully found it. The video shows the present boxes updating visually
(yellow for “checking,” gray for “checked,” and green for “found”), and the program correctly
displayed the “nice list” message. This confirms that the search algorithm stops as soon as a
match is found.</p>
<br>
<p>Video 2: Gift Not Found (Naughty List Case) https://drive.google.com/file/d/1qYrSWXZXpVJABrQlurdUVRRCyz5R7Sxt/view?usp=sharing
</p>

<p>This test demonstrates the worst-case scenario. I entered a gift that was not included in the
generated list, so the algorithm checked every present. Every checked item turned gray, and the
program correctly displayed the “naughty list” message once the entire list was searched. This
verifies that the algorithm handles the “not found” condition properly and checks all N items.</p>
<br>

<p>Video 3: Best Case Scenario (Gift at First Index): https://drive.google.com/file/d/1PZ6gGAfM-g0hEasf3AKLMFMXtWJ9UfwJ/view?usp=sharing
</p>


<p>In this test, the user’s gift appeared at index 0. Linear search immediately found the match on
the first comparison, demonstrating the best-case complexity of O(1). The video clearly shows
the first present turning green and the program reporting that it required only one step.</p>
<br>
<p>Video 4: Edge Case: Blank Input Validation: https://drive.google.com/file/d/1cND9bQWPRatjuxsRh-rhXvP0NIJtRCSq/view?usp=sharing
</p>


<p>This video shows what happens when the user attempts to continue without typing any gift. The
program correctly detects the empty input and displays an error message. It prevents the user
from progressing to the next stage until a valid gift name is entered. This confirms that user
input validation is working as intended.</p>
<br>
<p>Video 5: Reset Button Test (UI State Reset): https://drive.google.com/file/d/1wz-8bT1sHqMj1Gk0jmdc1cPtjdrjf7Um/view?usp=sharing
</p>


<p>This test confirms that the interface can reset cleanly. After beginning a search, I clicked the
Reset button, and the program properly restored the initial search state. All present boxes
returned to their default colors, the search index returned to the beginning, and the user was
able to start searching again. This demonstrates that the UI is robust and handles state
transitions correctly.</p>
<br>

<p>Summary of What Was Tested</p>

<p>● Normal successful search<br>
● Worst-case scenario (gift not found after checking all presents)<br>
● Best-case scenario (gift found at the first index)<br>
● User input validation (handling empty input)<br>
● UI behavior during search<br>
● UI reset functionality</p>

<p>Results</p>

<p>● All tests passed.<br>
● The linear search algorithm consistently returned correct results.<br>
● The visualization correctly highlighted each step<br>
● The interface behaved predictably and handled edge cases properly.</p>

<h2>Problem Breakdown &amp; Computational Thinking</h2>

<p><b>Why I chose Linear Search</b></p>

<p>I chose to implement and visualize Linear Search through an educational Christmas themed
game. When the program begins, the user plays as a kid on the night before Christmas. The
user types the gift they want Santa to bring and this wish is saved for the rest of the program.
On Christmas morning, the game displays a Christmas tree and a randomly generated set of
five to twelve presents. Each present is shown as a styled gift box with an index and a gift
name. These present names are stored internally in a Python list of strings. There is a controlled
probability that the user’s chosen gift is actually in the list, which allows the game to produce
both “nice list” (found) and “naughty list” (not found) outcomes.</p>

<p>Linear Search is the most suitable algorithm for this project because the presents under a tree
are unsorted and the number of items is small. Sorting the presents or using a more complex
search algorithm would be unrealistic in this setting. Instead, Linear Search follows exactly what
the story describes. The kid checks each present in order and compares it to the gift they asked
for. If it matches, the search stops. If it does not, the kid moves forward to the next present until
the list ends. This simple step by step pattern fits perfectly with the idea of checking gifts under
a Christmas tree.</p>

<p>This algorithm is also ideal for an introductory computer science class. The logic is easy to
explain and easy to visualize. It allows the user to click through each comparison using a “Step”
button, which clearly shows how Linear Search behaves in best, worst, and average cases.
Other algorithms like Binary Search or Jump Search require the data to be sorted and involve
skipping around the list. This does not match the Christmas story, and it adds complexity that
does not help with teaching. Linear Search keeps the focus on clarity and interactivity, which is
the main purpose of the project.</p>

<p><b>Decomposition:</b><br>
I broke the project into smaller parts. First, the program collects the user’s wish as a string.
Second, the program generates a list of random gifts and sometimes replaces one of them with
the user’s wish. Third, the program displays the Christmas tree and the generated present
boxes in a Gradio interface. Fourth, when the user clicks to begin searching, the search index is
set to position zero. Finally, every click on the “Step” button advances the search by one
comparison. The game highlights the current present, updates the message describing the step,
and ends when the gift is found or all presents have been checked.</p>

<p><b>Pattern Recognition:</b><br>
Linear Search repeats the same actions in a predictable pattern. It checks the current item,
compares it with the target, and then either stops or moves to the next item. My game displays
this pattern very clearly. Each present moves through a sequence of states such as “checking”,
“checked”, or “found”. The progress is shown to the user in a consistent format. This repetition
helps demonstrate how Linear Search always examines items in order and never skips ahead.</p>

<p><b>Abstraction:</b><br>
The program hides low level details and only shows what the user needs to understand Linear
Search. The user sees a Christmas tree, present boxes, indices, labels, and messages that
explain what is happening. The user does not see the list structure, the probability logic, the
random number generation, or the internal state variables. These technical components are
abstracted away. The interface instead focuses on the core idea that Linear Search checks each
present in order until the right one is found.</p>

<p><b>Algorithm Design (Input to Processing to Output):</b><br>
The user provides their wish as text input. The program then generates a list of gift names
stored as a Python list. Once the user begins the search, the program processes the list by
comparing one element at a time to the user’s wish. After each comparison, the interface
updates the highlighted present and the message describing the progress. The final output can
be one of two messages. If the gift is found, the game states that the user is on the nice list. If
the gift is not found after all comparisons, the game states that the user is on the naughty list.
The GUI provides the entire visual experience and serves as the main way of showing how
Linear Search operates.</p>

<img src="flowchart.png" alt="Flowchart" width="800">

<h2>Steps to Run</h2>

<p><b>Run Online (Easiest Way)</b><br>
You can run the project directly in your browser here:<br>
https://huggingface.co/spaces/bcsco/linear-search-visualization<br>
No installation is needed.</p>

<p><b>Run Locally</b><br>
1. Download the project files (app.py and requirements.txt).<br>
2. Open a terminal in the project folder.<br>
3. Install dependencies:<br>
pip install -r requirements.txt<br>
4. Run the app:<br>
python app.py<br>
5. Your browser will open automatically with the interactive program.</p>

<h2>Hugging Face Link</h2>

<p>https://huggingface.co/spaces/bcsco/linear-search-visualization</p>

<h2>Author &amp; Acknowledgment</h2>

<p>This project was created by Bosco Ng for CISC 121: Intro to Computer Science.</p>

<p>I used Level 4 AI assistance throughout the development of this project, primarily through
ChatGPT 5.1, and I am acknowledging all areas where AI contributed to my work:</p>

<p>1. Formatting and Documentation Support:<br>
I used ChatGPT to help format and structure my README, including converting
sections into clear and readable HTML-style formatting.</p>

<p>2. Algorithm Selection Discussion:<br>
I discussed the advantages and disadvantages of different searching algorithms with
ChatGPT. Through this, I refined my justification for choosing Linear Search and
developed the reflection used in Step 1.</p>

<p>3. Computational Thinking Planning:<br>
During Step 2, I asked ChatGPT questions to help outline my decomposition, pattern
recognition, abstraction, and algorithm design. I wrote the final content myself, based on
the planning guidance I received.</p>

<p>4. Flowchart Creation:<br>
I used my own ideas and algorithm structure to design the flowchart, and then used
Nano Banana Pro AI to help generate a polished visual diagram based on the detailed
instructions I provided.</p>

<p>5. Code Review and Algorithm Development:<br>
I wrote the Linear Search algorithm myself, and I used ChatGPT to help review my
commenting, improve clarity, and ensure my code followed correct logic for an
introductory-level assignment.</p>

<p>6. Learning Gradio:<br>
I was not familiar with Gradio before this project, so I asked ChatGPT for guidance on
how to create a multi-step interactive UI. I used its explanations to understand key
concepts and then customized the interface to fit my Christmas-themed visualization.</p>

<p>7. Testing and Verification Planning:<br>
For Step 5, I consulted ChatGPT to decide which test cases to include. From this
guidance, I created my own videos and documentation covering normal cases, edge
cases, best-case and worst-case scenarios, and interface behavior.</p>

<p>All final decisions, code implementation, testing, and written reflections were done by me. The
AI tools listed above were used for learning support, idea refinement, explanation, and
documentation assistance.</p>
