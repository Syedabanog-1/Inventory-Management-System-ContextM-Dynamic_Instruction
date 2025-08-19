import asyncio
from connection import config
from agents import Agent, trace, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel, Field
from typing import Dict
import rich


# Context Model (Inventory)
class Item(BaseModel):
    item_id: int
    name: str
    quantity: int
    price: float

class InventoryContext(BaseModel):
    inventory: Dict[int, Item] = Field(default_factory=dict)

# Dynamic Instructions
def dynamic_ins(wrapper: RunContextWrapper[InventoryContext], agent: Agent[InventoryContext]) -> str:
    return """
    You are an Inventory Manager.
    - To add an item, call 'add_item'.
    - To delete an item, call 'delete_item'.
    - To update an item, call 'update_item'.
    - To save and close the session, call 'save_and_close'.
    Always operate on the current inventory context.
    """
# Input Models for Tools
class AddItemInput(BaseModel):

    item_id: int = Field(..., description="Unique ID of the item")
    name: str = Field(..., description="Name of the item")
    quantity: int = Field(..., description="Quantity of the item")
    price: float = Field(..., description="Price of the item")

class DeleteItemInput(BaseModel):

    item_id: int = Field(..., description="ID of the item to delete")


class UpdateItemInput(BaseModel):

    item_id: int = Field(..., description="ID of the item to update")
    name: str = Field("", description="New name; leave empty to keep current")
    quantity: int = Field(-1, description="New quantity; use -1 to keep current")
    price: float = Field(-1.0, description="New price; use -1.0 to keep current")


# Tools
@function_tool
def add_item(wrapper: RunContextWrapper[InventoryContext], data: AddItemInput):
    wrapper.context.inventory[data.item_id] = Item(**data.model_dump())
    return f"Item '{data.name}' added with ID {data.item_id}."

@function_tool
def delete_item(wrapper: RunContextWrapper[InventoryContext], data: DeleteItemInput):
    if data.item_id in wrapper.context.inventory:
        removed = wrapper.context.inventory.pop(data.item_id)
        return f"Item '{removed.name}' deleted."
    return "Item not found."

@function_tool
def update_item(wrapper: RunContextWrapper[InventoryContext], data: UpdateItemInput):
    inv = wrapper.context.inventory
    item = inv.get(data.item_id)
    if not item:
        return "Item not found."

    updated = False
    if data.name != "":
        item.name = data.name
        updated = True
    if data.quantity != -1:
        item.quantity = data.quantity
        updated = True
    if data.price != -1.0:
        item.price = data.price
        updated = True

    if not updated:
        return "No fields to update. Provide at least one of: name, quantity, price."

    inv[data.item_id] = item
    return f"Item '{item.name}' updated: quantity={item.quantity}, price={item.price}"

@function_tool
def save_and_close(wrapper: RunContextWrapper[InventoryContext]):
    inventory_list = [item.model_dump() for item in wrapper.context.inventory.values()]
    return f"Session closed. Final inventory: {inventory_list}"


# Agent Setup
inventory_agent = Agent(
    name="InventoryAgent",
    instructions=dynamic_ins,
    tools=[add_item, delete_item, update_item, save_and_close],
)

# Runner
async def main():
    with trace("InventoryManagement Context"):
        inventory = InventoryContext(inventory={})

        
        result1 = await Runner.run(
            inventory_agent,
            "Add an item Laptop with id 1, quantity 10, and price 1200",
            run_config=config,
            context=inventory,
        )
        rich.print(result1.final_output)

        result2 = await Runner.run(
            inventory_agent,
            "Update item 1 quantity to 15 and price to 1350",
            run_config=config,
            context=inventory,
        )
        rich.print(result2.final_output)

        result3 = await Runner.run(
            inventory_agent,
            "Delete item 1",
            run_config=config,
            context=inventory,
        )
        rich.print(result3.final_output)

        result4 = await Runner.run(
            inventory_agent,
            "Save and close session",
            run_config=config,
            context=inventory,
        )
        rich.print(result4.final_output)

if __name__ == "__main__":
    asyncio.run(main())
