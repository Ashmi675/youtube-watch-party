import time

from app.room_manager import room_manager


class MessageHandler:

    def __init__(self, manager):
        self.manager = manager


    def can_control(self, role):

        return role in [
            "host",
            "moderator"
        ]



    def handle_message(
        self,
        room_code,
        username,
        data
    ):

        action = data.get("action")


        if action == "JOIN":

            return self.join_room(
                room_code,
                username
            )


        elif action == "PLAY":

            return self.play_video(
                room_code,
                username,
                data
            )


        elif action == "PAUSE":

            return self.pause_video(
                room_code,
                username,
                data
            )


        elif action == "SEEK":

            return self.seek_video(
                room_code,
                username,
                data
            )


        elif action == "CHANGE_VIDEO":

            return self.change_video(
                room_code,
                username,
                data
            )


        elif action == "ROLE":

            return self.change_role(
                room_code,
                username,
                data
            )


        elif action == "REMOVE":

            return self.remove_user(
                room_code,
                username,
                data
            )


        return {
            "type":"ERROR",
            "message":"Invalid action"
        }





    def join_room(
        self,
        room_code,
        username
    ):


        if not self.manager.room_exists(room_code):

            self.manager.create_room(room_code)



        # 🔥 CHECK IF USER WAS REMOVED

        if self.manager.is_removed(
            room_code,
            username
        ):

            return {

                "type":"KICKED"

            }




        participants = self.manager.get_participants(room_code)



        if username in participants:

            role = participants[username]["role"]


        else:

            role="participant"


            if len(participants)==0:

                role="host"



            self.manager.add_participant(
                room_code,
                username,
                role
            )



        return {

            "type":"JOIN",

            "username":username,

            "role":role,


            "participants":
            self.manager.get_participant_list(room_code),



            # late join sync

            "video":
            self.manager.get_video_state(room_code)

        }






    def play_video(
        self,
        room_code,
        username,
        data
    ):


        role=self.manager.get_role(
            room_code,
            username
        )


        if not self.can_control(role):

            return {
                "type":"ERROR",
                "message":"No permission"
            }




        state=self.manager.get_video_state(room_code)


        state["playState"]="playing"

        state["currentTime"]=data["currentTime"]



        return {

            "type":"PLAY",

            **state,

            "serverTime":time.time()

        }







    def pause_video(
        self,
        room_code,
        username,
        data
    ):


        role=self.manager.get_role(
            room_code,
            username
        )


        if not self.can_control(role):

            return {
                "type":"ERROR",
                "message":"No permission"
            }



        state=self.manager.get_video_state(room_code)


        state["playState"]="paused"

        state["currentTime"]=data["currentTime"]



        return {

            "type":"PAUSE",

            **state,

            "serverTime":time.time()

        }






    def seek_video(
        self,
        room_code,
        username,
        data
    ):


        role=self.manager.get_role(
            room_code,
            username
        )


        if not self.can_control(role):

            return {
                "type":"ERROR",
                "message":"No permission"
            }



        state=self.manager.get_video_state(room_code)


        state["currentTime"]=data["currentTime"]



        return {

            "type":"SEEK",

            **state,

            "serverTime":time.time()

        }







    def change_video(
        self,
        room_code,
        username,
        data
    ):


        role=self.manager.get_role(
            room_code,
            username
        )


        if not self.can_control(role):

            return {
                "type":"ERROR",
                "message":"No permission"
            }



        self.manager.update_video_state(

            room_code,

            data["videoId"],

            0,

            "paused"

        )



        return {

            "type":"CHANGE_VIDEO",

            **self.manager.get_video_state(room_code)

        }







    def change_role(
        self,
        room_code,
        username,
        data
    ):


        role=self.manager.get_role(
            room_code,
            username
        )


        if role!="host":

            return {

                "type":"ERROR",

                "message":"Only host can assign roles"

            }



        target=data["target"]

        new_role=data["role"]



        self.manager.assign_role(
            room_code,
            target,
            new_role
        )



        return {

            "type":"ROLE",

            "username":target,

            "role":new_role

        }







    def remove_user(
        self,
        room_code,
        username,
        data
    ):


        role=self.manager.get_role(
            room_code,
            username
        )


        if role!="host":

            return {

                "type":"ERROR",

                "message":"Only host can remove users"

            }




        target=data["target"]



        # 🔥 IMPORTANT
        # mark as kicked

        self.manager.remove_participant(
            room_code,
            target,
            kicked=True
        )



        return {

            "type":"REMOVE",

            "username":target

        }





handler = MessageHandler(room_manager)