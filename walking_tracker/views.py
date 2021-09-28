from django.db import transaction
from django.http import HttpResponse
# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from walking_tracker.models import WalkingTrackerSession, WalkingSnapshot
from walking_tracker.serializers import WalkingTrackerSessionSerializer


def session_create_test_view(request):
    return HttpResponse("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.5.21/vue.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios@0.18.0/dist/axios.min.js"></script>
    <title>Title</title>
</head>
<body style="background-color: black; color: white;">

<div id="app">

    <div v-if="loading">
        loading
    </div>
    <div v-else>
        {{ JSON.stringify(apidata) }}
    </div>

</div>

<script>
    new Vue({
        el: "#app",
        data() {
            return {
                apidata: null,
                loading: true,
            }
        },
        methods: {
            getData: function(){
                let vinst = this;
                axios.post('http://localhost:8000/api/v1/walking_tracker/session/create/',{
                  start_date_time: new Date(),
                  end_date_time: new Date(),
                  snapshots: [
                    {
                      health_api_steps: 25,
                      pedometer_steps: 36,
                      location_data: {}
                    },
                    {
                      health_api_steps: 20,
                      pedometer_steps: 30,
                      location_data: {}
                    },
                  ]
                }, {
                  headers: {
                    'Authorization': 'token 642c39cf0e7d20dc80285691db9b8416ec9c9d17',
                    'Content-Type': 'application/json'
                  }
                })
                  .then(function (response) {
                    vinst.loading = false;
                    vinst.apidata = response.data;

                  })
                  .catch(function (error) {

                    console.log(error);

                  })
            }
        },
        created: function(){
            this.getData();
        }
    });
</script>

</body>
</html>""")


class SessionCreateView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = WalkingTrackerSessionSerializer

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            session = WalkingTrackerSession.objects.create(
                user_profile=self.request.user.user_profile,
                start_date_time=request.data['start_date_time'],
                end_date_time=request.data['end_date_time'],
            )
            snapshots = request.data['snapshots']
            snapshot_object_list = [
                WalkingSnapshot(
                    session=session,
                    latitude=snapshot.get('location_data', {}).get('latitude', None),
                    longitude=snapshot.get('location_data', {}).get('longitude', None),
                    accuracy=snapshot.get('location_data', {}).get('accuracy', None),
                    altitude=snapshot.get('location_data', {}).get('altitude', None),
                    speed=snapshot.get('location_data', {}).get('speed', None),
                    speed_accuracy=snapshot.get('location_data', {}).get('speed_accuracy', None),
                    heading=snapshot.get('location_data', {}).get('heading', None),
                    datetime=snapshot.get('location_data', {}).get('datetime', None),
                    health_api_steps=snapshot['health_api_steps'],
                    pedometer_steps=snapshot['health_api_steps'],
                ) for snapshot in snapshots
            ]
            WalkingSnapshot.objects.bulk_create(snapshot_object_list)
            return Response({'created': True}, status=201)
