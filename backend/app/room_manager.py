from typing import Dict


class RoomManager:


    def __init__(self):

        self.rooms: Dict[str,dict] = {}




    def create_room(
        self,
        room_code
    ):


        if room_code not in self.rooms:


            self.rooms[room_code] = {


                "participants": {},


                # 🔥 Track removed users
                "removed_users": set(),


                "video": {

                    "videoId": "",

                    "currentTime": 0,

                    "playState": "paused"

                }


            }




    def room_exists(
        self,
        room_code
    ):

        return room_code in self.rooms





    def add_participant(
        self,
        room_code,
        username,
        role="participant"
    ):


        self.rooms[room_code]["participants"][username] = {

            "role": role

        }


        # if user joins again normally,
        # remove from removed list
        if username in self.rooms[room_code]["removed_users"]:

            self.rooms[room_code]["removed_users"].remove(
                username
            )





    def remove_participant(
        self,
        room_code,
        username,
        kicked=False
    ):


        if room_code in self.rooms:


            self.rooms[room_code]["participants"].pop(
                username,
                None
            )


            # only host removal will add here
            if kicked:

                self.rooms[room_code]["removed_users"].add(
                    username
                )





    def is_removed(
        self,
        room_code,
        username
    ):


        if room_code in self.rooms:

            return username in self.rooms[room_code]["removed_users"]


        return False





    def get_participants(
        self,
        room_code
    ):

        return self.rooms[room_code]["participants"]




    def get_participant_list(
        self,
        room_code
    ):


        return [

            {
                "username": username,
                "role": data["role"]
            }

            for username, data
            in self.rooms[room_code]["participants"].items()

        ]





    def get_role(
        self,
        room_code,
        username
    ):


        user = self.rooms[room_code]["participants"].get(username)


        if user:

            return user["role"]


        return None






    def assign_role(
        self,
        room_code,
        username,
        role
    ):


        if username in self.rooms[room_code]["participants"]:

            self.rooms[room_code]["participants"][username]["role"] = role






    def update_video_state(
        self,
        room_code,
        video_id,
        current_time,
        play_state
    ):


        self.rooms[room_code]["video"] = {

            "videoId": video_id,

            "currentTime": current_time,

            "playState": play_state

        }





    def get_video_state(
        self,
        room_code
    ):


        return self.rooms[room_code]["video"]





room_manager = RoomManager()