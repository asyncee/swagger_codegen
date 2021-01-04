from __future__ import annotations

from swagger_codegen.api.base import BaseApi

from . import deleteOrder, getInventory, getOrderById, placeOrder


class StoreApi(BaseApi):
    getInventory = getInventory.make_request
    placeOrder = placeOrder.make_request
    getOrderById = getOrderById.make_request
    deleteOrder = deleteOrder.make_request
