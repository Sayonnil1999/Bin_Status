import requests


class Notify:
    def __init__(self, api_key, event, d1, d2, d3, *args, **kwargs):
        self.event = event
        self.api_key = api_key
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3

    def return_url(self):
        self.url = (
            "https://maker.ifttt.com/trigger/"
            + self.event
            + "/with/key/"
            + self.api_key
        )

    def return_data(self):
        # data to be sent to api
        self.data = {
            "value1": self.d1,
            "value2": self.d2,
            "value3": self.d3,
        }

    def send(self):
        self.return_url()
        self.return_data()
        requests.post(self.url, self.data)


# notify = Notify(
#     event="notify",
#     api_key="mKaPMJdW5IuWTz-eizznhtuXU6Sr8wKSE6RT6TGNiyp",
#     d1="Dustbin 1 in 1st Floor is full.",
#     d2="Make it empty soon",
#     d3="",
# )
# notify.send()
