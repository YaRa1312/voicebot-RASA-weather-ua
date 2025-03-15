#### Weather Voice Chatbot ####

Welcome to the **Weather Voice Chatbot**! This is a simple voice-activated assistant that lets you ask about the weather in any city using your voice. The chatbot listens to your request, fetches real-time weather data, and responds with the temperature and conditions in Ukrainian.

No prior experience with Rasa or coding is needed to use this chatbot—just follow the steps below to get started!

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### What You Need ####

-- A Windows computer with a microphone.
-- An internet connection (for weather data and voice processing).
-- A little patience to set it up the first time!

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Installation ####

**Step 1: Download the Project**
1. Download the project folder voice chatbot RASA to your computer (e.g., save it to D:\voice chatbot RASA\).
-- If you received it as a ZIP file, unzip it to D:\voice chatbot RASA\.

**Step 2: Install Python**
1. If you don’t have Python installed:
-- Go to python.org, download Python 3.9 (or later), and install it.
-- During installation, check the box "Add Python to PATH".
2. Open a Command Prompt or PowerShell and check the version:
python --version
-- You should see something like Python 3.9.13.

**Step 3: Set Up the Virtual Environment**
1. Open PowerShell (search for "PowerShell" in the Start menu).
2. Navigate to the project folder:
cd D:\voice chatbot RASA
3. Activate the virtual environment:
& "D:\voice chatbot RASA\venv39\Scripts\Activate.ps1"
-- You’ll see (venv39) at the start of the line if it worked.

**Step 4: Install Dependencies**
1. While in the (venv39) environment, run:
pip install -r requirements.txt
-- This installs all necessary libraries (like rasa, gtts, pygame, etc.).
-- If requirements.txt is missing, install these manually:
pip install rasa gtts pygame speechrecognition requests

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### How to Run the Chatbot ####
You’ll need to open **three PowerShell windows** (terminals) to run the chatbot. Follow these steps carefully.

**Terminal 1: Start the Action Server**
1. Open a new PowerShell window.
2. Navigate to the project folder:
cd D:\voice chatbot RASA
3. Activate the virtual environment:
& "D:\voice chatbot RASA\venv39\Scripts\Activate.ps1"
4. Run the action server:
rasa run actions
5. Wait until you see:
Action endpoint is up and running on http://0.0.0.0:5055
-- Keep this window open!

**Terminal 2: Start the Rasa Server**
1. Open a second PowerShell window.
2. Navigate to the project folder:
cd D:\voice chatbot RASA
3. Activate the virtual environment:
& "D:\voice chatbot RASA\venv39\Scripts\Activate.ps1"
4. Run the Rasa server:
rasa run
5. Wait until you see:
Starting Rasa server on http://0.0.0.0:5005
-- Keep this window open too!

**Terminal 3: Start the Chatbot**
1. Open a third PowerShell window.
2. Navigate to the project folder:
cd D:\voice chatbot RASA
3. Activate the virtual environment:
& "D:\voice chatbot RASA\venv39\Scripts\Activate.ps1"
4. Run the chatbot:
python main.py
5. You’ll see:
pygame 2.6.1 (SDL 2.28.4, Python 3.9.13)
Hello from the pygame community. https://www.pygame.org/contribute.html
Переконайтеся, що Rasa сервер запущено командою 'rasa run'!
Слухаю... Скажіть ваш запит (наприклад, 'Яка погода в Києві сьогодні?')
--The chatbot is now listening!

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### How to Use the Chatbot ####
1. Make sure your microphone is connected and working.
2. Speak clearly into the microphone. For example, say:
-- "Яка погода в Києві сьогодні?" (What’s the weather in Kyiv today?) /jɐˈkɑ poˈɦodɐ w kɪˈji̯eβʲi sʲɔˈɦodʲnʲi/
-- "Яка погода в Парижі зараз?" (What’s the weather in Paris now?) /jɐˈkɑ poˈɦodɐ w pɐˈrʲiʒi ˈzɑrɐsʲ/
3. The chatbot will:
-- Print your request (e.g., "Ви сказали: яка погода в Києві сьогодні").
-- Respond with the weather (e.g., "Бот: Київ: 11.37°C, хмарно").
-- Speak the weather in Ukrainian (e.g., "Київ: 11.37°C, хмарно").
4. After each response, it will listen for your next question.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Notes ####
**Audio Files**: The chatbot creates temporary files like response_0.mp3, response_1.mp3, etc., in the project folder. They might not delete automatically due to Windows limitations, but this doesn’t affect the chatbot. You can delete them manually if they pile up.
**Stopping the Chatbot**: To stop, press Ctrl+C in each terminal window, starting with Terminal 3, then 2, then 1.
**Troubleshooting**:
-- No sound? Check your speakers/headphones and ensure they’re not muted.
-- Microphone not working? Test it in Windows Settings → Sound → Microphone.
-- Errors? Make sure all three terminals are running as described.