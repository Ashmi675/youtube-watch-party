from collections import defaultdict

from fastapi import WebSocket, WebSocketDisconnect

from app.message_handler import handler
from app.room_manager import room_manager


class ConnectionManager:

    def __init__(self):

        self.active_connections = defaultdict(dict)



    async def connect(
        self,
        room_code,
        username,
        websocket
    ):

        await websocket.accept()

        self.active_connections[room_code][username] = websocket




    def disconnect(
        self,
        room_code,
        username
    ):

        if room_code in self.active_connections:

            if username in self.active_connections[room_code]:

                del self.active_connections[room_code][username]


            if len(self.active_connections[room_code]) == 0:

                del self.active_connections[room_code]





    async def broadcast(
        self,
        room_code,
        message,
        exclude=None
    ):


        connections = self.active_connections.get(
            room_code,
            {}
        )


        for username, connection in connections.items():

            if username != exclude:

                await connection.send_json(message)






    async def send_to_user(
        self,
        room_code,
        username,
        message
    ):


        connection = (
            self.active_connections
            .get(room_code, {})
            .get(username)
        )


        if connection:

            await connection.send_json(message)




    def get_participant_list(
        self,
        room_code
    ):

        return room_manager.get_participant_list(
            room_code
        )





manager = ConnectionManager()







async def websocket_endpoint(
    websocket: WebSocket,
    room_code: str,
    username: str
):


    print(
        "🔥 WebSocket connected:",
        username
    )



    await manager.connect(
        room_code,
        username,
        websocket
    )



    try:


        # =====================
        # JOIN
        # =====================


        join_response = handler.handle_message(

            room_code,

            username,

            {
                "action":"JOIN"
            }

        )



        print(
            "JOIN:",
            join_response
        )



        await websocket.send_json(
            join_response
        )



        # 🔥 If removed user tries to join again

        if join_response.get("type") == "KICKED":

            await websocket.close()

            return





        await manager.broadcast(

            room_code,

            {

                "type":"PARTICIPANTS_UPDATE",

                "participants":
                manager.get_participant_list(room_code)

            }

        )






        # =====================
        # EVENTS
        # =====================


        while True:


            data = await websocket.receive_json()



            print(
                "EVENT:",
                data
            )



            response = handler.handle_message(

                room_code,

                username,

                data

            )



            print(
                "RESPONSE:",
                response
            )



            action = data.get("action")






            # =====================
            # PLAYBACK
            # =====================

            if action in [

                "PLAY",
                "PAUSE",
                "SEEK"

            ]:


                await manager.broadcast(

                    room_code,

                    response,

                    exclude=username

                )






            # =====================
            # VIDEO CHANGE
            # =====================

            elif action == "CHANGE_VIDEO":


                await manager.broadcast(

                    room_code,

                    response

                )






            # =====================
            # REMOVE USER
            # =====================

            elif action == "REMOVE":


                target = data.get(
                    "target"
                )



                await manager.send_to_user(

                    room_code,

                    target,

                    {

                        "type":"KICKED"

                    }

                )



                target_socket = (
                    manager.active_connections
                    .get(room_code, {})
                    .get(target)
                )



                if target_socket:

                    await target_socket.close()





                await manager.broadcast(

                    room_code,

                    response

                )



                await manager.broadcast(

                    room_code,

                    {

                        "type":"PARTICIPANTS_UPDATE",

                        "participants":
                        manager.get_participant_list(room_code)

                    }

                )








            # =====================
            # ROLE CHANGE
            # =====================

            elif action == "ROLE":


                await manager.broadcast(

                    room_code,

                    response

                )



                await manager.broadcast(

                    room_code,

                    {

                        "type":"PARTICIPANTS_UPDATE",

                        "participants":
                        manager.get_participant_list(room_code)

                    }

                )






            else:


                await manager.broadcast(

                    room_code,

                    response

                )









    except WebSocketDisconnect:


        print(
            "❌ Disconnected:",
            username
        )



        manager.disconnect(

            room_code,

            username

        )


        # ❌ Do NOT remove participant here
        # refresh/reconnect should work



        await manager.broadcast(

            room_code,

            {

                "type":"LEFT",

                "username":username

            }

        )



        await manager.broadcast(

            room_code,

            {

                "type":"PARTICIPANTS_UPDATE",

                "participants":
                manager.get_participant_list(room_code)

            }

        )






    except Exception as e:


        print(
            "🔥 WebSocket Error:",
            e
        )


        manager.disconnect(

            room_code,

            username

        )