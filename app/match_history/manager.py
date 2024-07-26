from app.matches.dao import MatchesDAO

from typing import Dict, Set, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, Set[WebSocket]] = {}
        # self.match_connections: Dict[int, List[bool, bool]] = {}
        # self.match_starts: Dict[int, bool] = {}

    async def connect(self, websocket: WebSocket, match_id: int, user_id: int):
        await websocket.accept()
        if match_id not in self.connections:
            self.connections[match_id] = set()
            # self.match_connections[match_id] = [False, False]
            # self.match_starts[match_id] = False
        self.connections[match_id].add(websocket)
        # match = await MatchesDAO.find_one_or_none(white_id=user_id, end=False)
        # if match is not None:
        #     self.match_connections[match_id][0] = True
        # else:
        #     self.match_connections[match_id][1] = True
        # if (self.match_connections[match_id][0]
        #     and self.match_connections[match_id][1]) \
        #         and not self.match_starts[match_id]:
        #     self.match_starts[match_id] = True

    # def check_status(self, match_id) -> bool:
    #     if self.match_connections[match_id][0] and self.match_connections[match_id][1]:
    #         return True
    #     return False

    def disconnect(self, websocket: WebSocket, match_id: int):
        self.connections[match_id].remove(websocket)

    async def broadcast(self, message: str, match_id: int):
        for connection in self.connections.get(match_id, []):
            await connection.send_text(message)
