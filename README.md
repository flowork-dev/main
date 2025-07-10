-----

### \#\# Step 1: Python Installation

The goal of this step is to install the "engine" that will run your code.

1.  **Extract the ZIP File**: Locate the `.zip` file containing the Python installer. Right-click it and select **"Extract All..."** to extract its contents into a folder, for example, on your Desktop.
2.  **Run the Python Installer**: Open the newly extracted folder and double-click the Python installer file (it will typically be named `python-3.10.x-amd64.exe` or something similar).
3.  **Check Important Options**: This is the most crucial part. On the first installation screen:
      * Check the box at the bottom that says **"Add Python 3.x to PATH"**. This is mandatory so the `python` command can be found from any folder.
      * Click on **"Customize installation"**.
4.  **Ensure All Features are Selected**: On the "Optional Features" screen, make sure all boxes are checked, especially **`pip`** and **`tcl/tk and IDLE`**. Then, click **"Next"**.
5.  **Choose Installation Location (Optional)**: On the "Advanced Options" screen, you can leave the installation path as the default. Consider checking the **"Install for all users"** box if you want Python to be accessible from all user profiles on the computer. Click **"Install"**.
6.  **Wait and Finish**: Let the installation process complete. If you see an option to **"Disable path length limit"** at the end, click it to prevent issues with long file paths.

-----

### \#\# Step 2: Install All Required Libraries

Now, we will install all the "parts" that the FLOWORK application needs to function.

1.  **Open Command Prompt (CMD)**:
      * Press the `Windows` key + `R`.
      * Type `cmd` and press **Enter**.
2.  **Navigate to the FLOWORK Folder**: You must tell the Command Prompt where your project folder is located. Use the `cd` (change directory) command.
      * For example, if your folder is on the Desktop:
        ```cmd
        cd C:\Users\YourUsername\Desktop\FLOWORK
        ```
      * **Quick Tip:** Type ` cd  ` (with a space), then drag and drop the `FLOWORK` folder from File Explorer directly into the Command Prompt window, and press **Enter**.
3.  **Run the Installation Command**: Once you are in the correct folder (you will see the path `C:\...\FLOWORK>` in your CMD window), type the command below and press **Enter**.
    ```cmd
    python -m pip install -r requirements.txt
    ```
      * This command reads the `requirements.txt` file and automatically downloads and installs every library listed inside it. This process may take a few minutes. Let it run until it's finished.

-----

### \#\# Step 3: Run the FLOWORK Application

With the engine (`Python`) and all the parts (`libraries`) installed, it's time to start the application.

1.  **Confirm Your Location**: Make sure your Command Prompt window is still in the `FLOWORK` folder.
2.  **Run `main.py`**: Type the following command and press **Enter**.
    ```cmd
    python main.py
    ```

The program will initialize its services (you'll see activity logs in the CMD window), and after a few moments, the main window of the FLOWORK application will appear on your screen. Congratulations, your application is now running\!
