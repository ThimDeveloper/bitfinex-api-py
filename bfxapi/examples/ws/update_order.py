import os
import sys

sys.path.append('../../../')

from bfxapi import Client, Order, WSEvents

API_KEY=os.getenv("BFX_KEY")
API_SECRET=os.getenv("BFX_SECRET")

bfx = Client(
  API_KEY=API_KEY,
  API_SECRET=API_SECRET,
  logLevel='DEBUG'
)

@bfx.ws.on(WSEvents.ORDER_UPDATE)
def order_updated(order):
  print ("Order updated.")
  print (order)

@bfx.ws.once(WSEvents.ORDER_UPDATE)
async def order_once_updated(order):
  # update a second time using the object function
  await order.update(price=80, amount=0.02, flags="2nd update")

@bfx.ws.once(WSEvents.ORDER_CONFIRMED)
async def trade_completed(order):
  print ("Order confirmed.")
  print (order)
  await bfx.ws.update_order(order.id, price=100, amount=0.01)

@bfx.ws.on(WSEvents.ERROR)
def log_error(msg):
  print ("Error: {}".format(msg))

@bfx.ws.once(WSEvents.AUTHENTICATED)
async def submit_order(auth_message):
  # create an inital order a really low price so it stays open
  await bfx.ws.submit_order('tBTCUSD', 10, 1, Order.Type.EXCHANGE_LIMIT)

bfx.ws.run()
