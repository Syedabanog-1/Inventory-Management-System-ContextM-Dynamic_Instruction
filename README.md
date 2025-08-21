
-----------------------------------------------------------------------------
**inventory management system where an AI agent is the “Inventory Manager”.**
-----------------------------------------------------------------------------

 Objective of the Code
 ********************

The goal of this code is to manage a small inventory of products (like a shop).
The agent can:

** Add items to the inventory

** Delete items from the inventory

** Update details of existing items (name, quantity, price)

** Save & close the session
------------------------------------------------------------------------------------------------------------------------
The system uses OpenAI Agent SDK to make the agent “intelligent” — meaning you can give it natural language commands like
-------------------------------------------------------------------------------------------------------------------------

“Update item 1 quantity to 15 and price to 1350”

and it will know which tool (update_item) to call.

 Main Objects
 ===========

** Item (class)
---------------
Represents a single product in the inventory.

Has item_id, name, quantity, and price.

Example:

{ "item_id": 1, "name": "Laptop", "quantity": 10, "price": 1200 }


** InventoryContext (class)
---------------------------
Holds all the items in a dictionary.

Dictionary format: { item_id: Item }.

Example after adding a laptop:

{
  1: Item(item_id=1, name="Laptop", quantity=10, price=1200)
}

---------------------------------------------------------------
** Input Models (AddItemInput, DeleteItemInput, UpdateItemInput)
----------------------------------------------------------------

Define the parameters each tool (function) expects.

These make sure data has the correct type (int, float, etc.).

Tools (functions decorated with @function_tool)
==============================================
add_item → add a new product

delete_item → remove a product

update_item → change details of a product

save_and_close → show final inventory

 Agent
=======
This is the “AI brain” that listens to natural language instructions.

It has access to the tools and decides which one to call.

Runner
======
Executes the agent’s thought process and tools.

Handles the conversation flow between you ↔️ agent ↔️ tools.

=========
 Workflow 
==========
Start program → we create an empty inventory.

inventory = InventoryContext(inventory={})

Run agent with a user query (like “Add an item Laptop…”).

The Runner passes your text to the inventory_agent.

The agent reads its dynamic instructions and decides:

“Oh, this is an add item request.”

It then calls the add_item function with the right parameters.

Tool executes and updates inventory.

Example: add_item puts a new Item inside inventory.

A success message is returned.

Repeat for other queries:

Update item 1 quantity to 15 and price to 1350 → agent calls update_item.

Delete item 1 → agent calls delete_item.

Save and close session → agent calls save_and_close.

Final Output → program prints results of each action using rich.print.
---------------
Simple Analogy
---------------

Think of this system like a shopkeeper’s assistant:

InventoryContext = the storage room (keeps all products).

Item = a single product box.

Tools = the assistant’s hands (add, remove, update, finalize).

Agent = the brain that understands your natural language command and decides which hand (tool) to use.

Runner = the messenger that takes your words, gives them to the assistant, and brings back the reply.
Logs = Trace WorkFlow
============
 Example Run
============
You say:
 “Add an item Laptop with id 1, quantity 10, and price 1200”
 Agent → calls add_item → Laptop added.

You say:
 “Update item 1 quantity to 15 and price to 1350”
 Agent → calls update_item → Laptop updated.

You say:
 “Delete item 1”
 Agent → calls delete_item → Laptop removed.

You say:
 “Save and close session”
 Agent → calls save_and_close → shows final inventory.

This is an AI-driven Inventory Manager that listens to natural commands, maps them to the correct tool, updates a Python dictionary as inventory, and shows results.

 Workflow Explanation
 ====================

Start → The system begins when a user makes a request.

Agent Receives Request → The Agent listens and understands what the user wants (add, update, or delete an item).

Check Inventory Context → The Agent looks at the current inventory data.

Function Tools (Add / Update / Delete) → The Agent uses the right function tool to make changes.

Update Context → The inventory context is updated with the new data.

End → The process finishes succ


https://github.com/user-attachments/assets/24a4acf8-ea30-4a74-b4ed-7a803fa2563f

<img width="1609" height="905" alt="InventoryM-Code-OutputResult" src="https://github.com/user-attachments/assets/37f0a4d0-55b1-47f3-946a-c62e5db7d51e" />
<img width="1607" height="906" alt="Log-Tracing" src="https://github.com/user-attachments/assets/0f932d10-2e75-4b70-84c5-f8ba10e648e9" />



Return + Display Result → The system shows the updated inventory to the user.

End → The process finishes successfully.
