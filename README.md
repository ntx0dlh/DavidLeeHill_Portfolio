The purpose of this project is to help someone track their monthly expenses.  The solution is designed
for data from Chase Bank.  

###  Steps to Setup  ###
1. Use your web browser to navigate to Chase.com.  Login with your own user ID, and download your account
activity, as a CSV file.
2. Modify line 56, to match the path and filename of the file you downloaded in Step 1.
3. Modify lines 27 to 43.  Edit the pattern field of each line of the dictionary to match your own payees.
If any lines are not needed, delete them.  If any extra lines are needed, just copy the last line, and add
it to the end.
4. Modify line 53, if needed.

###  How to Execute  ###
If you are using Jupyter lab, just run all cells.  The pivot table will display at the end.

If you are using any other IDE, run all the lines, but setup a breakpoint on line 170.  When the code breaks
you can look at the parameters in memory.  Choose the parameter called "formatted_table."  That will have the
pivot table with your monthly expenses.
