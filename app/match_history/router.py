import json
import random
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status

from app.matches.dao import MatchesDAO
from app.matches.models import Matches
from app.match_history.dao import MatchHistoryDAO
from app.match_history.dependencies import socket_get_user
from app.match_history.manager import ConnectionManager
from app.statistics.dao import StatisticsDAO
from app.statistics.models import Statistics
from app.users.dao import UsersDAO
from app.users.models import Users

router = APIRouter(
    prefix="/match",
    tags=["Socket"]
)

manager = ConnectionManager()


@router.websocket("/ws/{token}/{match_id}")
async def websocket_spectator_endpoint(websocket: WebSocket,
                                       match_id: int,
                                       current_user: Users = Depends(socket_get_user)):
    match: Matches = await MatchesDAO.find_one_or_none(id=match_id, end=False)
    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await manager.connect(websocket, match.id, current_user.id)
    try:
        while True:
            data_str = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, match.id)


@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, current_user: Users = Depends(socket_get_user)):
    if not current_user.inGame:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    match: Matches = await MatchesDAO.find_one_or_none_by_user(user_id=current_user.id)
    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await manager.connect(websocket, match.id, current_user.id)
    try:
        while True:
            data_str = await websocket.receive_text()
            try:
                data = json.loads(data_str)
                if data.get("board") == 'win':
                    response_dict = {'id': current_user.id,
                                     'board': 'win'
                                     }
                    response_str = json.dumps(response_dict)
                    await manager.broadcast(response_str, match.id)

                    stat: Statistics = await StatisticsDAO.find_one_or_none(user_id=current_user.id)
                    stat.rating += random.randint(20, 30)
                    await StatisticsDAO.update({'rating': stat.rating if stat.rating > 0 else 0,
                                                'games': stat.games + 1,
                                                'wins': stat.wins + 1},
                                               user_id=current_user.id)
                    await UsersDAO.update({'inGame': False}, id=current_user.id)

                    if match.white_id == current_user.id:
                        rival_id = match.black_id
                    else:
                        rival_id = match.white_id

                    stat: Statistics = await StatisticsDAO.find_one_or_none(user_id=rival_id)
                    stat.rating -= random.randint(20, 30)
                    await StatisticsDAO.update({'rating': stat.rating if stat.rating > 0 else 0,
                                                'games': stat.games + 1,
                                                'losses': stat.losses + 1},
                                               user_id=rival_id)

                    await MatchesDAO.update({'winner_id': current_user.id, 'end': True, 'time_end': datetime.now()},
                                            id=match.id)
                    await UsersDAO.update({'inGame': False},
                                          id=rival_id)
                elif data.get("board") == 'draw':
                    response_dict = {'id': current_user.id,
                                     'board': 'draw'
                                     }
                    response_str = json.dumps(response_dict)
                    await manager.broadcast(response_str, match.id)

                    stat: Statistics = await StatisticsDAO.find_one_or_none(user_id=current_user.id)
                    stat.rating += random.randint(1, 5)
                    await StatisticsDAO.update({'rating': stat.rating if stat.rating > 0 else 0,
                                                'games': stat.games + 1,
                                                'draws': stat.draws + 1},
                                               user_id=current_user.id)
                    await UsersDAO.update({'inGame': False}, id=current_user.id)

                    if match.white_id == current_user.id:
                        rival_id = match.black_id
                    else:
                        rival_id = match.white_id

                    stat: Statistics = await StatisticsDAO.find_one_or_none(user_id=rival_id)
                    stat.rating -= random.randint(1, 5)
                    await StatisticsDAO.update({'rating': stat.rating if stat.rating > 0 else 0,
                                                'games': stat.games + 1,
                                                'draws': stat.draws + 1},
                                               user_id=rival_id)

                    await MatchesDAO.update({'winner_id': None, 'end': True, 'time_end': datetime.now()},
                                            id=match.id)
                    await UsersDAO.update({'inGame': False},
                                          id=rival_id)

                elif data.get("board"):
                    # чья очередь ходить?
                    print('+')
                    history = await MatchHistoryDAO.find_all(match_id=match.id)
                    white = False
                    black = False
                    print(len(history))
                    if len(history) % 2 == 0 and match.white_id == current_user.id:
                        white = True
                    elif len(history) % 2 != 0 and match.black_id == current_user.id:
                        black = True
                    if white or black:
                        response_dict = {'id': current_user.id,
                                         'board': data.get("board")
                                         }
                        response_str = json.dumps(response_dict)
                        await manager.broadcast(response_str, match.id, )
                        await MatchHistoryDAO.add(match_id=match.id,
                                                  move_number=len(history) + 1,
                                                  board={'board': data.get("board")})

            except json.decoder.JSONDecodeError:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except WebSocketDisconnect:
        manager.disconnect(websocket, match.id)


@router.get("/test/{token}")
async def test(token: str):
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>

                var ws = new WebSocket(`ws://localhost:8000/match/ws/""" + token + """`);
                ws.onmessage = function(event) {
                    let messages = document.getElementById('messages')
                    let message = document.createElement('li')
                    let content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {
                    let input = document.getElementById("messageText");
                    let data = {
                        'board': input.value
                    };
                    ws.send(JSON.stringify(data));
                    input.value = '';
                    event.preventDefault();
                }
            </script>
        </body>
    </html>
    """)
