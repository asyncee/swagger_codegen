from __future__ import annotations

from swagger_codegen.api.base import BaseApi

from . import createUser
from . import createUsersWithListInput
from . import loginUser
from . import logoutUser
from . import getUserByName
from . import updateUser
from . import deleteUser


class UserApi(BaseApi):
    createUser = createUser.make_request
    createUsersWithListInput = createUsersWithListInput.make_request
    loginUser = loginUser.make_request
    logoutUser = logoutUser.make_request
    getUserByName = getUserByName.make_request
    updateUser = updateUser.make_request
    deleteUser = deleteUser.make_request
